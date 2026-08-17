"""Streaming local file and archive access for sandbox uploads.

A directory travels to the sandbox as a gzipped tar that the server extracts,
so the archive has to be produced while the request body is written rather than
staged whole. tarfile drives its own writes, so the producer runs on a thread
and hands finished chunks to the consumer through a bounded queue: blocking on
that queue is the backpressure, and it is what keeps an arbitrarily large tree
from being buffered in memory.

Not part of the unasync pair set. The sync and async iterators here differ by
more than the mechanical transformation, so both are written out.
"""

from __future__ import annotations

import asyncio
import os
import tarfile
import threading
from collections.abc import AsyncGenerator, AsyncIterator, Generator, Iterator
from pathlib import Path
from queue import Full, Queue
from typing import IO, cast

# Bytes coalesced before a chunk is handed to the transport. tarfile writes in
# 10 KiB records, each of which would otherwise become its own HTTP chunk.
CHUNK_SIZE = 1024 * 1024

# Chunks the producer may run ahead of the consumer.
_QUEUE_DEPTH = 4

# How long a blocked producer waits before rechecking whether the consumer left.
_POLL_SECONDS = 0.1

# How long the consumer waits for the producer to wind down. The producer only
# ever blocks in _POLL_SECONDS slices, so reaching this means something is stuck
# in a read; the thread is a daemon, so it cannot hold up interpreter exit.
_JOIN_SECONDS = 30.0


class _Done:
    """End-of-archive marker passed through the queue."""


_DONE = _Done()


class _ConsumerGone(Exception):
    """Raised in the producer thread when the consumer abandons the archive."""


class _ChunkSink:
    """File-like sink that coalesces tarfile's writes and applies backpressure."""

    def __init__(self, chunks: Queue[bytes | _Done]) -> None:
        self._chunks = chunks
        self._buffer = bytearray()
        self._closed = threading.Event()

    @property
    def abandoned(self) -> bool:
        return self._closed.is_set()

    def write(self, data: bytes) -> int:
        self._buffer += data
        while len(self._buffer) >= CHUNK_SIZE:
            self._emit(bytes(self._buffer[:CHUNK_SIZE]))
            del self._buffer[:CHUNK_SIZE]
        return len(data)

    def flush(self) -> None:
        if self._buffer:
            self._emit(bytes(self._buffer))
            self._buffer.clear()

    def close(self) -> None:
        """Tell the producer the consumer is gone.

        Without this, a producer parked on a full queue after an abandoned
        upload would never wake and the thread would leak. This is the
        counterpart to closing the read end of a pipe.
        """
        self._closed.set()

    def _emit(self, chunk: bytes) -> None:
        while True:
            if self._closed.is_set():
                raise _ConsumerGone
            try:
                self._chunks.put(chunk, timeout=_POLL_SECONDS)
                return
            except Full:
                continue


def _walk(root: Path) -> Iterator[tuple[Path, str]]:
    """Yield (path, archive name) for everything under root, parents first.

    root itself is not emitted: the archive carries the directory's contents so
    that extraction lands them at the remote path rather than nested under
    another level of directory.
    """
    stack = [root]
    while stack:
        current = stack.pop()
        with os.scandir(current) as entries:
            for entry in sorted(entries, key=lambda e: e.name):
                path = Path(entry.path)
                yield path, path.relative_to(root).as_posix()
                if entry.is_dir(follow_symlinks=False):
                    stack.append(path)


def _entry(tar: tarfile.TarFile, path: Path, arcname: str) -> tarfile.TarInfo | None:
    """Build the archive entry for path, or None if it should be skipped."""
    entry = tar.gettarinfo(str(path), arcname=arcname)
    if entry.islnk():
        # gettarinfo tracks inodes and emits a hardlink entry for the second and
        # later names of a file. Go's tar.FileInfoHeader does not, so the CLI
        # stores each name as its own regular file; match that.
        entry.type = tarfile.REGTYPE
        entry.linkname = ""
        entry.size = path.lstat().st_size
    if not (entry.isreg() or entry.isdir() or entry.issym()):
        # Sockets, fifos and devices: skipped on the way in, as the sandbox
        # skips them on the way out.
        return None
    return entry


def _produce(
    root: Path,
    sink: _ChunkSink,
    chunks: Queue[bytes | _Done],
    failure: list[BaseException],
) -> None:
    try:
        # Stream mode only ever writes to the fileobj, which is all the sink
        # implements; it is not a seekable file and cannot claim to be one.
        with tarfile.open(fileobj=cast("IO[bytes]", sink), mode="w|gz") as tar:
            for path, arcname in _walk(root):
                entry = _entry(tar, path, arcname)
                if entry is None:
                    continue
                if entry.isreg():
                    with open(path, "rb") as handle:
                        tar.addfile(entry, handle)
                else:
                    tar.addfile(entry)
        sink.flush()
    except _ConsumerGone:
        return
    except BaseException as exc:  # noqa: BLE001 - re-raised on the consumer's thread
        failure.append(exc)
    finally:
        _signal_done(chunks, sink)


def _signal_done(chunks: Queue[bytes | _Done], sink: _ChunkSink) -> None:
    while not sink.abandoned:
        try:
            chunks.put(_DONE, timeout=_POLL_SECONDS)
            return
        except Full:
            continue


def iter_tar_gzip(root: str | os.PathLike[str]) -> Generator[bytes, None, None]:
    """Yield a gzipped tar of the tree at root, one chunk at a time.

    Entry names are relative to root, symlinks are stored rather than followed,
    and anything that is not a file, directory or symlink is skipped.
    """
    # The caller reached this path via stat(), which follows symlinks. Follow it
    # here too: walking the link itself would produce an empty archive.
    resolved = Path(os.path.realpath(root))
    chunks: Queue[bytes | _Done] = Queue(maxsize=_QUEUE_DEPTH)
    sink = _ChunkSink(chunks)
    failure: list[BaseException] = []
    producer = threading.Thread(
        target=_produce,
        args=(resolved, sink, chunks, failure),
        name="render-sdk-sandbox-tar",
        daemon=True,
    )
    producer.start()
    try:
        while True:
            item = chunks.get()
            if isinstance(item, _Done):
                break
            yield item
    finally:
        sink.close()
        producer.join(timeout=_JOIN_SECONDS)
    if failure:
        raise failure[0]


async def aiter_tar_gzip(root: str | os.PathLike[str]) -> AsyncIterator[bytes]:
    """Async view of iter_tar_gzip, so the event loop is free while tar works."""
    chunks = iter_tar_gzip(root)
    # A cancelled upload leaves a worker thread inside next() while this
    # coroutine unwinds into the finally below. Closing a generator that is
    # still executing raises ValueError, which would mask the CancelledError
    # and skip iter_tar_gzip's own cleanup, parking the producer forever. The
    # lock makes the close wait for the in-flight next() instead.
    lock = threading.Lock()

    def next_chunk() -> bytes | None:
        with lock:
            return next(chunks, None)

    def close_chunks() -> None:
        with lock:
            chunks.close()

    try:
        while True:
            chunk = await asyncio.to_thread(next_chunk)
            if chunk is None:
                break
            yield chunk
    finally:
        # Closing the generator raises GeneratorExit inside it, which is what
        # tells the producer thread to stop when the upload is abandoned.
        await asyncio.to_thread(close_chunks)


def iter_file(path: str | os.PathLike[str]) -> Iterator[bytes]:
    """Yield the contents of path, one chunk at a time."""
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                return
            yield chunk


async def aiter_file(path: str | os.PathLike[str]) -> AsyncIterator[bytes]:
    """Async view of iter_file."""
    # open() is offloaded like the reads: on a stalled network mount it blocks
    # for as long as the mount does, and on the loop thread that stalls every
    # other task, not just this upload.
    handle = await asyncio.to_thread(open, path, "rb")
    try:
        while True:
            chunk = await asyncio.to_thread(handle.read, CHUNK_SIZE)
            if not chunk:
                return
            yield chunk
    finally:
        # Not offloaded: awaiting here during a cancellation is the trap the
        # archive iterator already had to work around, and closing a file
        # opened for reading has nothing to flush.
        handle.close()


def stat_path(path: str | os.PathLike[str]) -> os.stat_result:
    """Stat path, following symlinks."""
    return os.stat(path)


async def astat_path(path: str | os.PathLike[str]) -> os.stat_result:
    """Async view of stat_path, for the same reason aiter_file offloads open."""
    return await asyncio.to_thread(os.stat, path)


def close_content(content: Iterator[bytes]) -> None:
    """Release a request body httpx did not finish consuming."""
    if isinstance(content, Generator):
        content.close()


async def aclose_content(content: AsyncIterator[bytes]) -> None:
    """Async view of close_content."""
    if isinstance(content, AsyncGenerator):
        await content.aclose()
