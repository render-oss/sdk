package render

import (
	"archive/tar"
	"compress/gzip"
	"context"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"mime"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	sandboxes "github.com/render-oss/sdk/go/pkg/render/internal/client/sandboxes"
)

// File transfer content types. A single file travels as octet-stream and a
// directory as an x-tar archive the server extracts, with Content-Encoding
// carrying wire compression separately.
const (
	contentTypeOctetStream = "application/octet-stream"
	contentTypeTar         = "application/x-tar"
)

// CopyTo copies a local file or directory into the sandbox at remotePath.
//
// A relative remotePath resolves under the sandbox's home directory and an
// absolute one addresses the filesystem, as scp does. A file is uploaded as
// raw bytes. A directory is streamed as an archive the sandbox extracts at
// remotePath: names are relative to localPath, symlinks are stored rather than
// followed, and sockets, fifos and other special files are skipped.
func (s *SandboxClient) CopyTo(ctx context.Context, sandboxID, localPath, remotePath string) error {
	remotePath, err := cleanRemotePath(remotePath)
	if err != nil {
		return err
	}
	// Stat, not Lstat: a symlinked directory uploads as the directory it points
	// at. Statting before the mint also keeps a bad local path from spending a
	// token.
	info, err := os.Stat(localPath)
	if err != nil {
		return err
	}
	if !info.IsDir() && !info.Mode().IsRegular() {
		return fmt.Errorf("%s is not a file or directory; sockets, fifos and devices cannot be copied to a sandbox", localPath)
	}
	connection, err := s.mintFileToken(ctx, sandboxID, "upload", remotePath)
	if err != nil {
		return err
	}

	var body io.ReadCloser
	contentLength := int64(-1)
	if info.IsDir() {
		pr, pw := io.Pipe()
		go func() { pw.CloseWithError(writeTarGzip(pw, localPath)) }()
		// Closing the read end is what stops the producer when the request
		// dies before consuming the whole archive.
		defer func() { _ = pr.Close() }()
		body = pr
	} else {
		f, err := os.Open(localPath)
		if err != nil {
			return err
		}
		defer func() { _ = f.Close() }()
		body, contentLength = f, info.Size()
	}

	req, err := http.NewRequestWithContext(ctx, connection.Method, connection.Uri, body)
	if err != nil {
		return err
	}
	req.ContentLength = contentLength
	req.Header.Set("Authorization", "Bearer "+connection.Token)
	if info.IsDir() {
		// The archive's length is not known until it has been produced, so the
		// body goes out chunked. gzip is the wire encoding only: the server
		// gunzips it and extracts the tar underneath.
		req.Header.Set("Content-Type", contentTypeTar)
		req.Header.Set("Content-Encoding", "gzip")
	} else {
		req.Header.Set("Content-Type", contentTypeOctetStream)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to upload to sandbox: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()
	// Any 2xx, not just the 204 the sandbox sends today: the API deploys ahead
	// of the SDK, so pinning the exact code would break on a benign change.
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		respBody, _ := io.ReadAll(resp.Body)
		return sandboxHTTPError(sandboxID, resp.StatusCode, respBody, "upload")
	}
	return nil
}

// CopyFrom copies a file or directory out of a sandbox and returns the local
// path written.
//
// A directory is extracted under localPath. A file is written to localPath, or
// into it under the name the sandbox suggests when localPath is an existing
// directory. Returns ErrSandboxFileNotFound if the sandbox has no such path,
// and ErrSandboxDownload if the response is unsafe or cannot be written
// locally. Directory extraction is not atomic and may leave partial contents
// after a failure.
func (s *SandboxClient) CopyFrom(ctx context.Context, sandboxID, remotePath, localPath string) (string, error) {
	remotePath, err := cleanRemotePath(remotePath)
	if err != nil {
		return "", err
	}
	connection, err := s.mintFileToken(ctx, sandboxID, "download", remotePath)
	if err != nil {
		return "", err
	}

	ctx, idle := withIdleTimeout(ctx)
	defer idle.stop()
	req, err := http.NewRequestWithContext(ctx, connection.Method, connection.Uri, nil)
	if err != nil {
		return "", err
	}
	// No Accept-Encoding: left unset, the transport asks for gzip itself and
	// decodes it transparently.
	req.Header.Set("Authorization", "Bearer "+connection.Token)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", idleError(ctx, fmt.Errorf("failed to download sandbox file: %w", err))
	}
	defer func() { _ = resp.Body.Close() }()
	if resp.StatusCode >= 400 {
		respBody, _ := io.ReadAll(resp.Body)
		return "", sandboxHTTPError(sandboxID, resp.StatusCode, respBody, "download")
	}
	// The transport strips Content-Encoding after decoding gzip, so anything
	// left is a coding nobody undid, and writing it would corrupt the file.
	if ce := resp.Header.Get("Content-Encoding"); ce != "" && !strings.EqualFold(ce, "identity") {
		return "", fmt.Errorf("%w: cannot decode Content-Encoding %q", ErrSandboxDownload, ce)
	}

	body := idle.reader(resp.Body)
	written := localPath
	if mediaType(resp.Header.Get("Content-Type")) == contentTypeTar {
		err = extractTar(localPath, terminatedReader(body))
	} else {
		written, err = writeDownload(localPath, dispositionFilename(resp.Header.Get("Content-Disposition")), remotePath, body)
	}
	if err != nil {
		// A timeout or cancel mid-body surfaces as a read error, which
		// extraction would otherwise report as a malformed archive.
		if ctxErr := ctx.Err(); ctxErr != nil {
			return "", fmt.Errorf("failed to download sandbox file: %w", idleError(ctx, ctxErr))
		}
		if errors.Is(err, ErrSandboxDownload) {
			return "", err
		}
		return "", fmt.Errorf("%w: could not write the download to %s: %w", ErrSandboxDownload, localPath, err)
	}
	return written, nil
}

func (s *SandboxClient) mintFileToken(ctx context.Context, sandboxID, operation, remotePath string) (*sandboxes.SandboxConnectResponse, error) {
	ownerID, err := s.ownerID()
	if err != nil {
		return nil, err
	}
	resp, err := s.client.internal.ConnectSandboxFilesWithResponse(ctx, sandboxID, operation,
		&client.ConnectSandboxFilesParams{OwnerId: &ownerID, Path: remotePath})
	if err != nil {
		return nil, fmt.Errorf("failed to connect sandbox files: %w", err)
	}
	if resp.StatusCode() >= 400 {
		return nil, sandboxHTTPError(sandboxID, resp.StatusCode(), resp.Body, operation)
	}
	if resp.JSON201 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}
	return resp.JSON201, nil
}

// cleanRemotePath returns p in the canonical form the sandbox API requires,
// since the API rejects any path path.Clean would change. An empty path is an
// error rather than cleaning to ".", which would quietly transfer the home
// directory.
func cleanRemotePath(p string) (string, error) {
	if p == "" {
		return "", fmt.Errorf("remote path is required")
	}
	return path.Clean(p), nil
}

// writeTarGzip writes a gzipped tar of the tree at root to w. Entry names are
// relative to root, which itself is not emitted, so extraction lands the
// contents at the remote path rather than nested a level down.
func writeTarGzip(w io.Writer, root string) error {
	// The caller reached root via Stat, which follows symlinks. Follow it here
	// too: walking the link itself would produce an empty archive.
	root, err := filepath.EvalSymlinks(root)
	if err != nil {
		return err
	}
	gz := gzip.NewWriter(w)
	tw := tar.NewWriter(gz)
	err = filepath.WalkDir(root, func(p string, d fs.DirEntry, err error) error {
		if err != nil || p == root {
			return err
		}
		info, err := d.Info()
		if err != nil {
			return err
		}
		var link string
		switch {
		case info.Mode()&fs.ModeSymlink != 0:
			if link, err = os.Readlink(p); err != nil {
				return err
			}
		case !info.IsDir() && !info.Mode().IsRegular():
			// Sockets, fifos and devices: skipped on the way in, as the
			// sandbox skips them on the way out.
			return nil
		}
		hdr, err := tar.FileInfoHeader(info, link)
		if err != nil {
			return err
		}
		rel, err := filepath.Rel(root, p)
		if err != nil {
			return err
		}
		hdr.Name = filepath.ToSlash(rel)
		if info.IsDir() {
			hdr.Name += "/"
		}
		if err := tw.WriteHeader(hdr); err != nil {
			return err
		}
		if !info.Mode().IsRegular() {
			return nil
		}
		f, err := os.Open(p)
		if err != nil {
			return err
		}
		defer func() { _ = f.Close() }()
		_, err = io.Copy(tw, f)
		return err
	})
	if err != nil {
		return err
	}
	if err := tw.Close(); err != nil {
		return err
	}
	return gz.Close()
}

// writeDownload writes a single downloaded file. It lands in a temp file next
// to the destination first, so an interrupted transfer never leaves a truncated
// file looking complete.
func writeDownload(localPath, filename, remotePath string, r io.Reader) (string, error) {
	dest := localPath
	// Writing into an existing directory mirrors cp and scp. The name comes
	// from the sandbox, so it is reduced to one path component.
	if info, err := os.Stat(localPath); err == nil && info.IsDir() {
		name := baseName(filename)
		if name == "" {
			name = baseName(remotePath)
		}
		if name == "" {
			return "", fmt.Errorf("%w: cannot name the downloaded file under %s: the sandbox suggested no usable filename", ErrSandboxDownload, localPath)
		}
		dest = filepath.Join(localPath, name)
	}

	abs, err := filepath.Abs(dest)
	if err != nil {
		return "", err
	}
	f, err := os.CreateTemp(filepath.Dir(abs), ".render-partial-")
	if err != nil {
		return "", err
	}
	// A no-op once the rename has moved the temp file away.
	defer func() { _ = os.Remove(f.Name()) }()
	defer func() { _ = f.Close() }()
	if _, err := io.Copy(f, r); err != nil {
		return "", err
	}
	// CreateTemp opens 0o600. Widen to what a plain create would produce under
	// a default umask.
	if err := f.Chmod(0o644); err != nil {
		return "", err
	}
	if err := f.Close(); err != nil {
		return "", err
	}
	return dest, os.Rename(f.Name(), dest)
}

// extractTar extracts an archive from the (untrusted) sandbox under dest.
//
// os.Root refuses any entry that names or links its way out of dest. A symlink
// pointing outside dest still gets created, matching what tar does, but
// nothing can be written through it.
func extractTar(dest string, r io.Reader) error {
	if err := os.MkdirAll(dest, 0o750); err != nil {
		return err
	}
	root, err := os.OpenRoot(dest)
	if err != nil {
		return err
	}
	defer func() { _ = root.Close() }()

	tr := tar.NewReader(r)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			if errors.Is(err, ErrSandboxDownload) {
				return err
			}
			return fmt.Errorf("%w: sandbox archive is malformed: %w", ErrSandboxDownload, err)
		}
		name, err := entryName(hdr.Name)
		if err != nil {
			return err
		}
		if name == "" {
			continue
		}
		// Masking to 0o777 drops setuid/setgid, which an archive from the
		// sandbox has no business setting locally; the or'd owner bits keep the
		// tree writable enough to finish extracting into.
		mode := fs.FileMode(hdr.Mode) & 0o777

		switch hdr.Typeflag {
		case tar.TypeDir:
			err = root.MkdirAll(name, mode|0o700)
		case tar.TypeReg:
			err = extractFile(root, name, mode|0o600, tr)
		case tar.TypeSymlink:
			if err = makeParents(root, name); err == nil {
				if err = clearTarget(root, name); err == nil {
					err = root.Symlink(hdr.Linkname, name)
				}
			}
		case tar.TypeLink:
			var source string
			if source, err = entryName(hdr.Linkname); err == nil && source == "" {
				err = fmt.Errorf("%w: archive hard link to %q is not a file", ErrSandboxDownload, hdr.Linkname)
			}
			if err == nil {
				if err = makeParents(root, name); err == nil {
					if err = clearTarget(root, name); err == nil {
						err = root.Link(source, name)
					}
				}
			}
		}
		// Devices, fifos, and other special entries are skipped.
		if err != nil {
			return err
		}
	}
}

func extractFile(root *os.Root, name string, mode fs.FileMode, r io.Reader) error {
	if err := makeParents(root, name); err != nil {
		return err
	}
	// Recreate every non-directory target instead of truncating an existing
	// regular file, which may be a hard link to an inode outside root.
	if err := clearTarget(root, name); err != nil {
		return err
	}
	f, err := root.OpenFile(name, os.O_CREATE|os.O_EXCL|os.O_WRONLY, mode)
	if err != nil {
		return err
	}
	_, err = io.Copy(f, r)
	if closeErr := f.Close(); err == nil {
		err = closeErr
	}
	return err
}

func makeParents(root *os.Root, name string) error {
	if dir := path.Dir(name); dir != "." {
		return root.MkdirAll(dir, 0o750)
	}
	return nil
}

// clearTarget removes whatever sits at name so an archive entry can take its
// place. A directory is refused rather than emptied: a download quietly
// deleting a local tree is a surprise nobody asks for.
func clearTarget(root *os.Root, name string) error {
	info, err := root.Lstat(name)
	if errors.Is(err, fs.ErrNotExist) {
		return nil
	}
	if err != nil {
		return err
	}
	if info.IsDir() {
		return fmt.Errorf("%w: archive entry %q would replace a directory", ErrSandboxDownload, name)
	}
	return root.Remove(name)
}

// entryName cleans a tar entry name. It returns "" for the archive's own root
// entry and an error for a name pointing anywhere but under the destination.
func entryName(name string) (string, error) {
	clean := path.Clean(name)
	if clean == "." || clean == "/" {
		return "", nil
	}
	if !filepath.IsLocal(filepath.FromSlash(clean)) {
		return "", fmt.Errorf("%w: archive entry %q escapes the destination", ErrSandboxDownload, name)
	}
	return clean, nil
}

// terminatedReader reports the stream's EOF as a truncated archive. The tar
// reader stops at the end-of-archive marker, so a complete archive never
// reaches EOF; a truncated one does, and would otherwise read as a clean end
// if it stopped on a 512-byte boundary.
func terminatedReader(r io.Reader) io.Reader {
	return readerFunc(func(p []byte) (int, error) {
		n, err := r.Read(p)
		if err == io.EOF {
			err = fmt.Errorf("%w: sandbox archive ended without an end-of-archive marker", ErrSandboxDownload)
		}
		return n, err
	})
}

func mediaType(header string) string {
	mt, _, _ := mime.ParseMediaType(header)
	return mt
}

// dispositionFilename is the filename a Content-Disposition header suggests.
func dispositionFilename(header string) string {
	_, params, err := mime.ParseMediaType(header)
	if err != nil {
		return ""
	}
	return params["filename"]
}

// baseName reduces an untrusted name to a single path component, or "" if
// nothing usable is left. Both separators and a drive prefix count on every
// platform, which is the strictest reading available.
func baseName(name string) string {
	name = name[strings.LastIndexAny(name, `/\`)+1:]
	if len(name) >= 2 && name[1] == ':' {
		name = name[2:]
	}
	if name == "." || name == ".." {
		return ""
	}
	return name
}
