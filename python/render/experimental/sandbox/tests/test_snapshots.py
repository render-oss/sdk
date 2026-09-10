import json
from datetime import datetime, timezone

import httpx
import pytest

from render.client.errors import ClientError, RenderError
from render.experimental.sandbox.client import SandboxClient, SnapshotClient
from render.experimental.sandbox.errors import (
    SandboxNotFoundError,
    SnapshotNotFoundError,
    SnapshotNotReadyError,
    SnapshotPlanMismatchError,
)
from render.public_api.client import AuthenticatedClient

SANDBOX_JSON = {
    "id": "sbx-abc",
    "status": "creating",
    "plan": "standard",
    "networkPolicy": {"default": "deny-all"},
    "region": "oregon",
    "timeoutSeconds": 300,
    "createdAt": "2026-09-01T00:00:00Z",
    "terminatedAt": None,
}

CREATING_SNAPSHOT_JSON = {
    "id": "snp-abc",
    "sandboxGroupId": "sbg-abc",
    "sourceSandboxId": "sbx-abc",
    "kind": "filesystem",
    "status": "creating",
    "plan": "standard",
    "requestedAt": "2026-09-01T00:00:00Z",
    "capturedAt": None,
    "expiresAt": "2026-09-08T00:00:00Z",
    "sizeBytes": None,
    "error": None,
}

AVAILABLE_SNAPSHOT_JSON = {
    **CREATING_SNAPSHOT_JSON,
    "kind": "runtime",
    "status": "available",
    "capturedAt": "2026-09-01T00:00:05Z",
    "expiresAt": "2026-09-08T00:00:05Z",
    "sizeBytes": 1048576,
}


def _sandbox_client(handler, *, default_owner_id="tea-test"):
    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return SandboxClient(internal, default_owner_id=default_owner_id)


def _sync_sandbox_client(handler, *, default_owner_id="tea-test"):
    from render.experimental.sandbox.client_sync import SyncSandboxClient

    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return SyncSandboxClient(internal, default_owner_id=default_owner_id)


async def _unreachable(request: httpx.Request) -> httpx.Response:
    raise AssertionError("handler should not be reached")


def test_sandbox_client_exposes_snapshots():
    client = _sandbox_client(_unreachable)
    assert isinstance(client.snapshots, SnapshotClient)


@pytest.mark.asyncio
async def test_create_posts_kind_and_returns_creating_snapshot():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        captured["body"] = json.loads(request.content)
        return httpx.Response(202, json=CREATING_SNAPSHOT_JSON)

    client = _sandbox_client(handler)
    snapshot = await client.snapshots.create("sbx-abc")

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-abc/snapshots"
    assert captured["query"]["ownerId"] == "tea-test"
    assert captured["body"] == {"kind": "filesystem"}
    assert snapshot.id == "snp-abc"
    assert snapshot.sandbox_group_id == "sbg-abc"
    assert snapshot.source_sandbox_id == "sbx-abc"
    assert snapshot.kind == "filesystem"
    assert snapshot.status == "creating"
    assert snapshot.plan == "standard"
    assert snapshot.requested_at.isoformat() == "2026-09-01T00:00:00+00:00"
    assert snapshot.captured_at is None
    assert snapshot.expires_at.isoformat() == "2026-09-08T00:00:00+00:00"
    assert snapshot.size_bytes is None
    assert snapshot.error is None


@pytest.mark.asyncio
async def test_create_sends_the_runtime_kind_and_an_explicit_owner_id():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["query"] = dict(request.url.params)
        captured["body"] = json.loads(request.content)
        return httpx.Response(202, json=CREATING_SNAPSHOT_JSON)

    client = _sandbox_client(handler)
    await client.snapshots.create("sbx-abc", kind="runtime", owner_id="tea-other")

    assert captured["query"]["ownerId"] == "tea-other"
    assert captured["body"] == {"kind": "runtime"}


@pytest.mark.asyncio
async def test_create_rejects_an_unknown_kind():
    client = _sandbox_client(_unreachable)
    with pytest.raises(ValueError, match="bogus"):
        await client.snapshots.create("sbx-abc", kind="bogus")


@pytest.mark.asyncio
async def test_create_sends_expires_at():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(202, json=CREATING_SNAPSHOT_JSON)

    client = _sandbox_client(handler)
    await client.snapshots.create(
        "sbx-abc", expires_at=datetime(2026, 9, 8, tzinfo=timezone.utc)
    )

    assert captured["body"]["expiresAt"].startswith("2026-09-08T00:00:00")


@pytest.mark.asyncio
async def test_create_raises_sandbox_not_found_on_404():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "sandbox not found"})

    client = _sandbox_client(handler)
    with pytest.raises(SandboxNotFoundError):
        await client.snapshots.create("sbx-missing")


@pytest.mark.asyncio
async def test_create_surfaces_sandbox_not_running_as_a_client_error_with_code():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409, json={"message": "sandbox is suspended", "code": "sandbox_not_running"}
        )

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match="sandbox is suspended") as excinfo:
        await client.snapshots.create("sbx-abc")

    assert type(excinfo.value) is ClientError
    assert excinfo.value.code == "sandbox_not_running"


@pytest.mark.asyncio
async def test_from_id_gets_the_snapshot_from_its_group():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=AVAILABLE_SNAPSHOT_JSON)

    client = _sandbox_client(handler)
    snapshot = await client.snapshots.from_id(
        sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
    )

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/snapshots/snp-abc"
    assert captured["query"]["ownerId"] == "tea-test"
    assert snapshot.kind == "runtime"
    assert snapshot.status == "available"
    assert snapshot.captured_at.isoformat() == "2026-09-01T00:00:05+00:00"
    assert snapshot.expires_at.isoformat() == "2026-09-08T00:00:05+00:00"
    assert snapshot.size_bytes == 1048576


@pytest.mark.asyncio
async def test_from_id_reads_a_failed_snapshots_error():
    async def handler(request: httpx.Request) -> httpx.Response:
        failed = {**CREATING_SNAPSHOT_JSON, "status": "failed", "error": "disk full"}
        return httpx.Response(200, json=failed)

    client = _sandbox_client(handler)
    snapshot = await client.snapshots.from_id(
        sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
    )

    assert snapshot.status == "failed"
    assert snapshot.error == "disk full"


@pytest.mark.asyncio
async def test_list_by_group_sends_filters_and_returns_snapshots_and_cursor():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["owner_id"] = request.url.params.get_list("ownerId")
        captured["status"] = request.url.params.get_list("status")
        captured["cursor"] = request.url.params.get("cursor")
        captured["limit"] = request.url.params.get("limit")
        body = [
            {"snapshot": AVAILABLE_SNAPSHOT_JSON, "cursor": "cur-1"},
            {
                "snapshot": {**CREATING_SNAPSHOT_JSON, "id": "snp-def"},
                "cursor": "cur-2",
            },
        ]
        return httpx.Response(200, json=body)

    client = _sandbox_client(handler)
    page = await client.snapshots.list(
        sandbox_group_id="sbg-abc",
        status=["available", "creating"],
        cursor="cur-0",
        limit=50,
    )

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/snapshots"
    assert captured["owner_id"] == ["tea-test"]
    assert captured["status"] == ["available", "creating"]
    assert captured["cursor"] == "cur-0"
    assert captured["limit"] == "50"
    assert [s.id for s in page.snapshots] == ["snp-abc", "snp-def"]
    assert page.next_cursor == "cur-2"


@pytest.mark.asyncio
async def test_list_empty_has_no_cursor():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    page = await client.snapshots.list(sandbox_group_id="sbg-abc")

    assert page.snapshots == []
    assert page.next_cursor is None


@pytest.mark.asyncio
async def test_list_sends_a_single_status_string_as_one_value():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    await client.snapshots.list(sandbox_group_id="sbg-abc", status="available")

    assert captured["status"] == ["available"]


@pytest.mark.asyncio
async def test_list_omits_optional_params_when_not_given():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    client = _sandbox_client(handler)
    await client.snapshots.list(sandbox_group_id="sbg-abc")

    assert set(captured["query"]) == {"ownerId"}


@pytest.mark.asyncio
async def test_list_rejects_an_unknown_status():
    client = _sandbox_client(_unreachable)
    with pytest.raises(ValueError, match="bogus"):
        await client.snapshots.list(sandbox_group_id="sbg-abc", status="bogus")


@pytest.mark.asyncio
async def test_list_raises_client_error_on_404():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "sandbox group not found"})

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match="sandbox group not found"):
        await client.snapshots.list(sandbox_group_id="sbg-missing")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "call"),
    [
        (202, lambda snapshots: snapshots.create("sbx-abc")),
        (
            200,
            lambda snapshots: snapshots.from_id(
                sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
            ),
        ),
        (
            204,
            lambda snapshots: snapshots.delete(
                sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
            ),
        ),
    ],
    ids=["create", "from_id", "delete"],
)
async def test_omits_owner_id_when_none_is_configured(status, call):
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["query"] = dict(request.url.params)
        return httpx.Response(status, json=CREATING_SNAPSHOT_JSON)

    client = _sandbox_client(handler, default_owner_id=None)
    await call(client.snapshots)

    assert "ownerId" not in captured["query"]


@pytest.mark.asyncio
async def test_list_requires_owner_id():
    client = _sandbox_client(_unreachable, default_owner_id=None)
    with pytest.raises(RenderError):
        await client.snapshots.list(sandbox_group_id="sbg-abc")


@pytest.mark.asyncio
async def test_delete_sends_delete_and_returns_none():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(204)

    client = _sandbox_client(handler)
    await client.snapshots.delete(sandbox_group_id="sbg-abc", snapshot_id="snp-abc")

    assert captured["method"] == "DELETE"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/snapshots/snp-abc"
    assert captured["query"]["ownerId"] == "tea-test"


def _from_id(client):
    return client.snapshots.from_id(sandbox_group_id="sbg-abc", snapshot_id="snp-abc")


def _delete(client):
    return client.snapshots.delete(sandbox_group_id="sbg-abc", snapshot_id="snp-abc")


def _create_from_snapshot(client):
    return client.create(snapshot_id="snp-abc", plan="pro")


def _create_plain(client):
    return client.create()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("call", "status", "body", "error_type", "code", "match"),
    [
        (
            _from_id,
            404,
            {"message": "snapshot not found"},
            SnapshotNotFoundError,
            None,
            "snp-abc",
        ),
        (
            _delete,
            404,
            {"message": "snapshot not found"},
            SnapshotNotFoundError,
            None,
            "snp-abc",
        ),
        (
            _delete,
            409,
            {"message": "still creating", "code": "snapshot_creating"},
            SnapshotNotReadyError,
            "snapshot_creating",
            "still creating",
        ),
        (
            _delete,
            409,
            {"message": "something else", "code": "some_other_code"},
            ClientError,
            "some_other_code",
            "something else",
        ),
        (
            _create_from_snapshot,
            404,
            {"message": "snapshot not found", "code": "snapshot_not_found"},
            SnapshotNotFoundError,
            "snapshot_not_found",
            "snp-abc",
        ),
        (
            _create_from_snapshot,
            404,
            {"message": "workspace not found"},
            ClientError,
            None,
            "workspace not found",
        ),
        (
            _create_plain,
            404,
            {"message": "workspace not found"},
            ClientError,
            None,
            "workspace not found",
        ),
        (
            _create_from_snapshot,
            409,
            {"message": "snapshot is creating", "code": "snapshot_not_available"},
            SnapshotNotReadyError,
            "snapshot_not_available",
            "snapshot is creating",
        ),
        (
            _create_from_snapshot,
            409,
            {"message": "requires plan standard", "code": "snapshot_plan_mismatch"},
            SnapshotPlanMismatchError,
            "snapshot_plan_mismatch",
            "requires plan standard",
        ),
    ],
    ids=[
        "from_id-404",
        "delete-404",
        "delete-409-creating",
        "delete-409-other",
        "create-404-snapshot_not_found",
        "create-404-no-code",
        "create-without-snapshot-404",
        "create-409-not_available",
        "create-409-plan_mismatch",
    ],
)
async def test_maps_api_errors_to_snapshot_error_types(
    call, status, body, error_type, code, match
):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match=match) as excinfo:
        await call(client)

    assert type(excinfo.value) is error_type
    assert excinfo.value.code == code


@pytest.mark.asyncio
async def test_delete_wraps_non_json_error_response():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="upstream boom")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError):
        await client.snapshots.delete(sandbox_group_id="sbg-abc", snapshot_id="snp-abc")


@pytest.mark.asyncio
async def test_create_wraps_unexpected_exceptions_as_render_errors():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise RuntimeError("transport exploded")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError, match="unexpected error") as excinfo:
        await client.snapshots.create("sbx-abc")
    assert type(excinfo.value) is RenderError
    assert isinstance(excinfo.value.__cause__, RuntimeError)


@pytest.mark.asyncio
async def test_sandbox_create_sends_snapshot_id():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create(snapshot_id="snp-abc")

    assert captured["body"]["snapshotId"] == "snp-abc"
    assert sandbox.id == "sbx-abc"


@pytest.mark.asyncio
async def test_sandbox_create_omits_snapshot_id_by_default():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create()

    assert "snapshotId" not in captured["body"]
    assert sandbox.id == "sbx-abc"


def test_sync_create_posts_kind_and_returns_snapshot():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content)
        return httpx.Response(202, json=CREATING_SNAPSHOT_JSON)

    client = _sync_sandbox_client(handler)
    snapshot = client.snapshots.create("sbx-abc", kind="runtime")

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandboxes/sbx-abc/snapshots"
    assert captured["body"] == {"kind": "runtime"}
    assert snapshot.id == "snp-abc"
    assert snapshot.status == "creating"


def test_sync_list_by_group_returns_snapshots_and_cursor():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["status"] = request.url.params.get_list("status")
        return httpx.Response(
            200, json=[{"snapshot": AVAILABLE_SNAPSHOT_JSON, "cursor": "cur-1"}]
        )

    client = _sync_sandbox_client(handler)
    page = client.snapshots.list(sandbox_group_id="sbg-abc", status="available")

    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/snapshots"
    assert captured["status"] == ["available"]
    assert [s.id for s in page.snapshots] == ["snp-abc"]
    assert page.next_cursor == "cur-1"


def test_sync_delete_raises_not_ready_while_the_snapshot_is_creating():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409, json={"message": "still creating", "code": "snapshot_creating"}
        )

    client = _sync_sandbox_client(handler)
    with pytest.raises(SnapshotNotReadyError) as excinfo:
        client.snapshots.delete(sandbox_group_id="sbg-abc", snapshot_id="snp-abc")
    assert excinfo.value.code == "snapshot_creating"


def test_sync_sandbox_create_sends_snapshot_id():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sync_sandbox_client(handler)
    sandbox = client.create(snapshot_id="snp-abc")

    assert captured["body"]["snapshotId"] == "snp-abc"
    assert sandbox.id == "sbx-abc"
