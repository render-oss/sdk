import json

import httpx
import pytest

from render_sdk.client.errors import ClientError, RenderError
from render_sdk.experimental.sandbox.client import SandboxClient
from render_sdk.experimental.sandbox.errors import (
    SandboxExecError,
    SandboxExecStreamError,
    SandboxNotFoundError,
)
from render_sdk.experimental.sandbox.types import SandboxExecExit, SandboxExecOutput
from render_sdk.public_api.client import AuthenticatedClient

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
        body = [
            {"sandbox": SANDBOX_JSON, "cursor": "cur-1"},
            {"sandbox": {**SANDBOX_JSON, "id": "sbx-def"}, "cursor": "cur-2"},
        ]
        return httpx.Response(200, json=body)

    client = _sandbox_client(handler)
    page = await client.list(status="running", limit=50)

    assert captured["path"] == "/v1/sandboxes"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["query"]["status"] == "running"
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
        "render_sdk.experimental.sandbox.api.httpx.AsyncClient",
        return_value=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


@pytest.mark.asyncio
async def test_mint_run_token_requests_the_token_endpoint():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(201, json=CONNECT_JSON)

    client = _sandbox_client(handler)
    connection = await client.api._mint_run_token("sbx-123", "tea-test", "stream")

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-123/runs/stream/token"
    assert captured["query"]["ownerId"] == "tea-test"
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

    from render_sdk.client.client import Client

    client = Client()
    sandboxes = client.experimental.sandboxes
    assert isinstance(sandboxes, SandboxClient)
    assert sandboxes._default_owner_id == "tea-default"
    assert sandboxes._default_region == "oregon"


def test_sync_experimental_service_exposes_sandboxes(monkeypatch):
    monkeypatch.setenv("RENDER_API_KEY", "test-token")
    monkeypatch.setenv("RENDER_WORKSPACE_ID", "tea-default")

    from render_sdk import Render
    from render_sdk.experimental.sandbox.client_sync import SyncSandboxClient

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
    from render_sdk import RenderAsync

    render = RenderAsync(token="test")
    assert isinstance(render.experimental.sandboxes, SandboxClient)
