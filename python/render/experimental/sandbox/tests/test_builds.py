import json

import httpx
import pytest

from render.client.errors import ClientError, RateLimitError, RenderError
from render.experimental.sandbox.client import BuildClient, SandboxClient
from render.experimental.sandbox.errors import (
    BuildNotFoundError,
    BuildNotReadyError,
    SnapshotNotFoundError,
)
from render.experimental.sandbox.types import BuildSource, RegistryCredential
from render.public_api.client import AuthenticatedClient

SANDBOX_JSON = {
    "id": "sbx-abc",
    "status": "creating",
    "plan": "standard",
    "networkPolicy": {"type": "deny-all"},
    "region": "oregon",
    "timeoutSeconds": 300,
    "idleTimeoutSeconds": 900,
    "createdAt": "2026-10-01T00:00:00Z",
    "terminatedAt": None,
}

RUNNING_BUILD_JSON = {
    "id": "sbb-abc",
    "sandboxGroupId": "sbg-abc",
    "name": "python",
    "source": {
        "repository": "docker.io/library",
        "image": "python",
        "reference": "3.13",
    },
    "sourceDigest": "sha256:c19d4a1",
    "status": "running",
    "failureReason": None,
    "createdAt": "2026-10-01T00:00:00Z",
    "finishedAt": None,
}

SUCCEEDED_BUILD_JSON = {
    **RUNNING_BUILD_JSON,
    "status": "succeeded",
    "finishedAt": "2026-10-01T00:00:10Z",
}

FAILED_BUILD_JSON = {
    **RUNNING_BUILD_JSON,
    "status": "failed",
    "failureReason": "image is not linux/amd64",
    "finishedAt": "2026-10-01T00:00:10Z",
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


def test_sandbox_client_exposes_builds():
    client = _sandbox_client(_unreachable)
    assert isinstance(client.builds, BuildClient)


@pytest.mark.asyncio
async def test_create_posts_name_and_image_and_returns_running_build():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_BUILD_JSON)

    client = _sandbox_client(handler)
    build = await client.builds.create(
        sandbox_group_id="sbg-abc", name="python", source_image="python:3.13"
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds"
    assert captured["query"] == {}
    assert captured["body"] == {"name": "python", "sourceImage": "python:3.13"}
    assert build.id == "sbb-abc"
    assert build.sandbox_group_id == "sbg-abc"
    assert build.name == "python"
    assert build.source == BuildSource(
        repository="docker.io/library", image="python", reference="3.13"
    )
    assert build.source_digest == "sha256:c19d4a1"
    assert build.status == "running"
    assert build.failure_reason is None
    assert build.finished_at is None
    assert build.created_at.year == 2026


@pytest.mark.asyncio
async def test_create_sends_registry_credential_only_when_given():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_BUILD_JSON)

    client = _sandbox_client(handler)
    await client.builds.create(
        sandbox_group_id="sbg-abc",
        name="internal",
        source_image="ghcr.io/acme/internal:1.0",
        registry_credential=RegistryCredential(username="bot", password="s3cret"),
    )

    assert captured["body"]["registryCredential"] == {
        "username": "bot",
        "password": "s3cret",
    }


@pytest.mark.asyncio
async def test_create_returns_the_existing_build_for_a_known_digest():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json=SUCCEEDED_BUILD_JSON)

    client = _sandbox_client(handler)
    build = await client.builds.create(
        sandbox_group_id="sbg-abc", name="python", source_image="python:3.13"
    )

    assert build.status == "succeeded"
    assert build.finished_at is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "body", "error_type", "code", "match"),
    [
        (
            400,
            {"message": "invalid sourceImage: could not parse reference"},
            ClientError,
            None,
            "could not parse reference",
        ),
        (
            400,
            {"message": "invalid sandbox group ID", "code": "invalid_sandbox_group_id"},
            ClientError,
            "invalid_sandbox_group_id",
            "invalid sandbox group ID",
        ),
        (404, {"message": "not found: sandbox group"}, ClientError, None, "not found"),
        (
            409,
            {
                "message": "sandbox group is suspended",
                "code": "sandbox_group_suspended",
            },
            ClientError,
            "sandbox_group_suspended",
            "suspended",
        ),
        (
            429,
            {"message": "sandbox group has too many builds in progress (limit 5)"},
            RateLimitError,
            None,
            "limit 5",
        ),
    ],
    ids=[
        "400-bad-image",
        "400-bad-group-id",
        "404-group",
        "409-suspended",
        "429-limit",
    ],
)
async def test_create_maps_api_errors(status, body, error_type, code, match):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match=match) as excinfo:
        await client.builds.create(
            sandbox_group_id="sbg-abc", name="python", source_image="python:3.13"
        )

    assert type(excinfo.value) is error_type
    assert excinfo.value.code == code


@pytest.mark.asyncio
async def test_from_id_gets_the_build_from_its_group():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=SUCCEEDED_BUILD_JSON)

    client = _sandbox_client(handler)
    build = await client.builds.from_id(sandbox_group_id="sbg-abc", build_id="sbb-abc")

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds/sbb-abc"
    assert captured["query"] == {}
    assert build.id == "sbb-abc"
    assert build.status == "succeeded"
    assert build.finished_at is not None
    assert build.finished_at.second == 10


@pytest.mark.asyncio
async def test_from_id_reads_a_failed_builds_reason():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=FAILED_BUILD_JSON)

    client = _sandbox_client(handler)
    build = await client.builds.from_id(sandbox_group_id="sbg-abc", build_id="sbb-abc")

    assert build.status == "failed"
    assert build.failure_reason == "image is not linux/amd64"


@pytest.mark.asyncio
async def test_from_id_raises_not_found_for_a_missing_or_foreign_build():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "not found: build", "code": "build_not_found"}
        )

    client = _sandbox_client(handler)
    with pytest.raises(BuildNotFoundError, match="build sbb-missing not found"):
        await client.builds.from_id(sandbox_group_id="sbg-abc", build_id="sbb-missing")


@pytest.mark.asyncio
async def test_from_id_wraps_non_json_error_response():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="upstream boom")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError):
        await client.builds.from_id(sandbox_group_id="sbg-abc", build_id="sbb-abc")


@pytest.mark.asyncio
async def test_sandbox_create_sends_build_id():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create(build_id="sbb-abc")

    assert captured["body"]["buildId"] == "sbb-abc"
    assert "buildName" not in captured["body"]
    assert sandbox.id == "sbx-abc"


@pytest.mark.asyncio
async def test_sandbox_create_sends_build_name():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create(build_name="python")

    assert captured["body"]["buildName"] == "python"
    assert "buildId" not in captured["body"]
    assert sandbox.id == "sbx-abc"


@pytest.mark.asyncio
async def test_sandbox_create_omits_build_fields_by_default():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    await client.create()

    assert "buildId" not in captured["body"]
    assert "buildName" not in captured["body"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kwargs",
    [
        {"build_id": "sbb-abc", "build_name": "python"},
        {"build_id": "sbb-abc", "snapshot_id": "snp-abc"},
        {"build_id": "sbb-abc", "snapshot_name": "gold"},
        {"build_name": "python", "snapshot_id": "snp-abc"},
        {"build_name": "python", "snapshot_name": "gold"},
    ],
    ids=[
        "id-and-name",
        "id-and-snapshot-id",
        "id-and-snapshot-name",
        "name-and-snapshot-id",
        "name-and-snapshot-name",
    ],
)
async def test_sandbox_create_rejects_a_build_with_another_source(kwargs):
    client = _sandbox_client(_unreachable)

    with pytest.raises(ValueError, match="mutually exclusive"):
        await client.create(**kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kwargs", "status", "body", "error_type", "code", "match"),
    [
        (
            {"build_id": "sbb-missing"},
            404,
            {"message": "not found: build", "code": "build_not_found"},
            BuildNotFoundError,
            "build_not_found",
            "build sbb-missing not found",
        ),
        (
            {"build_name": "missing"},
            404,
            {"message": "not found: build", "code": "build_not_found"},
            BuildNotFoundError,
            "build_not_found",
            "build missing not found",
        ),
        (
            {"build_id": "sbb-running"},
            409,
            {"message": "build has not succeeded", "code": "build_not_succeeded"},
            BuildNotReadyError,
            "build_not_succeeded",
            "build has not succeeded",
        ),
        (
            {"build_name": "python"},
            409,
            {"message": "build has not succeeded", "code": "build_not_succeeded"},
            BuildNotReadyError,
            "build_not_succeeded",
            "build has not succeeded",
        ),
        (
            {"build_id": "sbb-abc"},
            409,
            {
                "message": "sandbox group is suspended",
                "code": "sandbox_group_suspended",
            },
            ClientError,
            "sandbox_group_suspended",
            "suspended",
        ),
        (
            {"build_id": "sbb-abc"},
            400,
            {"message": "a build excludes snapshotId and snapshotName"},
            ClientError,
            None,
            "excludes",
        ),
        (
            {"build_id": "sbb-abc"},
            404,
            {"message": "not found: sandbox group"},
            ClientError,
            None,
            "not found",
        ),
        (
            {"build_name": "python"},
            409,
            {"message": "conflict"},
            ClientError,
            None,
            "conflict",
        ),
        (
            {"snapshot_name": "missing"},
            404,
            {"message": "snapshot not found", "code": "snapshot_not_found"},
            SnapshotNotFoundError,
            "snapshot_not_found",
            "snapshot missing not found",
        ),
    ],
    ids=[
        "id-404",
        "name-404",
        "id-409-not-succeeded",
        "name-409-not-succeeded",
        "id-409-with-code",
        "id-400",
        "id-404-without-code",
        "name-409-without-code",
        "snapshot-404-unaffected",
    ],
)
async def test_sandbox_create_maps_build_errors(
    kwargs, status, body, error_type, code, match
):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match=match) as excinfo:
        await client.create(**kwargs)

    assert type(excinfo.value) is error_type
    assert excinfo.value.code == code


# --- sync client ---


def test_sync_create_posts_and_returns_build():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_BUILD_JSON)

    client = _sync_sandbox_client(handler)
    build = client.builds.create(
        sandbox_group_id="sbg-abc",
        name="python",
        source_image="python:3.13",
        registry_credential=RegistryCredential(username="bot", password="s3cret"),
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds"
    assert captured["body"] == {
        "name": "python",
        "sourceImage": "python:3.13",
        "registryCredential": {"username": "bot", "password": "s3cret"},
    }
    assert build.id == "sbb-abc"
    assert build.status == "running"


def test_sync_from_id_raises_not_found():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "not found: build", "code": "build_not_found"}
        )

    client = _sync_sandbox_client(handler)
    with pytest.raises(BuildNotFoundError):
        client.builds.from_id(sandbox_group_id="sbg-abc", build_id="sbb-missing")


def test_sync_sandbox_create_sends_build_name():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sync_sandbox_client(handler)
    sandbox = client.create(build_name="python")

    assert captured["body"]["buildName"] == "python"
    assert sandbox.id == "sbx-abc"


def test_sync_sandbox_create_raises_not_ready_for_an_unfinished_build():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={"message": "build has not succeeded", "code": "build_not_succeeded"},
        )

    client = _sync_sandbox_client(handler)
    with pytest.raises(BuildNotReadyError):
        client.create(build_id="sbb-running")


def test_sync_sandbox_create_rejects_build_id_and_name_together():
    client = _sync_sandbox_client(lambda request: httpx.Response(500))

    with pytest.raises(ValueError, match="mutually exclusive"):
        client.create(build_id="sbb-abc", build_name="python")
