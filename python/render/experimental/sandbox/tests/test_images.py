import inspect
import json

import httpx
import pytest

from render.client.errors import ClientError, RateLimitError, RenderError, TimeoutError
from render.experimental.sandbox import _wait
from render.experimental.sandbox.client import BuildClient, ImageClient, SandboxClient
from render.experimental.sandbox.client_sync import SyncSandboxClient
from render.experimental.sandbox.errors import (
    ImageFailedError,
    ImageNotFoundError,
    ImageNotReadyError,
    ImageWaitTimeoutError,
    SnapshotNotFoundError,
)
from render.experimental.sandbox.types import ImageSource, RegistryCredentials
from render.public_api.client import AuthenticatedClient

# An image ID in the API's format. create(image=...) sends only this format as
# an ID; anything else, including a shorter sbb- value, is a name.
IMAGE_ID = "sbb-cph1rs3idesc73a2b2mg"

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

RUNNING_IMAGE_JSON = {
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

SUCCEEDED_IMAGE_JSON = {
    **RUNNING_IMAGE_JSON,
    "status": "succeeded",
    "finishedAt": "2026-10-01T00:00:10Z",
}

FAILED_IMAGE_JSON = {
    **RUNNING_IMAGE_JSON,
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
    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return SyncSandboxClient(internal, default_owner_id=default_owner_id)


@pytest.fixture(params=["async", "sync"])
def make_client(request):
    if request.param == "async":
        return _sandbox_client
    return _sync_sandbox_client


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


@pytest.fixture
def clock(monkeypatch):
    now = [0.0]

    def sleep(seconds):
        now[0] += seconds

    async def asleep(seconds):
        sleep(seconds)

    monkeypatch.setattr(_wait, "monotonic", lambda: now[0])
    monkeypatch.setattr(_wait, "asleep", asleep)
    monkeypatch.setattr(_wait, "sleep", sleep)
    return now


async def _unreachable(request: httpx.Request) -> httpx.Response:
    raise AssertionError("handler should not be reached")


def test_sandbox_client_exposes_images():
    client = _sandbox_client(_unreachable)
    assert isinstance(client.images, ImageClient)


@pytest.mark.asyncio
async def test_import_posts_name_and_source_and_returns_running_image():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = _sandbox_client(handler)
    image = await client.images.import_(
        sandbox_group_id="sbg-abc", name="python", source="python:3.13"
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds"
    assert captured["query"] == {}
    assert captured["body"] == {"name": "python", "sourceImage": "python:3.13"}
    assert image.id == "sbb-abc"
    assert image.sandbox_group_id == "sbg-abc"
    assert image.name == "python"
    assert image.source == ImageSource(
        repository="docker.io/library", image="python", reference="3.13"
    )
    assert image.source_digest == "sha256:c19d4a1"
    assert image.status == "running"
    assert image.failure_reason is None
    assert image.finished_at is None
    assert image.created_at.year == 2026


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "registry_credentials",
    [
        RegistryCredentials(username="bot", password="s3cret"),
        {"username": "bot", "password": "s3cret"},
    ],
    ids=["dataclass", "mapping"],
)
async def test_import_sends_registry_credentials(registry_credentials):
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = _sandbox_client(handler)
    await client.images.import_(
        sandbox_group_id="sbg-abc",
        name="internal",
        source="ghcr.io/acme/internal:1.0",
        registry_credentials=registry_credentials,
    )

    assert captured["body"]["registryCredential"] == {
        "username": "bot",
        "password": "s3cret",
    }


@pytest.mark.asyncio
async def test_import_accepts_a_name_with_the_id_prefix(make_client):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = make_client(handler)
    await _resolve(
        client.images.import_(
            sandbox_group_id="sbg-abc", name="sbb-runtime", source="python:3.13"
        )
    )

    assert captured["body"]["name"] == "sbb-runtime"


@pytest.mark.asyncio
async def test_import_returns_the_existing_image_for_a_known_digest():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json=SUCCEEDED_IMAGE_JSON)

    client = _sandbox_client(handler)
    image = await client.images.import_(
        sandbox_group_id="sbg-abc", name="python", source="python:3.13"
    )

    assert image.status == "succeeded"
    assert image.finished_at is not None


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
async def test_import_maps_api_errors(status, body, error_type, code, match):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match=match) as excinfo:
        await client.images.import_(
            sandbox_group_id="sbg-abc", name="python", source="python:3.13"
        )

    assert type(excinfo.value) is error_type
    assert excinfo.value.code == code


@pytest.mark.asyncio
async def test_from_id_gets_the_image_from_its_group():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=SUCCEEDED_IMAGE_JSON)

    client = _sandbox_client(handler)
    image = await client.images.from_id(sandbox_group_id="sbg-abc", image_id="sbb-abc")

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds/sbb-abc"
    assert captured["query"] == {}
    assert image.id == "sbb-abc"
    assert image.status == "succeeded"
    assert image.finished_at is not None
    assert image.finished_at.second == 10


@pytest.mark.asyncio
async def test_from_id_reads_a_failed_images_reason():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=FAILED_IMAGE_JSON)

    client = _sandbox_client(handler)
    image = await client.images.from_id(sandbox_group_id="sbg-abc", image_id="sbb-abc")

    assert image.status == "failed"
    assert image.failure_reason == "image is not linux/amd64"


@pytest.mark.asyncio
async def test_from_id_raises_not_found_for_a_missing_or_foreign_image():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "not found: build", "code": "build_not_found"}
        )

    client = _sandbox_client(handler)
    with pytest.raises(ImageNotFoundError, match="image sbb-missing not found"):
        await client.images.from_id(sandbox_group_id="sbg-abc", image_id="sbb-missing")


@pytest.mark.asyncio
async def test_from_id_wraps_non_json_error_response():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="upstream boom")

    client = _sandbox_client(handler)
    with pytest.raises(RenderError):
        await client.images.from_id(sandbox_group_id="sbg-abc", image_id="sbb-abc")


# --- wait_until_ready ---


def _image_handler(*statuses):
    """Serve image status checks from a queue; the last one repeats."""
    queue = list(statuses)
    gets = []

    def handler(request: httpx.Request) -> httpx.Response:
        gets.append(request)
        body = queue.pop(0) if len(queue) > 1 else queue[0]
        return httpx.Response(200, json=body)

    return handler, gets


@pytest.mark.asyncio
async def test_wait_until_ready_polls_until_the_image_succeeds(make_client, clock):
    handler, gets = _image_handler(RUNNING_IMAGE_JSON, SUCCEEDED_IMAGE_JSON)
    client = make_client(handler)

    image = await _resolve(
        client.images.wait_until_ready(sandbox_group_id="sbg-abc", image_id="sbb-abc")
    )

    assert image.status == "succeeded"
    assert gets[0].url.path == "/v1/sandbox-groups/sbg-abc/builds/sbb-abc"
    assert len(gets) == 2


@pytest.mark.asyncio
async def test_wait_until_ready_raises_with_the_reason_an_import_failed(
    make_client, clock
):
    handler, _ = _image_handler(FAILED_IMAGE_JSON)
    client = make_client(handler)

    with pytest.raises(ImageFailedError) as excinfo:
        await _resolve(
            client.images.wait_until_ready(
                sandbox_group_id="sbg-abc", image_id="sbb-abc"
            )
        )

    assert (
        str(excinfo.value) == "image sbb-abc failed to import: image is not linux/amd64"
    )
    assert excinfo.value.image_id == "sbb-abc"
    assert excinfo.value.failure_reason == "image is not linux/amd64"


@pytest.mark.asyncio
async def test_wait_until_ready_times_out_after_10_minutes_by_default(
    make_client, clock
):
    handler, _ = _image_handler(RUNNING_IMAGE_JSON)
    client = make_client(handler)

    with pytest.raises(ImageWaitTimeoutError) as excinfo:
        await _resolve(
            client.images.wait_until_ready(
                sandbox_group_id="sbg-abc", image_id="sbb-abc"
            )
        )

    error = excinfo.value
    assert isinstance(error, TimeoutError)
    assert error.image_id == "sbb-abc"
    assert error.timeout_seconds == 600
    assert error.last_status == "running"
    assert clock[0] == pytest.approx(600)


# --- create(image=...) ---


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("image", "field", "other"),
    [
        (IMAGE_ID, "buildId", "buildName"),
        ("python", "buildName", "buildId"),
        ("sbb-runtime", "buildName", "buildId"),
        ("sbb-abc", "buildName", "buildId"),
    ],
    ids=["id", "name", "name-with-id-prefix", "short-id-like-name"],
)
async def test_sandbox_create_sends_an_image_by_id_or_name(image, field, other):
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    sandbox = await client.create(image=image)

    assert captured["body"][field] == image
    assert other not in captured["body"]
    assert sandbox.id == "sbx-abc"


@pytest.mark.asyncio
async def test_sandbox_create_omits_image_fields_by_default():
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
        {"image": "sbb-abc", "snapshot_id": "snp-abc"},
        {"image": "python", "snapshot_name": "gold"},
        {"image": "python", "build_id": "sbb-abc"},
        {"build_id": "sbb-abc", "build_name": "python"},
        {"build_name": "python", "snapshot_id": "snp-abc"},
    ],
    ids=[
        "image-and-snapshot-id",
        "image-and-snapshot-name",
        "image-and-build-id",
        "build-id-and-build-name",
        "build-name-and-snapshot-id",
    ],
)
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_sandbox_create_rejects_an_image_with_another_source(kwargs):
    client = _sandbox_client(_unreachable)

    with pytest.raises(ValueError, match="mutually exclusive"):
        await client.create(**kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("image", "status", "body", "error_type", "code", "match"),
    [
        (
            IMAGE_ID,
            404,
            {"message": "not found: build", "code": "build_not_found"},
            ImageNotFoundError,
            "build_not_found",
            f"image {IMAGE_ID} not found",
        ),
        (
            "missing",
            404,
            {"message": "not found: build", "code": "build_not_found"},
            ImageNotFoundError,
            "build_not_found",
            "image missing not found",
        ),
        (
            IMAGE_ID,
            409,
            {"message": "build has not succeeded", "code": "build_not_succeeded"},
            ImageNotReadyError,
            "build_not_succeeded",
            "build has not succeeded",
        ),
        (
            "python",
            409,
            {"message": "build has not succeeded", "code": "build_not_succeeded"},
            ImageNotReadyError,
            "build_not_succeeded",
            "build has not succeeded",
        ),
        (
            IMAGE_ID,
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
            IMAGE_ID,
            404,
            {"message": "not found: sandbox group"},
            ClientError,
            None,
            "not found",
        ),
        (
            "python",
            409,
            {"message": "conflict"},
            ClientError,
            None,
            "conflict",
        ),
    ],
    ids=[
        "id-404",
        "name-404",
        "id-409-not-succeeded",
        "name-409-not-succeeded",
        "id-409-with-code",
        "id-404-without-code",
        "name-409-without-code",
    ],
)
async def test_sandbox_create_maps_image_errors(
    image, status, body, error_type, code, match
):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    client = _sandbox_client(handler)
    with pytest.raises(ClientError, match=match) as excinfo:
        await client.create(image=image)

    assert type(excinfo.value) is error_type
    assert excinfo.value.code == code


@pytest.mark.asyncio
async def test_sandbox_create_snapshot_errors_are_unaffected():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "snapshot not found", "code": "snapshot_not_found"}
        )

    client = _sandbox_client(handler)
    with pytest.raises(SnapshotNotFoundError, match="snapshot missing not found"):
        await client.create(snapshot_name="missing")


# --- deprecated build names ---


@pytest.mark.asyncio
async def test_builds_create_warns_and_imports_the_image():
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = _sandbox_client(handler)
    assert isinstance(client.builds, BuildClient)
    with pytest.warns(DeprecationWarning, match="images.import_"):
        build = await client.builds.create(
            sandbox_group_id="sbg-abc",
            name="python",
            source_image="python:3.13",
            registry_credential=RegistryCredentials(username="bot", password="s3cret"),
        )

    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds"
    assert captured["body"] == {
        "name": "python",
        "sourceImage": "python:3.13",
        "registryCredential": {"username": "bot", "password": "s3cret"},
    }
    assert build.id == "sbb-abc"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_builds_create_still_sends_a_name_starting_with_sbb(make_client):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = make_client(handler)
    await _resolve(
        client.builds.create(
            sandbox_group_id="sbg-abc", name="sbb-runtime", source_image="python:3.13"
        )
    )

    assert captured["body"] == {"name": "sbb-runtime", "sourceImage": "python:3.13"}


@pytest.mark.asyncio
async def test_builds_from_id_warns_and_gets_the_image():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/sandbox-groups/sbg-abc/builds/sbb-abc"
        return httpx.Response(200, json=SUCCEEDED_IMAGE_JSON)

    client = _sandbox_client(handler)
    with pytest.warns(DeprecationWarning, match="images.from_id"):
        build = await client.builds.from_id(
            sandbox_group_id="sbg-abc", build_id="sbb-abc"
        )

    assert build.status == "succeeded"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kwargs", "field", "value"),
    [
        ({"build_id": "sbb-abc"}, "buildId", "sbb-abc"),
        ({"build_name": "python"}, "buildName", "python"),
    ],
    ids=["build-id", "build-name"],
)
async def test_sandbox_create_with_a_build_warns_and_still_sends_it(
    kwargs, field, value
):
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sandbox_client(handler)
    with pytest.warns(DeprecationWarning, match="use image"):
        await client.create(**kwargs)

    assert captured["body"][field] == value


# --- sync client ---


def test_sync_import_posts_and_returns_image():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = _sync_sandbox_client(handler)
    image = client.images.import_(
        sandbox_group_id="sbg-abc",
        name="python",
        source="python:3.13",
        registry_credentials={"username": "bot", "password": "s3cret"},
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/builds"
    assert captured["body"] == {
        "name": "python",
        "sourceImage": "python:3.13",
        "registryCredential": {"username": "bot", "password": "s3cret"},
    }
    assert image.id == "sbb-abc"
    assert image.status == "running"


def test_sync_from_id_raises_not_found():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404, json={"message": "not found: build", "code": "build_not_found"}
        )

    client = _sync_sandbox_client(handler)
    with pytest.raises(ImageNotFoundError):
        client.images.from_id(sandbox_group_id="sbg-abc", image_id="sbb-missing")


def test_sync_sandbox_create_sends_an_image_name():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(201, json=SANDBOX_JSON)

    client = _sync_sandbox_client(handler)
    sandbox = client.create(image="python")

    assert captured["body"]["buildName"] == "python"
    assert sandbox.id == "sbx-abc"


def test_sync_sandbox_create_raises_not_ready_for_an_unfinished_image():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={"message": "build has not succeeded", "code": "build_not_succeeded"},
        )

    client = _sync_sandbox_client(handler)
    with pytest.raises(ImageNotReadyError):
        client.create(image=IMAGE_ID)


def test_sync_builds_create_warns():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json=RUNNING_IMAGE_JSON)

    client = _sync_sandbox_client(handler)
    with pytest.warns(DeprecationWarning):
        client.builds.create(
            sandbox_group_id="sbg-abc", name="python", source_image="python:3.13"
        )
