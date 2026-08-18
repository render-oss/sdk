"""Filesystem side of sandbox file transfer.

Nothing here talks to the sandbox, so the async and sync sandbox APIs both
import this module unchanged and unasync leaves it alone. The one pair that
differs between them, arun_blocking and run_blocking, is defined here for
the same reason: a transformed module cannot hold both.
"""

from __future__ import annotations

import asyncio
import contextlib
import email.message
import ntpath
import os
import posixpath
import stat
import tarfile
import tempfile
from collections.abc import Callable
from types import TracebackType
from typing import IO, Any, TypeVar, cast

from render_sdk.experimental.sandbox.errors import SandboxDownloadError

_T = TypeVar("_T")

_PARTIAL_PREFIX = ".render-partial-"

# Codings httpx negotiates and decodes before we see the body. Anything else
# arrives as-is, and passing those bytes on means writing them to disk as the
# file or reading them as a tar, so we refuse instead.
_DECODED_CODINGS = frozenset({"gzip", "x-gzip"})


async def arun_blocking(func: Callable[..., _T], *args: Any) -> _T:
    """Run a blocking filesystem call off the event loop."""
    return await asyncio.to_thread(func, *args)


def run_blocking(func: Callable[..., _T], *args: Any) -> _T:
    """Run a blocking filesystem call. The sync client owns its own thread."""
    return func(*args)


def normalize_remote_path(path: str) -> str:
    """Clean a remote path the way the sandbox API requires.

    The API rejects any path that Go's path.Clean would change, and the CLI
    cleans before it mints a token, so `render sandbox cp` and the SDK agree on
    what a path means. An empty path raises rather than cleaning to ".", which
    would quietly transfer the home directory, and matches what copy_to does.
    """
    if not path:
        raise ValueError("remote_path is required")
    cleaned = posixpath.normpath(path)
    # normpath keeps exactly two leading slashes, which POSIX reserves; Go's
    # path.Clean collapses them, and the API compares against path.Clean.
    if cleaned.startswith("//") and not cleaned.startswith("///"):
        cleaned = cleaned[1:]
    return cleaned


def media_type(header: str) -> str:
    """The media type of a Content-Type header, lowercased, parameters dropped."""
    return header.split(";", 1)[0].strip().lower()


def disposition_filename(header: str) -> str:
    """The filename a Content-Disposition header suggests, or "" if it has none."""
    if not header:
        return ""
    message = email.message.Message()
    message["Content-Disposition"] = header
    name = message.get_filename()
    return name if isinstance(name, str) else ""


def base_name(name: str) -> str:
    """Reduce an untrusted name to a single path component, or "" if nothing
    usable is left.

    Content-Disposition filenames come from the sandbox and nothing in the
    parsing strips separators, so a filename of "../../x" would otherwise escape
    the destination directory. ntpath treats both separators and a drive prefix
    as separators on every platform, which is the strictest reading available.
    """
    base = ntpath.basename(name)
    if base in ("", ".", ".."):
        return ""
    return base


def check_content_encoding(header: str) -> None:
    """Refuse a body that arrives under a coding httpx has not already undone.

    httpx sets its own Accept-Encoding, transparently decodes a gzip response,
    and leaves the header in place, so gzip here means the body is already
    plain. Content-Type: application/gzip is a payload type, not an encoding,
    and is deliberately not handled here.
    """
    codings = [token.strip().lower() for token in header.split(",")]
    codings = [coding for coding in codings if coding and coding != "identity"]
    if not codings:
        return
    # Multiple codings would have to be undone in reverse order; nothing sends
    # them, so refuse rather than guess.
    if len(codings) > 1 or codings[0] not in _DECODED_CODINGS:
        raise SandboxDownloadError(f"cannot decode Content-Encoding {header!r}")


def resolve_file_dest(local_path: str, filename: str, remote_path: str) -> str:
    """Where a single downloaded file lands.

    Writing into local_path when it is an existing directory mirrors cp and scp;
    the name comes from the sandbox, so it is reduced to one path component.
    """
    if not os.path.isdir(local_path):
        return local_path
    name = base_name(filename) or base_name(remote_path)
    if not name:
        raise SandboxDownloadError(
            f"cannot name the downloaded file under {local_path}: "
            "the sandbox suggested no usable filename"
        )
    return os.path.join(local_path, name)


def parent_dir(path: str) -> str:
    """The directory holding path, as somewhere to put a temp sibling."""
    return os.path.dirname(os.path.abspath(path))


def prepare_extract_dir(local_path: str) -> str:
    """Create the extraction destination and return where its spool file goes."""
    os.makedirs(local_path, 0o750, exist_ok=True)
    return parent_dir(local_path)


class PartialDownload:
    """A temp file holding a download in flight.

    Everything the sandbox sends lands here first: a single file is renamed over
    its destination once complete, and an archive is extracted from here. An
    interrupted transfer leaves only the temp file, never a truncated file
    looking complete at the destination. The name is unique, so an unrelated
    file that happens to share the prefix survives, as does a second download
    running against the same destination.
    """

    def __init__(self, directory: str):
        fd, self.path = tempfile.mkstemp(prefix=_PARTIAL_PREFIX, dir=directory)
        self._file: IO[bytes] | None = os.fdopen(fd, "wb")

    def __enter__(self) -> PartialDownload:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._close()
        # A no-op once commit has renamed the temp file away.
        with contextlib.suppress(OSError):
            os.remove(self.path)

    def write(self, chunk: bytes) -> None:
        if self._file is None:
            raise SandboxDownloadError("write to a finished download")
        self._file.write(chunk)

    def commit(self, dest: str) -> str:
        """Move the completed download to dest, replacing what is there."""
        # mkstemp opens 0o600. Widen to the 0o644 a plain create would produce
        # under a default umask, which is also what extraction writes with.
        os.chmod(self.path, 0o644)
        self._close()
        os.replace(self.path, dest)
        return dest

    def extract(self, dest: str) -> None:
        """Extract the completed download as a tar archive under dest."""
        self._close()
        with open(self.path, "rb") as archive:
            extract_tar(dest, archive)

    def _close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None


class _TerminatedReader:
    """Reports the underlying stream's EOF as a truncated archive.

    tarfile stops reading at the end-of-archive marker, so a complete archive
    never reaches the end of the stream and never trips this; a truncated one
    does. Nothing else catches that: tarfile reads a stream that simply stopped
    on a 512-byte boundary as a clean end of archive, and httpx's decompressor
    does not check the gzip trailer, so a cut-off transfer would otherwise
    extract part of a tree and report success.
    """

    def __init__(self, fileobj: IO[bytes]):
        self._fileobj = fileobj

    def read(self, size: int = -1) -> bytes:
        if size == 0:
            return b""
        chunk = self._fileobj.read(size)
        if not chunk:
            raise SandboxDownloadError(
                "sandbox archive ended without an end-of-archive marker"
            )
        return chunk


def extract_tar(dest: str, fileobj: IO[bytes]) -> None:
    """Extract a downloaded archive under dest.

    The archive comes from the (untrusted) sandbox, so every path is resolved
    against dest before anything is created: an entry naming its way out is
    refused, and so is one routed through a symlink that leaves dest. A symlink
    pointing outside dest still gets created, matching what tar does and what
    the trees people download contain, but nothing can be written through it.
    """
    os.makedirs(dest, 0o750, exist_ok=True)
    dest_real = os.path.realpath(dest)

    # Streaming mode even though the spool file is seekable: seeking would break
    # the sequential reads _TerminatedReader relies on. The cast is because a
    # stream-mode archive only ever calls read() on its fileobj.
    reader = cast("IO[bytes]", _TerminatedReader(fileobj))
    # A malformed header or a bad checksum raises TarError, which says nothing
    # about the sandbox to a caller catching RenderError.
    try:
        with tarfile.open(fileobj=reader, mode="r|") as archive:
            for member in archive:
                parts = _entry_parts(member.name)
                if not parts:
                    continue
                # Masking to 0o777 drops setuid/setgid, which an archive from
                # the sandbox has no business setting locally; the or'd owner
                # bits keep the tree writable enough to finish extracting into.
                if member.isdir():
                    _make_dirs(dest, dest_real, parts, member.mode & 0o777 | 0o700)
                elif member.isreg():
                    target = _make_parents(dest, dest_real, parts)
                    _write_file(target, member.mode & 0o777 | 0o600, archive, member)
                elif member.issym():
                    target = _make_parents(dest, dest_real, parts)
                    _clear_target(target, member.name)
                    os.symlink(member.linkname, target)
                elif member.islnk():
                    target = _make_parents(dest, dest_real, parts)
                    source = _link_source(dest, dest_real, member.linkname)
                    _clear_target(target, member.name)
                    os.link(source, target)
                # Devices, fifos, and other special entries are skipped.
    except tarfile.TarError as exc:
        raise SandboxDownloadError(f"sandbox archive is malformed: {exc}") from exc


def _entry_parts(name: str) -> list[str]:
    """Split a tar entry name into path components under the destination.

    Returns an empty list for the archive's own root entry, and raises for a
    name that points anywhere but under the destination.
    """
    clean = posixpath.normpath(name)
    if clean in (".", "/", ""):
        return []
    escapes = (
        posixpath.isabs(clean)
        or bool(ntpath.splitdrive(clean)[0])
        or clean == ".."
        or clean.startswith("../")
    )
    if escapes:
        raise SandboxDownloadError(f"archive entry {name!r} escapes the destination")
    return clean.split("/")


def _make_dirs(dest: str, dest_real: str, parts: list[str], mode: int) -> str:
    """Create each directory in parts under dest, checking as it descends.

    Creating the tree one component at a time is what keeps a symlink planted by
    an earlier entry from redirecting the rest of the extraction: a component
    that already exists as a link out of dest fails the check before anything is
    written through it.
    """
    current = dest
    for index, part in enumerate(parts):
        current = os.path.join(current, part)
        with contextlib.suppress(FileExistsError):
            os.mkdir(current, mode if index == len(parts) - 1 else 0o750)
        # Something that is not a directory sitting in the path is the archive
        # and the destination disagreeing about what a name is. Say so, rather
        # than letting the next write fail with a bare ENOTDIR.
        if not os.path.isdir(current):
            raise SandboxDownloadError(
                f"archive entry {'/'.join(parts)!r} needs a directory at "
                f"{current}, which is not one"
            )
        real = os.path.realpath(current)
        if real != dest_real and not real.startswith(dest_real + os.sep):
            raise SandboxDownloadError(
                f"archive entry {'/'.join(parts)!r} escapes the destination"
            )
    return current


def _make_parents(dest: str, dest_real: str, parts: list[str]) -> str:
    """Create the directories leading to the last component and return its path."""
    parent = _make_dirs(dest, dest_real, parts[:-1], 0o750)
    return os.path.join(parent, parts[-1])


def _write_file(
    target: str, mode: int, archive: tarfile.TarFile, member: tarfile.TarInfo
) -> None:
    source = archive.extractfile(member)
    if source is None:
        return
    # O_NOFOLLOW refuses a symlink sitting at target but opens a FIFO normally,
    # and opening one blocks until a writer appears, which may be never. Clear
    # anything that is not a regular file, as the symlink branch already does.
    existing = _lstat(target)
    if existing is not None and not stat.S_ISREG(existing.st_mode):
        _clear_target(target, member.name)
    flags = os.O_CREAT | os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW
    with os.fdopen(os.open(target, flags, mode), "wb") as out:
        while True:
            chunk = source.read(64 * 1024)
            if not chunk:
                break
            out.write(chunk)


def _link_source(dest: str, dest_real: str, linkname: str) -> str:
    """Resolve a hard link's target, which the archive names relative to itself."""
    parts = _entry_parts(linkname)
    if not parts:
        raise SandboxDownloadError(f"archive hard link to {linkname!r} is not a file")
    source = os.path.join(dest, *parts)
    real = os.path.realpath(source)
    if not real.startswith(dest_real + os.sep):
        raise SandboxDownloadError(
            f"archive hard link to {linkname!r} escapes the destination"
        )
    return source


def _lstat(path: str) -> os.stat_result | None:
    """lstat path, or None when nothing is there."""
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def _clear_target(target: str, name: str) -> None:
    """Remove whatever sits at target so an archive entry can take its place.

    A directory is refused rather than emptied: a download quietly deleting a
    local tree is a surprise nobody asks for. Every other failure surfaces,
    since swallowing it here only produces a stranger error at the next call.
    """
    existing = _lstat(target)
    if existing is None:
        return
    if stat.S_ISDIR(existing.st_mode):
        raise SandboxDownloadError(
            f"archive entry {name!r} would replace the directory at {target}"
        )
    os.remove(target)
