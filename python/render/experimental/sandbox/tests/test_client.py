import gzip
import io
import json
import os
import tarfile
from typing import cast

import httpx
import pytest

from render.client.errors import ClientError, RenderError
from render.experimental.sandbox.client import SandboxClient
from render.experimental.sandbox.errors import (
    SandboxExecError,
    SandboxExecStreamError,
    SandboxNotFoundError,
)
from render.experimental.sandbox.types import SandboxExecExit, SandboxExecOutput
from render.public_api.client import AuthenticatedClient

SANDBOX_JSON = {
    "id": "sbx-abc",
    "status": "running",
    "plan": "standard",
    "networkPolicy": {"default": "deny-all"},
    "region": "oregon",
    "timeoutSeconds": 300,
    "createdAt": "2026-07-17T00:00:00Z",
    "terminatedAt": None,
}

SANDBOX_GROUP_JSON = {
    "id": "sbg-abc",
    "ownerId": "tea-test",
    "name": "Default",
    "region": "oregon",
    "isDefault": True,
    "concurrencyLimit": 10,
    "environmentId": None,
    "createdAt": "2026-07-02T18:30:00Z",
    "updatedAt": "2026-07-02T18:30:00Z",
}


def _sandbox_client(handler, *, default_owner_id="tea-test"):
    transport = httpx.MockTransport(handler)
    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": transport},
    )
    return SandboxClient(internal, default_owner_id=default_owner_id)


@pytest.mark.asyncio
async def test_create_sends_sandbox_post_and_returns_sandbox():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create(plan="standard", timeout_seconds=300)

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes"
    assert captured["body"]["ownerId"] == "tea-test"
    assert captured["body"]["plan"] == "standard"
    assert captured["body"]["timeoutSeconds"] == 300
    assert "env" not in captured["body"]
    assert sandbox.id == "sbx-abc"
    assert sandbox.status == "running"
    assert sandbox.network_policy == "deny-all"
    assert sandbox.terminated_at is None


@pytest.mark.asyncio
async def test_create_sends_env_in_post_body():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    await client.create(env={"FOO": "bar", "BAZ": "qux"})

    assert captured["body"]["env"] == {"FOO": "bar", "BAZ": "qux"}


@pytest.mark.asyncio
async def test_create_requires_owner_id():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("handler should not be reached")

    client = _sandbox_client(handler, default_owner_id=None)
    with pytest.raises(RenderError):
        await client.create()


@pytest.mark.asyncio
async def test_from_id_returns_sandbox():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.from_id("sbx-abc")

    assert captured["path"] == "/v1/sandboxes/sbx-abc"
    assert captured["query"]["ownerId"] == "tea-test"
    assert sandbox.id == "sbx-abc"


@pytest.mark.asyncio
async def test_from_id_raises_not_found_on_404():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await client.from_id("sbx-missing")


@pytest.mark.asyncio
async def test_list_returns_sandboxes_and_cursor():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        captured["status_values"] = request.url.params.get_list("status")
        body = [
            {"sandbox": SANDBOX_JSON, "cursor": "cur-1"},
            {"sandbox": {**SANDBOX_JSON, "id": "sbx-def"}, "cursor": "cur-2"},
        ]
        return httpx.Response(200, json=body)

    client = _sandbox_client(handler)
    page = await client.list(status="running", limit=50)

    assert captured["path"] == "/v1/sandboxes"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["status_values"] == ["running"]
    assert captured["query"]["limit"] == "50"
    assert [s.id for s in page.sandboxes] == ["sbx-abc", "sbx-def"]
    assert page.next_cursor == "cur-2"


@pytest.mark.asyncio
async def test_list_empty_has_no_cursor():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    page = await client.list()
    assert page.sandboxes == []
    assert page.next_cursor is None


@pytest.mark.asyncio
async def test_list_sends_one_status_query_param_per_value():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    await client.list(status=["running", "creating"])

    assert captured["status"] == ["running", "creating"]


@pytest.mark.asyncio
async def test_list_sends_a_single_status_string_as_one_value():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    await client.list(status="running")

    assert captured["status"] == ["running"]


@pytest.mark.asyncio
async def test_list_omits_status_when_no_filter_is_given():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)

    await client.list()
    assert "status" not in captured["query"]

    await client.list(status=[])
    assert "status" not in captured["query"]


@pytest.mark.asyncio
async def test_list_rejects_an_unknown_status():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("handler should not be reached")

    client = _sandbox_client(handler)

    with pytest.raises(ValueError, match="bogus"):
        await client.list(status=["running", "bogus"])

    with pytest.raises(ValueError, match="bogus"):
        await client.list(status="bogus")


@pytest.mark.asyncio
async def test_list_groups_returns_groups_and_cursor():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["owner_id"] = request.url.params.get_list("ownerId")
        body = [{"sandboxGroup": SANDBOX_GROUP_JSON, "cursor": "cur-1"}]
        return httpx.Response(200, json=body)

    client = _sandbox_client(handler)
    page = await client.list_groups()

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups"
    assert captured["owner_id"] == ["tea-test"]

    group = page.groups[0]
    assert group.id == "sbg-abc"
    assert group.owner_id == "tea-test"
    assert group.name == "Default"
    assert group.region == "oregon"
    assert group.is_default is True
    assert group.concurrency_limit == 10
    assert group.environment_id is None
    assert group.created_at.isoformat() == "2026-07-02T18:30:00+00:00"
    assert group.updated_at.isoformat() == "2026-07-02T18:30:00+00:00"
    assert page.next_cursor == "cur-1"


@pytest.mark.asyncio
async def test_list_groups_uses_an_explicit_owner_id():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["owner_id"] = request.url.params.get_list("ownerId")
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    await client.list_groups(owner_id="tea-other")

    assert captured["owner_id"] == ["tea-other"]


@pytest.mark.asyncio
async def test_list_groups_empty_has_no_cursor():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    page = await client.list_groups()

    assert page.groups == []
    assert page.next_cursor is None


@pytest.mark.asyncio
async def test_list_groups_requires_owner_id():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("handler should not be reached")

    client = _sandbox_client(handler, default_owner_id=None)
    with pytest.raises(RenderError):
        await client.list_groups()


@pytest.mark.asyncio
async def test_list_groups_raises_client_error_on_404():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "workspace not found"})

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match="workspace not found"):
        await client.list_groups()


@pytest.mark.asyncio
async def test_list_groups_reads_a_set_environment_id():
    async def handler(request: httpx.Request) -> httpx.Response:
        group = {**SANDBOX_GROUP_JSON, "environmentId": "evm-1"}
        return httpx.Response(200, json=[{"sandboxGroup": group, "cursor": "cur-1"}])

    client = _sandbox_client(handler)
    page = await client.list_groups()

    assert page.groups[0].environment_id == "evm-1"


@pytest.mark.asyncio
async def test_list_groups_treats_an_omitted_environment_id_as_none():
    async def handler(request: httpx.Request) -> httpx.Response:
        group = {k: v for k, v in SANDBOX_GROUP_JSON.items() if k != "environmentId"}
        return httpx.Response(200, json=[{"sandboxGroup": group, "cursor": "cur-1"}])

    client = _sandbox_client(handler)
    page = await client.list_groups()

    assert page.groups[0].environment_id is None


def _sync_sandbox_client(handler, *, default_owner_id="tea-test"):
    from render.experimental.sandbox.client_sync import SyncSandboxClient

    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return SyncSandboxClient(internal, default_owner_id=default_owner_id)


def test_sync_list_sends_one_status_query_param_per_value():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(200, json=[{"sandbox": SANDBOX_JSON, "cursor": "cur-1"}])

    client = _sync_sandbox_client(handler)
    page = client.list(status=["running", "suspended"])

    assert captured["status"] == ["running", "suspended"]
    assert [s.id for s in page.sandboxes] == ["sbx-abc"]
    assert page.next_cursor == "cur-1"


def test_sync_list_sends_a_single_status_string_as_one_value():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(200, json=[])

    client = _sync_sandbox_client(handler)
    client.list(status="running")

    assert captured["status"] == ["running"]


def test_sync_list_omits_status_when_no_filter_is_given():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    client = _sync_sandbox_client(handler)

    client.list()
    assert "status" not in captured["query"]

    client.list(status=[])
    assert "status" not in captured["query"]


def test_sync_list_rejects_an_unknown_status():
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("handler should not be reached")

    client = _sync_sandbox_client(handler)

    with pytest.raises(ValueError, match="bogus"):
        client.list(status=["running", "bogus"])

    with pytest.raises(ValueError, match="bogus"):
        client.list(status="bogus")


def test_sync_list_groups_returns_groups_and_cursor():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["owner_id"] = request.url.params.get_list("ownerId")
        body = [{"sandboxGroup": SANDBOX_GROUP_JSON, "cursor": "cur-1"}]
        return httpx.Response(200, json=body)

    client = _sync_sandbox_client(handler)
    page = client.list_groups()

    assert captured["path"] == "/v1/sandbox-groups"
    assert captured["owner_id"] == ["tea-test"]
    assert [g.id for g in page.groups] == ["sbg-abc"]
    assert page.next_cursor == "cur-1"


def test_sync_list_groups_empty_has_no_cursor():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    client = _sync_sandbox_client(handler)
    page = client.list_groups()

    assert page.groups == []
    assert page.next_cursor is None


def test_sync_list_groups_requires_owner_id():
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("handler should not be reached")

    client = _sync_sandbox_client(handler, default_owner_id=None)
    with pytest.raises(RenderError):
        client.list_groups()


@pytest.mark.asyncio
async def test_terminate_posts_to_terminate_and_returns_none():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(204)

    client = _sandbox_client(handler)
    result = await client.terminate("sbx-abc")

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-abc/terminate"
    assert captured["query"]["ownerId"] == "tea-test"
    assert result is None


@pytest.mark.asyncio
async def test_terminate_raises_not_found_on_404():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await client.terminate("sbx-missing")


CONNECT_JSON = {
    "executionId": "exc-1",
    "token": "run-token-xyz",
    "uri": "https://proxy.test/runs/stream",
    "method": "POST",
    "expiresAt": "2026-07-21T00:05:00Z",
}


async def _collect(agen):
    return [event async for event in agen]


async def _noop_handler(request: httpx.Request) -> httpx.Response:
    raise AssertionError("the API client should not be called in this test")


def _patch_proxy(mocker, handler):
    """Patch the fresh httpx.AsyncClient that exec uses for the proxy stream."""
    mocker.patch(
        "render.experimental.sandbox.api.httpx.AsyncClient",
        return_value=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


@pytest.mark.asyncio
async def test_mint_run_token_requests_the_token_endpoint():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=CONNECT_JSON)

    client = _sandbox_client(handler)
    connection = await client.api._mint_run_token(
        "sbx-123", "tea-test", "stream", "ls -la"
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-123/runs/stream/token"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["body"] == {"command": "ls -la"}
    assert connection["token"] == "run-token-xyz"  # noqa: S105
    assert connection["uri"] == "https://proxy.test/runs/stream"


@pytest.mark.asyncio
async def test_exec_streams_from_the_proxy_uri(mocker):
    proxy = {}
    sse = (
        b'event: output\ndata: {"stream":"stdout","data":"hi\\n"}\n\n'
        b'event: output\ndata: {"stream":"stderr","data":"warn\\n"}\n\n'
        b'event: exit\ndata: {"exit_code":7}\n\n'
    )

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        proxy["method"] = request.method
        proxy["url"] = str(request.url)
        proxy["auth"] = request.headers.get("authorization")
        proxy["accept"] = request.headers.get("accept")
        proxy["body"] = json.loads(request.content)
        return httpx.Response(
            200, content=sse, headers={"content-type": "text/event-stream"}
        )

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_run_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)

    events = await _collect(client.exec("sbx-123", "echo hi"))

    assert proxy["method"] == "POST"
    assert proxy["url"] == "https://proxy.test/runs/stream"
    assert proxy["auth"] == "Bearer run-token-xyz"
    assert proxy["accept"] == "text/event-stream"
    assert proxy["body"] == {"command": "echo hi"}
    assert events == [
        SandboxExecOutput(stream="stdout", data="hi\n"),
        SandboxExecOutput(stream="stderr", data="warn\n"),
        SandboxExecExit(exit_code=7),
    ]


@pytest.mark.asyncio
async def test_exec_error_event_raises_stream_error(mocker):
    sse = b'event: error\ndata: {"status":408,"message":"exec timed out"}\n\n'

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, content=sse, headers={"content-type": "text/event-stream"}
        )

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_run_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(SandboxExecStreamError) as excinfo:
        await _collect(client.exec("sbx-123", "boom"))
    assert excinfo.value.status == 408
    assert excinfo.value.message == "exec timed out"


@pytest.mark.asyncio
async def test_exec_missing_terminal_event_raises(mocker):
    sse = b'event: output\ndata: {"stream":"stdout","data":"hi\\n"}\n\n'

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, content=sse, headers={"content-type": "text/event-stream"}
        )

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_run_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(SandboxExecError):
        await _collect(client.exec("sbx-123", "hi"))


@pytest.mark.asyncio
async def test_exec_proxy_non_2xx_raises_client_error(mocker):
    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, text="sandbox not ready")

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api, "_mint_run_token", new=mocker.AsyncMock(return_value=CONNECT_JSON)
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(ClientError):
        await _collect(client.exec("sbx-123", "hi"))


@pytest.mark.asyncio
async def test_exec_mint_404_raises_not_found():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await _collect(client.exec("sbx-missing", "hi"))


@pytest.mark.asyncio
async def test_exec_requires_owner_id():
    client = _sandbox_client(_noop_handler, default_owner_id=None)
    with pytest.raises(RenderError):
        await _collect(client.exec("sbx-123", "hi"))


def test_experimental_service_exposes_sandboxes(monkeypatch):
    monkeypatch.setenv("RENDER_API_KEY", "test-token")
    monkeypatch.setenv("RENDER_WORKSPACE_ID", "tea-default")
    monkeypatch.setenv("RENDER_REGION", "oregon")

    from render.client.client import Client

    client = Client()
    sandboxes = client.experimental.sandboxes
    assert isinstance(sandboxes, SandboxClient)
    assert sandboxes._default_owner_id == "tea-default"
    assert sandboxes._default_region == "oregon"


def test_sync_experimental_service_exposes_sandboxes(monkeypatch):
    monkeypatch.setenv("RENDER_API_KEY", "test-token")
    monkeypatch.setenv("RENDER_WORKSPACE_ID", "tea-default")

    from render import Render
    from render.experimental.sandbox.client_sync import SyncSandboxClient

    render = Render()
    sandboxes = render.experimental.sandboxes
    assert isinstance(sandboxes, SyncSandboxClient)
    assert sandboxes._default_owner_id == "tea-default"


@pytest.mark.asyncio
async def test_from_id_wraps_non_json_error_response():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="upstream boom")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError):
        await client.from_id("sbx-abc")


@pytest.mark.asyncio
async def test_terminate_wraps_non_json_error_response():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="upstream boom")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError):
        await client.terminate("sbx-abc")


def test_render_async_exposes_sandboxes():
    from render import RenderAsync

    render = RenderAsync(token="test")
    assert isinstance(render.experimental.sandboxes, SandboxClient)


FILES_CONNECT_JSON = {
    "token": "file-token-xyz",
    "uri": "https://proxy.test/files/upload",
    "method": "PUT",
    "expiresAt": "2026-07-21T00:05:00Z",
}


def _capture_upload(captured):
    async def handler(request: httpx.Request) -> httpx.Response:
        # The body is a stream; it has to be read before .content is available.
        captured["body"] = await request.aread()
        captured["method"] = request.method
        captured["url"] = str(request.url)
        captured["headers"] = dict(request.headers)
        return httpx.Response(204)

    return handler


@pytest.mark.asyncio
async def test_mint_file_token_requests_the_files_token_endpoint():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(201, json=FILES_CONNECT_JSON)

    client = _sandbox_client(handler)
    connection = await client.api._mint_file_token(
        "sbx-123", "tea-test", "upload", "/app/data"
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-123/files/upload/token"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["query"]["path"] == "/app/data"
    assert connection["token"] == "file-token-xyz"  # noqa: S105


@pytest.mark.asyncio
async def test_copy_to_file_puts_raw_bytes_with_a_length(mocker, tmp_path):
    source = tmp_path / "hello.txt"
    source.write_bytes(b"hello sandbox\n")
    captured = {}

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, _capture_upload(captured))

    await client.copy_to("sbx-123", source, "/app/hello.txt")

    assert captured["method"] == "PUT"
    assert captured["url"] == "https://proxy.test/files/upload"
    assert captured["headers"]["authorization"] == "Bearer file-token-xyz"
    assert captured["headers"]["content-type"] == "application/octet-stream"
    assert captured["headers"]["content-length"] == "14"
    assert "content-encoding" not in captured["headers"]
    # An explicit length has to win over httpx's chunked default for an
    # iterator body, or the sandbox gets a body it cannot size.
    assert "transfer-encoding" not in captured["headers"]
    assert captured["body"] == b"hello sandbox\n"


@pytest.mark.asyncio
async def test_copy_to_directory_puts_a_gzipped_tar(mocker, tmp_path):
    (tmp_path / "a.txt").write_text("a\n")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_text("b\n")
    (tmp_path / "link.txt").symlink_to("sub/b.txt")
    captured = {}

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, _capture_upload(captured))

    await client.copy_to("sbx-123", tmp_path, "/app/tree")

    assert captured["headers"]["content-type"] == "application/x-tar"
    assert captured["headers"]["content-encoding"] == "gzip"
    # The archive's size is not known until it is produced.
    assert "content-length" not in captured["headers"]

    raw = gzip.decompress(captured["body"])
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        members = {member.name: member for member in tar.getmembers()}
    assert set(members) == {"a.txt", "sub", "sub/b.txt", "link.txt"}
    assert members["link.txt"].issym()


@pytest.mark.asyncio
async def test_copy_to_accepts_any_2xx(mocker, tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        return httpx.Response(200)

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, proxy_handler)

    await client.copy_to("sbx-123", source, "/app/hello.txt")


@pytest.mark.asyncio
async def test_copy_to_proxy_non_2xx_raises_client_error(mocker, tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        return httpx.Response(409, text="path is a directory")

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(ClientError):
        await client.copy_to("sbx-123", source, "/app/hello.txt")


@pytest.mark.asyncio
async def test_copy_to_mint_404_raises_not_found(tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await client.copy_to("sbx-missing", source, "/app/hello.txt")


@pytest.mark.asyncio
async def test_copy_to_missing_local_path_never_mints_a_token(mocker, tmp_path):
    client = _sandbox_client(_noop_handler)
    mint = mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )

    with pytest.raises(FileNotFoundError):
        await client.copy_to("sbx-123", tmp_path / "absent.txt", "/app/absent.txt")
    mint.assert_not_called()


@pytest.mark.asyncio
async def test_copy_to_requires_owner_id(tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")

    client = _sandbox_client(_noop_handler, default_owner_id=None)
    with pytest.raises(RenderError):
        await client.copy_to("sbx-123", source, "/app/hello.txt")


@pytest.mark.asyncio
async def test_copy_to_rejects_a_fifo_before_minting(mocker, tmp_path):
    fifo = tmp_path / "pipe"
    os.mkfifo(fifo)

    client = _sandbox_client(_noop_handler)
    mint = mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )

    # Opening a fifo with no writer would block the event loop forever.
    with pytest.raises(ValueError, match="not a file or directory"):
        await client.copy_to("sbx-123", fifo, "pipe")
    mint.assert_not_called()


@pytest.mark.asyncio
async def test_copy_to_normalizes_the_remote_path(mocker, tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")
    captured = {}

    client = _sandbox_client(_noop_handler)
    mint = mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, _capture_upload(captured))

    # The sandbox rejects any path it would have to clean, so a trailing slash
    # or a redundant separator must not reach it.
    await client.copy_to("sbx-123", source, "workspace//data/")

    assert mint.await_args.args[3] == "workspace/data"


@pytest.mark.asyncio
async def test_copy_to_closes_the_body_when_the_request_fails(mocker, tmp_path):
    (tmp_path / "a.txt").write_text("a\n")
    closed = []
    # Held so the generator cannot be finalized by garbage collection during
    # the test: `closed` then records only a close upload made itself.
    bodies = []

    async def _body():
        try:
            yield b"tar bytes"
        finally:
            closed.append(True)

    def tracked_archive(root):
        body = _body()
        bodies.append(body)
        return body

    mocker.patch("render.experimental.sandbox.api.aiter_tar_gzip", tracked_archive)

    async def proxy_handler(request: httpx.Request) -> httpx.Response:
        # Take a chunk so the body is genuinely in flight, then fail the way a
        # dropped connection does mid-upload.
        stream = cast(httpx.AsyncByteStream, request.stream)
        await stream.__aiter__().__anext__()
        raise httpx.ConnectError("connection reset")

    client = _sandbox_client(_noop_handler)
    mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )
    _patch_proxy(mocker, proxy_handler)

    with pytest.raises(RenderError):
        await client.copy_to("sbx-123", tmp_path, "tree")

    # A failed upload must not leave the archive producer parked on its body.
    # httpx happens to close it here too, so this guards the property rather
    # than upload's own close; it would catch httpx changing that.
    assert closed == [True]


@pytest.mark.asyncio
async def test_copy_to_rejects_an_empty_remote_path(mocker, tmp_path):
    source = tmp_path / "hello.txt"
    source.write_text("hi\n")

    client = _sandbox_client(_noop_handler)
    mint = mocker.patch.object(
        client.api,
        "_mint_file_token",
        new=mocker.AsyncMock(return_value=FILES_CONNECT_JSON),
    )

    # Normalizing "" would give ".", quietly targeting the home directory.
    with pytest.raises(ValueError, match="remote_path is required"):
        await client.copy_to("sbx-123", source, "")
    mint.assert_not_called()
