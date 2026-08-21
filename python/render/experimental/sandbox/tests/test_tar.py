import asyncio
import gzip
import io
import os
import tarfile
import threading
from pathlib import Path

import pytest

from render.experimental.sandbox._tar import (
    CHUNK_SIZE,
    aiter_tar_gzip,
    iter_tar_gzip,
)


def _members(chunks: list[bytes]) -> dict[str, tarfile.TarInfo]:
    raw = gzip.decompress(b"".join(chunks))
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        return {member.name: member for member in tar.getmembers()}


def _tree(root: Path) -> Path:
    (root / "a.txt").write_text("a\n")
    (root / "sub").mkdir()
    (root / "sub" / "b.txt").write_text("b\n")
    return root


def test_entries_are_relative_and_the_root_is_not_emitted(tmp_path):
    members = _members(list(iter_tar_gzip(_tree(tmp_path))))

    assert set(members) == {"a.txt", "sub", "sub/b.txt"}
    assert members["sub"].isdir()
    assert members["a.txt"].isreg()
    assert str(tmp_path) not in " ".join(members)


def test_symlinks_are_stored_not_followed(tmp_path):
    _tree(tmp_path)
    (tmp_path / "link.txt").symlink_to("sub/b.txt")

    members = _members(list(iter_tar_gzip(tmp_path)))

    assert members["link.txt"].issym()
    assert members["link.txt"].linkname == "sub/b.txt"
    assert members["link.txt"].size == 0


def test_special_files_are_skipped(tmp_path):
    _tree(tmp_path)
    os.mkfifo(tmp_path / "pipe")

    members = _members(list(iter_tar_gzip(tmp_path)))

    assert "pipe" not in members
    assert "a.txt" in members


def test_hardlinks_are_stored_as_regular_files(tmp_path):
    (tmp_path / "one.txt").write_text("shared\n")
    os.link(tmp_path / "one.txt", tmp_path / "two.txt")

    raw = gzip.decompress(b"".join(iter_tar_gzip(tmp_path)))
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        members = {member.name: member for member in tar.getmembers()}
        # Both names carry their own content, as the CLI's archive does: an
        # extractor never has to resolve one entry against another.
        assert members["one.txt"].isreg()
        assert members["two.txt"].isreg()
        assert tar.extractfile("two.txt").read() == b"shared\n"


def test_a_symlinked_root_is_followed(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    _tree(real)
    link = tmp_path / "link"
    link.symlink_to(real)

    members = _members(list(iter_tar_gzip(link)))

    assert set(members) == {"a.txt", "sub", "sub/b.txt"}


def test_producer_failure_reaches_the_consumer(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(iter_tar_gzip(tmp_path / "missing"))


def test_multi_chunk_archive_round_trips(tmp_path):
    # Incompressible data well past CHUNK_SIZE, so the sink actually splits the
    # archive and the chunk boundaries have to land in the right places. Every
    # other test here fits in a single chunk and never exercises that.
    payloads = {f"blob{i}.bin": os.urandom(900_000) for i in range(4)}
    for name, data in payloads.items():
        (tmp_path / name).write_bytes(data)

    chunks = list(iter_tar_gzip(tmp_path))

    assert len(chunks) > 1
    assert all(len(chunk) == CHUNK_SIZE for chunk in chunks[:-1])
    raw = gzip.decompress(b"".join(chunks))
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        extracted = {}
        for member in tar.getmembers():
            handle = tar.extractfile(member)
            assert handle is not None
            extracted[member.name] = handle.read()
    assert extracted == payloads


def test_abandoning_the_archive_stops_the_producer(tmp_path):
    # Incompressible data larger than the queue holds, so the producer is
    # parked on a full queue at the moment the consumer walks away.
    (tmp_path / "big.bin").write_bytes(os.urandom(6 * 1024 * 1024))

    chunks = iter_tar_gzip(tmp_path)
    next(chunks)
    chunks.close()

    assert not [t for t in threading.enumerate() if t.name == "render-sdk-sandbox-tar"]


@pytest.mark.asyncio
async def test_cancelling_mid_archive_stops_the_producer(tmp_path):
    # Big enough that the producer is still working when the cancellation
    # lands, so the close races an in-flight next().
    (tmp_path / "big.bin").write_bytes(os.urandom(6 * 1024 * 1024))

    chunks = aiter_tar_gzip(tmp_path)
    await chunks.__anext__()
    pending = asyncio.ensure_future(chunks.__anext__())
    await asyncio.sleep(0.01)
    pending.cancel()
    with pytest.raises(asyncio.CancelledError):
        await pending

    # Must not raise ValueError("generator already executing"), which would
    # mask the cancellation and leave the producer parked.
    await chunks.aclose()

    assert not [t for t in threading.enumerate() if t.name == "render-sdk-sandbox-tar"]


@pytest.mark.asyncio
async def test_async_archive_matches_the_sync_one(tmp_path):
    _tree(tmp_path)

    collected = [chunk async for chunk in aiter_tar_gzip(tmp_path)]

    assert set(_members(collected)) == {"a.txt", "sub", "sub/b.txt"}
