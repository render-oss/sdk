package render

import (
	"archive/tar"
	"bytes"
	"compress/gzip"
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"testing/iotest"
	"time"

	"github.com/stretchr/testify/require"
)

const sandboxJSON = `{"id":"sbx-1","status":"running","plan":"starter","networkPolicy":{"type":"allow-all","default":"allow-all"},"region":"oregon","timeoutSeconds":60,"createdAt":"2026-01-01T00:00:00Z"}`

// newSandboxTestClient serves the API under /v1 and the sandbox proxy under
// /proxy. Every token mint points at /proxy/<operation>.
func newSandboxTestClient(t *testing.T, proxy http.HandlerFunc) *SandboxClient {
	t.Setenv(UseLocalDev, "")
	t.Setenv(LocalDevURL, "")
	mux := http.NewServeMux()
	var srv *httptest.Server
	mint := func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "tea-1", r.URL.Query().Get("ownerId"))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		method := map[string]string{"stream": "POST", "upload": "PUT", "download": "GET"}[r.PathValue("op")]
		_, _ = fmt.Fprintf(w, `{"executionId":"e","expiresAt":"2026-01-01T00:00:00Z","method":%q,"token":"tok","uri":"%s/proxy/%s"}`,
			method, srv.URL, r.PathValue("op"))
	}
	mux.HandleFunc("POST /v1/sandboxes/sbx-1/runs/{op}/token", mint)
	mux.HandleFunc("POST /v1/sandboxes/sbx-1/files/{op}/token", mint)
	mux.HandleFunc("POST /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"ownerId":"tea-1","region":"ohio","plan":"pro"}`, string(body))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(sandboxJSON))
	})
	mux.HandleFunc("GET /v1/sandboxes", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "running", r.URL.Query().Get("status"))
		w.Header().Set("Content-Type", "application/json")
		_, _ = fmt.Fprintf(w, `[{"cursor":"c1","sandbox":%s}]`, sandboxJSON)
	})
	mux.HandleFunc("GET /v1/sandboxes/missing", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusNotFound)
		_, _ = w.Write([]byte(`{"message":"not found"}`))
	})
	mux.HandleFunc("DELETE /v1/sandbox-groups/grp-1/snapshots/snap-1", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusConflict)
		_, _ = w.Write([]byte(`{"code":"snapshot_creating","message":"still creating"}`))
	})
	mux.HandleFunc("/proxy/", func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "Bearer tok", r.Header.Get("Authorization"))
		proxy(w, r)
	})
	srv = httptest.NewServer(mux)
	t.Cleanup(srv.Close)

	c, err := NewClient(WithBaseURL(srv.URL), WithToken("t"), WithOwnerID("tea-1"), WithRegion("ohio"))
	require.NoError(t, err)
	return c.Experimental.Sandboxes
}

func TestSandboxAPI(t *testing.T) {
	sandboxes := newSandboxTestClient(t, nil)
	ctx := context.Background()

	sbx, err := sandboxes.Create(ctx, CreateSandboxParams{Plan: "pro"})
	require.NoError(t, err)
	require.Equal(t, &Sandbox{ID: "sbx-1", Status: "running", Plan: "starter", NetworkPolicy: "allow-all",
		Region: "oregon", TimeoutSeconds: 60, CreatedAt: sbx.CreatedAt}, sbx)

	list, err := sandboxes.List(ctx, &ListSandboxesOptions{Status: []string{"running"}})
	require.NoError(t, err)
	require.Len(t, list.Sandboxes, 1)
	require.Equal(t, "c1", *list.NextCursor)

	_, err = sandboxes.FromID(ctx, "missing")
	require.ErrorIs(t, err, ErrSandboxNotFound)

	err = sandboxes.Snapshots.Delete(ctx, "grp-1", "snap-1")
	require.ErrorIs(t, err, ErrSnapshotNotReady)
	require.ErrorContains(t, err, "still creating")

	_, err = sandboxes.Create(ctx, CreateSandboxParams{SnapshotID: "a", SnapshotName: "b"})
	require.ErrorContains(t, err, "mutually exclusive")
}

func TestSandboxExec(t *testing.T) {
	stream := ": keep-alive\n\n" +
		"event: output\ndata: {\"stream\":\"stdout\",\ndata: \"data\":\"hi\\n\"}\n\n" +
		"event: exit\ndata: {\"exit_code\":3}\n\n"
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		require.JSONEq(t, `{"command":"echo hi"}`, string(body))
		if r.URL.Path == "/proxy/stream" {
			_, _ = w.Write([]byte(stream))
		}
	})

	var events []SandboxExecEvent
	for event, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		require.NoError(t, err)
		events = append(events, event)
	}
	require.Equal(t, []SandboxExecEvent{SandboxExecOutput{Stream: "stdout", Data: "hi\n"}, SandboxExecExit{ExitCode: 3}}, events)

	stream = "event: error\ndata: {\"status\":500,\"message\":\"boom\"}\n\n"
	var streamErr *SandboxExecStreamError
	for _, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		require.ErrorAs(t, err, &streamErr)
	}
	require.Equal(t, &SandboxExecStreamError{Status: 500, Message: "boom"}, streamErr)

	stream = "event: output\ndata: {\"stream\":\"stdout\",\"data\":\"x\"}\n\n"
	var last error
	for _, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		last = err
	}
	require.ErrorIs(t, last, ErrSandboxExec)

	// An exit event cut off before its terminating blank line is not an exit.
	stream = "event: exit\ndata: {\"exit_code\":0}\n"
	events = nil
	for event, err := range sandboxes.Exec(context.Background(), "sbx-1", "echo hi") {
		events = append(events, event)
		last = err
	}
	require.Equal(t, []SandboxExecEvent{nil}, events)
	require.ErrorContains(t, last, "without an exit event")
}

func TestSSEEventsReadError(t *testing.T) {
	reset := errors.New("connection reset")
	var readErr error
	var names []string
	for name := range sseEvents(io.MultiReader(strings.NewReader("event: output\ndata: {\"str"), iotest.ErrReader(reset)), &readErr) {
		names = append(names, name)
	}
	require.Empty(t, names, "half-received event yielded")
	require.ErrorIs(t, readErr, reset)
}

// cancelMidBody serves a partial body of the given type, then cancels the
// client's context and holds the connection open. The pause lets the client
// get past Do and block reading the body, so the cancel lands mid-body.
func cancelMidBody(contentType, body string, cancel context.CancelFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		_, _ = io.Copy(io.Discard, r.Body)
		w.Header().Set("Content-Type", contentType)
		_, _ = w.Write([]byte(body))
		w.(http.Flusher).Flush()
		time.Sleep(100 * time.Millisecond)
		cancel()
		<-r.Context().Done()
	}
}

func TestSandboxStreamsReportCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	sandboxes := newSandboxTestClient(t, cancelMidBody("text/event-stream", "event: output\ndata: {\"str", cancel))
	var last error
	for _, err := range sandboxes.Exec(ctx, "sbx-1", "echo hi") {
		last = err
	}
	require.ErrorIs(t, last, context.Canceled)
	require.NotErrorIs(t, last, ErrSandboxExec)

	ctx, cancel = context.WithCancel(context.Background())
	sandboxes = newSandboxTestClient(t, cancelMidBody(contentTypeTar, strings.Repeat("x", 100), cancel))
	_, err := sandboxes.CopyFrom(ctx, "sbx-1", "/tmp/dir", t.TempDir())
	require.ErrorIs(t, err, context.Canceled)
	require.NotErrorIs(t, err, ErrSandboxDownload)

	require.ErrorIs(t, ErrSandboxIdleTimeout, context.DeadlineExceeded)
}

// TestSandboxCopyRoundTrip uploads a directory and downloads the same archive
// back, so it covers both writeTarGzip and extractTar.
func TestSandboxCopyRoundTrip(t *testing.T) {
	var archive []byte
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "PUT":
			require.Equal(t, contentTypeTar, r.Header.Get("Content-Type"))
			require.Equal(t, "gzip", r.Header.Get("Content-Encoding"))
			gz, err := gzip.NewReader(r.Body)
			require.NoError(t, err)
			archive, err = io.ReadAll(gz)
			require.NoError(t, err)
			w.WriteHeader(http.StatusNoContent)
		case "GET":
			w.Header().Set("Content-Type", contentTypeTar)
			_, _ = w.Write(archive)
		}
	})
	ctx := context.Background()

	src := t.TempDir()
	require.NoError(t, os.MkdirAll(filepath.Join(src, "sub"), 0o755))
	require.NoError(t, os.WriteFile(filepath.Join(src, "sub", "a.txt"), []byte("hello"), 0o644))
	require.NoError(t, os.Symlink("sub/a.txt", filepath.Join(src, "link")))
	require.NoError(t, sandboxes.CopyTo(ctx, "sbx-1", src, "dir/"))

	dest := filepath.Join(t.TempDir(), "out")
	written, err := sandboxes.CopyFrom(ctx, "sbx-1", "dir", dest)
	require.NoError(t, err)
	require.Equal(t, dest, written)
	data, err := os.ReadFile(filepath.Join(dest, "link"))
	require.NoError(t, err)
	require.Equal(t, "hello", string(data))
}

func TestSandboxCopyFromFile(t *testing.T) {
	sandboxes := newSandboxTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Disposition", `attachment; filename="../../evil.txt"`)
		_, _ = w.Write([]byte("data"))
	})
	dir := t.TempDir()
	written, err := sandboxes.CopyFrom(context.Background(), "sbx-1", "/tmp/x.txt", dir)
	require.NoError(t, err)
	require.Equal(t, filepath.Join(dir, "evil.txt"), written)
	entries, err := os.ReadDir(dir)
	require.NoError(t, err)
	require.Len(t, entries, 1, "temp file left behind")
}

func TestExtractTarRefusesUnsafeArchives(t *testing.T) {
	build := func(complete bool, headers ...*tar.Header) io.Reader {
		var buf bytes.Buffer
		tw := tar.NewWriter(&buf)
		for _, h := range headers {
			require.NoError(t, tw.WriteHeader(h))
			_, _ = tw.Write(make([]byte, h.Size))
		}
		if complete {
			require.NoError(t, tw.Close())
		} else {
			require.NoError(t, tw.Flush())
		}
		return terminatedReader(&buf)
	}
	file := func(name string) *tar.Header {
		return &tar.Header{Name: name, Typeflag: tar.TypeReg, Mode: 0o644, Size: 1}
	}

	for name, archive := range map[string]io.Reader{
		"dot-dot":      build(true, file("../evil")),
		"absolute":     build(true, file("/etc/evil")),
		"through link": build(true, &tar.Header{Name: "l", Typeflag: tar.TypeSymlink, Linkname: "/tmp"}, file("l/evil")),
		"truncated":    build(false, file("a")),
		"hardlink out": build(true, &tar.Header{Name: "h", Typeflag: tar.TypeLink, Linkname: "../x"}),
		"replaces dir": build(true, &tar.Header{Name: "d/", Typeflag: tar.TypeDir, Mode: 0o755}, &tar.Header{Name: "d", Typeflag: tar.TypeSymlink, Linkname: "x"}),
	} {
		t.Run(name, func(t *testing.T) {
			require.Error(t, extractTar(t.TempDir(), archive))
		})
	}
	require.NoError(t, extractTar(t.TempDir(), build(true, file("ok"))))
}
