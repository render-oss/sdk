import json

import httpx
import pytest

from render_sdk.client.errors import RenderError
from render_sdk.experimental.sandbox.client import SandboxClient
from render_sdk.experimental.sandbox.errors import SandboxNotFoundError
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
    assert sandbox.id == "sbx-abc"
    assert sandbox.status == "running"
    assert sandbox.network_policy == "deny-all"
    assert sandbox.terminated_at is None


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
