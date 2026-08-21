"""Tests for sandbox downloads: the copy_from path and its filesystem half."""

import gzip
import io
import os
import stat
import tarfile
import threading

import httpx
import pytest

from render.client.errors import ClientError, RenderError
from render.experimental.sandbox.client import SandboxClient
from render.experimental.sandbox.errors import (
    SandboxDownloadError,
    SandboxFileNotFoundError,
    SandboxNotFoundError,
)
from render.experimental.sandbox.files import (
    base_name,
    check_content_encoding,
    disposition_filename,
    extract_tar,
    media_type,
    normalize_remote_path,
    resolve_file_dest,
)
from render.public_api.client import AuthenticatedClient

CONNECT_JSON = {
    "token": "file-token-xyz",
    "uri": "https://proxy.test/files/download",
    "method": "GET",
    "expiresAt": "2026-07-21T00:05:00Z",
}


def _tar(entries, *, terminated=True):
    """Build a tar archive from (name, kind, payload, mode) tuples.

    payload is bytes for a regular file and a link target for a link. With
    terminated False the end-of-archive marker is cut off, which is what a
    transfer interrupted on a block boundary looks like.
    """
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as archive:
        for name, kind, payload, mode in entries:
            info = tarfile.TarInfo(name)
            info.type = kind
            info.mode = mode
            if kind == tarfile.REGTYPE:
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            else:
                info.linkname = payload if isinstance(payload, str) else ""
                archive.addfile(info)
    data = buf.getvalue()
    body = data.rstrip(b"\x00")
    padded = body + b"\x00" * (-len(body) % 512)
    # Python pads to 10240 bytes; the sandbox agent's Go writer emits the two
    # zero blocks and stops, so test against that shape.
    return padded + b"\x00" * 1024 if terminated else padded


def _file(name, content=b"", mode=0o644):
    return (name, tarfile.REGTYPE, content, mode)


def _dir(name, mode=0o755):
    return (name, tarfile.DIRTYPE, "", mode)


def _symlink(name, target):
    return (name, tarfile.SYMTYPE, target, 0o777)


def _extract(dest, data):
    extract_tar(str(dest), io.BytesIO(data))


# --- filesystem helpers -----------------------------------------------------


def test_extract_writes_the_tree(tmp_path):
    dest = tmp_path / "out"
    _extract(
        dest,
        _tar([_dir("sub"), _file("sub/a.txt", b"hello"), _file("b.txt", b"world")]),
    )

    assert (dest / "sub" / "a.txt").read_bytes() == b"hello"
    assert (dest / "b.txt").read_bytes() == b"world"


def test_extract_creates_missing_parent_dirs(tmp_path):
    dest = tmp_path / "out"
    _extract(dest, _tar([_file("deep/nested/a.txt", b"hi")]))

    assert (dest / "deep" / "nested" / "a.txt").read_bytes() == b"hi"


def test_extract_creates_symlinks(tmp_path):
    dest = tmp_path / "out"
    _extract(dest, _tar([_file("a.txt", b"hi"), _symlink("link", "a.txt")]))

    assert os.readlink(dest / "link") == "a.txt"
    assert (dest / "link").read_bytes() == b"hi"


def test_extract_drops_setuid(tmp_path):
    dest = tmp_path / "out"
    _extract(dest, _tar([_file("a.txt", b"hi", mode=0o4755)]))

    mode = (dest / "a.txt").stat().st_mode
    assert not mode & stat.S_ISUID
    assert mode & 0o600 == 0o600


def test_extract_refuses_an_entry_escaping_the_destination(tmp_path):
    dest = tmp_path / "out"
    with pytest.raises(SandboxDownloadError):
        _extract(dest, _tar([_file("../evil.txt", b"pwned")]))

    assert not (tmp_path / "evil.txt").exists()


def test_extract_refuses_an_absolute_entry(tmp_path):
    dest = tmp_path / "out"
    with pytest.raises(SandboxDownloadError):
        _extract(dest, _tar([_file("/etc/evil.txt", b"pwned")]))


def test_extract_refuses_a_write_through_an_escaping_symlink(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    dest = tmp_path / "out"

    with pytest.raises(SandboxDownloadError):
        _extract(
            dest,
            _tar(
                [_symlink("escape", str(outside)), _file("escape/evil.txt", b"pwned")]
            ),
        )

    assert list(outside.iterdir()) == []


def test_extract_replaces_a_symlink_at_the_leaf_rather_than_following_it(tmp_path):
    target = tmp_path / "outside.txt"
    target.write_bytes(b"original")
    dest = tmp_path / "out"

    _extract(
        dest,
        _tar([_symlink("evil.txt", str(target)), _file("evil.txt", b"pwned")]),
    )

    assert target.read_bytes() == b"original"
    written = dest / "evil.txt"
    assert not written.is_symlink()
    assert written.read_bytes() == b"pwned"


def test_extract_replaces_a_fifo_at_the_target(tmp_path):
    """Opening a FIFO blocks until a writer appears, which may be never, so
    extraction has to clear one instead of opening it."""
    dest = tmp_path / "out"
    dest.mkdir()
    os.mkfifo(dest / "a.txt")
    data = _tar([_file("a.txt", b"hi")])

    # In a thread so a regression fails the test instead of hanging the run.
    worker = threading.Thread(target=_extract, args=(dest, data), daemon=True)
    worker.start()
    worker.join(timeout=10)

    assert not worker.is_alive(), "extraction blocked on the FIFO"
    assert not stat.S_ISFIFO((dest / "a.txt").stat().st_mode)
    assert (dest / "a.txt").read_bytes() == b"hi"


def test_extract_links_hard_links_to_their_target(tmp_path):
    dest = tmp_path / "out"
    _extract(
        dest,
        _tar([_file("a.txt", b"hi"), ("b.txt", tarfile.LNKTYPE, "a.txt", 0o644)]),
    )

    assert (dest / "b.txt").read_bytes() == b"hi"
    assert (dest / "a.txt").stat().st_ino == (dest / "b.txt").stat().st_ino


def test_extract_refuses_a_hard_link_escaping_the_destination(tmp_path):
    dest = tmp_path / "out"
    with pytest.raises(SandboxDownloadError):
        _extract(dest, _tar([("b.txt", tarfile.LNKTYPE, "../outside.txt", 0o644)]))


def test_extract_skips_special_entries(tmp_path):
    dest = tmp_path / "out"
    _extract(dest, _tar([("fifo", tarfile.FIFOTYPE, "", 0o644), _file("a.txt", b"hi")]))

    assert not (dest / "fifo").exists()
    assert (dest / "a.txt").read_bytes() == b"hi"


def test_extract_reports_a_malformed_archive_as_a_download_error(tmp_path):
    """A bad header raises tarfile.TarError, which says nothing about the
    sandbox to a caller catching RenderError."""
    dest = tmp_path / "out"
    data = bytearray(_tar([_file("a.txt", b"hi")]))
    # Corrupt the mode field so the header checksum no longer matches.
    data[100:108] = b"garbage!"

    with pytest.raises(SandboxDownloadError, match="malformed"):
        _extract(dest, bytes(data))


def test_extract_refuses_to_replace_a_directory_with_a_file(tmp_path):
    dest = tmp_path / "out"
    (dest / "a.txt").mkdir(parents=True)
    (dest / "a.txt" / "keep.txt").write_bytes(b"mine")

    with pytest.raises(SandboxDownloadError, match="would replace the directory"):
        _extract(dest, _tar([_file("a.txt", b"pwned")]))

    assert (dest / "a.txt" / "keep.txt").read_bytes() == b"mine"


def test_extract_refuses_a_file_where_the_archive_needs_a_directory(tmp_path):
    dest = tmp_path / "out"
    dest.mkdir()
    (dest / "sub").write_bytes(b"i am a file")

    with pytest.raises(SandboxDownloadError, match="needs a directory"):
        _extract(dest, _tar([_file("sub/a.txt", b"hi")]))


def test_extract_refuses_a_truncated_archive(tmp_path):
    dest = tmp_path / "out"
    data = _tar([_file("a.txt", b"hi" * 500)], terminated=False)

    with pytest.raises(SandboxDownloadError, match="end-of-archive"):
        _extract(dest, data)


def test_extract_refuses_an_archive_cut_mid_entry(tmp_path):
    dest = tmp_path / "out"
    data = _tar([_file("a.txt", b"hi" * 500)])

    with pytest.raises(SandboxDownloadError, match="end-of-archive"):
        _extract(dest, data[:600])


def test_base_name_reduces_untrusted_names():
    assert base_name("../../etc/passwd") == "passwd"
    assert base_name("a/b.txt") == "b.txt"
    assert base_name("C:\\evil.txt") == "evil.txt"
    assert base_name("..") == ""
    assert base_name("/") == ""
    assert base_name("") == ""


def test_media_type_drops_parameters():
    assert media_type("application/X-Tar; charset=utf-8") == "application/x-tar"
    assert media_type("") == ""


def test_disposition_filename_reads_the_header():
    assert disposition_filename('attachment; filename="a b.txt"') == "a b.txt"
    assert disposition_filename("attachment") == ""
    assert disposition_filename("") == ""


def test_check_content_encoding_accepts_what_httpx_decodes():
    for header in ("", "identity", "gzip", "x-gzip", " GZIP "):
        check_content_encoding(header)


def test_check_content_encoding_refuses_anything_else():
    for header in ("br", "zstd", "gzip, gzip"):
        with pytest.raises(SandboxDownloadError):
            check_content_encoding(header)


def test_normalize_remote_path_matches_go_path_clean():
    assert normalize_remote_path("/app/data") == "/app/data"
    assert normalize_remote_path("/app/data/") == "/app/data"
    assert normalize_remote_path("workspace/") == "workspace"
    assert normalize_remote_path("/app/./data/../data.txt") == "/app/data.txt"
    assert normalize_remote_path("/app//x") == "/app/x"
    assert normalize_remote_path("//app/x") == "/app/x"
    assert normalize_remote_path("///app/x") == "/app/x"


def test_normalize_remote_path_rejects_an_empty_path():
    """Cleaning "" gives ".", which would quietly transfer the home directory;
    copy_to rejects it the same way."""
    with pytest.raises(ValueError, match="remote_path is required"):
        normalize_remote_path("")


def test_resolve_file_dest_picks_a_name_inside_a_directory(tmp_path):
    dest = resolve_file_dest(str(tmp_path), "a.txt", "/remote/b.txt")
    assert dest == str(tmp_path / "a.txt")


def test_resolve_file_dest_sanitizes_the_suggested_name(tmp_path):
    dest = resolve_file_dest(str(tmp_path), "../../evil.txt", "/remote/b.txt")
    assert dest == str(tmp_path / "evil.txt")


def test_resolve_file_dest_falls_back_to_the_remote_name(tmp_path):
    dest = resolve_file_dest(str(tmp_path), "", "/remote/b.txt")
    assert dest == str(tmp_path / "b.txt")


def test_resolve_file_dest_keeps_a_non_directory_path(tmp_path):
    target = tmp_path / "chosen.txt"
    assert resolve_file_dest(str(target), "a.txt", "/remote/b.txt") == str(target)


def test_resolve_file_dest_raises_without_a_usable_name(tmp_path):
    with pytest.raises(SandboxDownloadError):
        resolve_file_dest(str(tmp_path), "", "/")


# --- copy_from --------------------------------------------------------------


def _sandbox_client(handler, *, default_owner_id="tea-test"):
    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return SandboxClient(internal, default_owner_id=default_owner_id)


async def _noop_handler(request: httpx.Request) -> httpx.Response:
    raise AssertionError("the API client should not be called in this test")


def _patch_proxy(mocker, handler):
    """Patch the fresh httpx.AsyncClient the download uses for the proxy stream."""
    mocker.patch(
        "render.experimental.sandbox.api.httpx.AsyncClient",
        return_value=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def _download_client(mocker, content, headers):
    """A client whose token mint is stubbed and whose proxy serves content."""
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["auth"] = request.headers.get("authorization")
        captured["accept_encoding"] = request.headers.get("accept-encoding")
        return httpx.Response(200, content=content, headers=headers)

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_file_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, handler)
    return client, captured


@pytest.mark.asyncio
async def test_mint_file_token_requests_the_token_endpoint():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(201, json=CONNECT_JSON)

    client = _sandbox_client(handler)
    connection = await client.api._mint_file_token(
        "sbx-123", "tea-test", "download", "/app/data.txt"
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-123/files/download/token"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["query"]["path"] == "/app/data.txt"
    assert connection["uri"] == "https://proxy.test/files/download"


@pytest.mark.asyncio
async def test_copy_from_writes_a_single_file(tmp_path, mocker):
    client, captured = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )
    dest = tmp_path / "local.txt"

    written = await client.copy_from("sbx-123", "/app/data.txt", dest)

    assert captured["method"] == "GET"
    assert captured["auth"] == "Bearer file-token-xyz"
    assert written == str(dest)
    assert dest.read_bytes() == b"payload"
    assert dest.stat().st_mode & 0o600 == 0o600
    assert [p.name for p in tmp_path.iterdir()] == ["local.txt"]


@pytest.mark.asyncio
async def test_copy_from_asks_only_for_a_coding_httpx_undoes(tmp_path, mocker):
    """httpx would otherwise advertise deflate too, and a deflate body would
    reach the encoding check instead of being written."""
    client, captured = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )

    await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "x")

    assert captured["accept_encoding"] == "gzip"


@pytest.mark.asyncio
async def test_copy_from_cleans_the_remote_path_before_minting(tmp_path, mocker):
    client, _ = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )

    await client.copy_from("sbx-123", "/app/./data/../data.txt", tmp_path / "x")

    assert client.api._mint_file_token.await_args.args[3] == "/app/data.txt"


@pytest.mark.asyncio
async def test_copy_from_accepts_a_path_object(tmp_path, mocker):
    client, _ = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )

    written = await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "out.txt")

    assert written == str(tmp_path / "out.txt")


@pytest.mark.asyncio
async def test_copy_from_into_a_directory_uses_the_suggested_name(tmp_path, mocker):
    client, _ = _download_client(
        mocker,
        b"payload",
        {
            "content-type": "application/octet-stream",
            "content-disposition": 'attachment; filename="data.txt"',
        },
    )

    written = await client.copy_from("sbx-123", "/app/data.txt", tmp_path)

    assert written == str(tmp_path / "data.txt")
    assert (tmp_path / "data.txt").read_bytes() == b"payload"


@pytest.mark.asyncio
async def test_copy_from_sanitizes_the_suggested_name(tmp_path, mocker):
    client, _ = _download_client(
        mocker,
        b"payload",
        {
            "content-type": "application/octet-stream",
            "content-disposition": 'attachment; filename="../../evil.txt"',
        },
    )
    dest = tmp_path / "into"
    dest.mkdir()

    written = await client.copy_from("sbx-123", "/app/data.txt", dest)

    assert written == str(dest / "evil.txt")
    assert not (tmp_path / "evil.txt").exists()


@pytest.mark.asyncio
async def test_copy_from_falls_back_to_the_remote_name(tmp_path, mocker):
    client, _ = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )

    written = await client.copy_from("sbx-123", "/app/data.txt", tmp_path)

    assert written == str(tmp_path / "data.txt")


@pytest.mark.asyncio
async def test_copy_from_saves_legacy_gzip_as_a_file(tmp_path, mocker):
    """A pre-#34092 agent sends application/gzip; it is a payload type, so the
    body is written as-is rather than extracted."""
    archive = gzip.compress(_tar([_file("a.txt", b"hi")]))
    client, _ = _download_client(mocker, archive, {"content-type": "application/gzip"})
    dest = tmp_path / "dir.tar.gz"

    written = await client.copy_from("sbx-123", "/app/dir", dest)

    assert written == str(dest)
    assert dest.read_bytes() == archive


@pytest.mark.asyncio
async def test_copy_from_extracts_a_gzip_encoded_tar(tmp_path, mocker):
    """The agent sends x-tar under Content-Encoding: gzip, which httpx has
    already decoded by the time the body reaches us."""
    archive = _tar([_dir("sub"), _file("sub/a.txt", b"hello")])
    client, _ = _download_client(
        mocker,
        gzip.compress(archive),
        {"content-type": "application/x-tar", "content-encoding": "gzip"},
    )
    dest = tmp_path / "tree"

    written = await client.copy_from("sbx-123", "/app/dir", dest)

    assert written == str(dest)
    assert (dest / "sub" / "a.txt").read_bytes() == b"hello"


@pytest.mark.asyncio
async def test_copy_from_extracts_an_identity_tar(tmp_path, mocker):
    client, _ = _download_client(
        mocker,
        _tar([_file("a.txt", b"hello")]),
        {"content-type": "application/x-tar; charset=binary"},
    )
    dest = tmp_path / "tree"

    await client.copy_from("sbx-123", "/app/dir", dest)

    assert (dest / "a.txt").read_bytes() == b"hello"


@pytest.mark.asyncio
async def test_copy_from_leaves_no_spool_file_behind(tmp_path, mocker):
    client, _ = _download_client(
        mocker,
        _tar([_file("a.txt", b"hi" * 500)], terminated=False),
        {"content-type": "application/x-tar"},
    )
    dest = tmp_path / "tree"

    with pytest.raises(SandboxDownloadError):
        await client.copy_from("sbx-123", "/app/dir", dest)

    assert [p.name for p in tmp_path.iterdir()] == ["tree"]


@pytest.mark.asyncio
async def test_copy_from_refuses_an_encoding_it_cannot_undo(tmp_path, mocker):
    client, _ = _download_client(
        mocker,
        b"payload",
        {"content-type": "application/octet-stream", "content-encoding": "br"},
    )
    dest = tmp_path / "local.txt"

    with pytest.raises(SandboxDownloadError):
        await client.copy_from("sbx-123", "/app/data.txt", dest)

    assert not dest.exists()


def _proxy_error_client(mocker, status, **response_kwargs):
    """A client whose token mint succeeds and whose proxy returns an error."""

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, **response_kwargs)

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_file_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)
    return client


@pytest.mark.asyncio
async def test_copy_from_missing_remote_path_raises_file_not_found(tmp_path, mocker):
    """The agent 404s a bad remote_path with this code while the sandbox is
    alive, so it must not look like a terminated sandbox."""
    client = _proxy_error_client(
        mocker,
        404,
        json={"code": "file_not_found", "message": "no file or directory at path"},
    )

    with pytest.raises(SandboxFileNotFoundError) as excinfo:
        await client.copy_from("sbx-123", "/no/such/file", tmp_path / "x")

    assert not isinstance(excinfo.value, SandboxNotFoundError)
    assert "no file or directory at path" in str(excinfo.value)


@pytest.mark.asyncio
async def test_copy_from_proxy_404_without_the_code_raises_not_found(tmp_path, mocker):
    client = _proxy_error_client(mocker, 404, json={"message": "sandbox is gone"})

    with pytest.raises(SandboxNotFoundError):
        await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "x")


@pytest.mark.asyncio
async def test_copy_from_proxy_404_with_a_non_json_body_raises_not_found(
    tmp_path, mocker
):
    client = _proxy_error_client(mocker, 404, text="404 page not found")

    with pytest.raises(SandboxNotFoundError):
        await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "x")


@pytest.mark.asyncio
async def test_copy_from_reports_a_local_write_failure_as_a_download_error(
    tmp_path, mocker
):
    """A bare OSError from the spool, the extract or the rename says nothing
    about which download failed."""
    client, _ = _download_client(
        mocker, b"payload", {"content-type": "application/octet-stream"}
    )
    missing_parent = tmp_path / "no" / "such" / "dir" / "out.txt"

    with pytest.raises(SandboxDownloadError, match="could not write the download"):
        await client.copy_from("sbx-123", "/app/data.txt", missing_parent)


@pytest.mark.asyncio
async def test_copy_from_bounds_the_wait_for_the_next_chunk(tmp_path, mocker):
    """read=None would let a body that stops arriving hang forever."""
    captured = {}

    # Bound before the patch below, so building the stub does not re-enter it.
    real_async_client = httpx.AsyncClient

    def fake_client(*args, **kwargs):
        captured["timeout"] = kwargs["timeout"]
        return real_async_client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    content=b"payload",
                    headers={"content-type": "application/octet-stream"},
                )
            )
        )

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_file_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    mocker.patch("render.experimental.sandbox.api.httpx.AsyncClient", new=fake_client)

    await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "out.txt")

    assert captured["timeout"].read == 45.0
    assert captured["timeout"].connect == 5.0


@pytest.mark.asyncio
async def test_copy_from_mint_404_raises_not_found(tmp_path):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await client.copy_from("sbx-missing", "/app/data.txt", tmp_path / "x")


@pytest.mark.asyncio
async def test_copy_from_proxy_error_raises_client_error(tmp_path, mocker):
    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, text="no such file")

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_file_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(ClientError, match="no such file"):
        await client.copy_from("sbx-123", "/app/missing", tmp_path / "x")


@pytest.mark.asyncio
async def test_copy_from_requires_owner_id(tmp_path):
    client = _sandbox_client(_noop_handler, default_owner_id=None)
    with pytest.raises(RenderError):
        await client.copy_from("sbx-123", "/app/data.txt", tmp_path / "x")


def test_sync_copy_from_writes_a_single_file(tmp_path, mocker):
    from render.experimental.sandbox.client_sync import SyncSandboxClient

    def api_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json=CONNECT_JSON)

    def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"payload",
            headers={"content-type": "application/octet-stream"},
        )

    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(api_handler)},
    )
    # Build the API client before patching: httpx.Client is one attribute on one
    # module, so the patch below would otherwise catch this construction too.
    internal.get_httpx_client()
    mocker.patch(
        "render.experimental.sandbox.api_sync.httpx.Client",
        return_value=httpx.Client(transport=httpx.MockTransport(proxy_handler)),
    )
    client = SyncSandboxClient(internal, default_owner_id="tea-test")
    dest = tmp_path / "local.txt"

    written = client.copy_from("sbx-123", "/app/data.txt", dest)

    assert written == str(dest)
    assert dest.read_bytes() == b"payload"
