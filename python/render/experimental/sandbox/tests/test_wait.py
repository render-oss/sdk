import asyncio
import inspect
import json

import httpx
import pytest

from render.client.errors import RenderError, ServerError, TimeoutError
from render.experimental.sandbox import _wait
from render.experimental.sandbox.client import SandboxClient
from render.experimental.sandbox.client_sync import SyncSandboxClient
from render.experimental.sandbox.errors import (
    SandboxCreateWaitError,
    SandboxNotFoundError,
    SandboxNotRunningError,
    SandboxWaitTimeoutError,
    SnapshotCreateWaitError,
    SnapshotFailedError,
    SnapshotWaitTimeoutError,
)
from render.experimental.sandbox.types import SandboxWaitOptions
from render.public_api.client import AuthenticatedClient


def _sandbox_json(status):
    return {
        "id": "sbx-abc",
        "status": status,
        "plan": "starter",
        "networkPolicy": {"type": "deny-all"},
        "region": "oregon",
        "timeoutSeconds": 300,
        "idleTimeoutSeconds": 900,
        "createdAt": "2026-09-01T00:00:00Z",
        "terminatedAt": None,
    }


def _snapshot_json(status, error=None):
    return {
        "id": "snp-abc",
        "sandboxGroupId": "sbg-abc",
        "sourceSandboxId": "sbx-abc",
        "name": None,
        "kind": "filesystem",
        "status": status,
        "plan": "starter",
        "requestedAt": "2026-09-01T00:00:00Z",
        "capturedAt": None,
        "expiresAt": "2026-09-08T00:00:00Z",
        "sizeBytes": None,
        "error": error,
    }


class _Api:
    """A fake API that serves sandbox creates and a queue of status checks.

    The last status repeats once the queue runs out.
    """

    def __init__(self, *polled, created="creating", snapshot=False):
        self.created = created
        self.polled = list(polled)
        self.snapshot = snapshot
        self.requests: list[httpx.Request] = []

    @property
    def gets(self):
        return [r for r in self.requests if r.method == "GET"]

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.method == "POST" and self.snapshot:
            return httpx.Response(202, json=_snapshot_json(*self.created))
        if request.method == "POST":
            return httpx.Response(201, json=_sandbox_json(self.created))
        status = self.polled.pop(0) if len(self.polled) > 1 else self.polled[0]
        if isinstance(status, httpx.Response):
            return status
        if isinstance(status, Exception):
            raise status
        if self.snapshot:
            return httpx.Response(200, json=_snapshot_json(*status))
        return httpx.Response(200, json=_sandbox_json(status))


@pytest.fixture(params=["async", "sync"])
def make_client(request):
    def make(handler):
        internal = AuthenticatedClient(
            base_url="https://api.test/v1",
            token="test-token",
            httpx_args={"transport": httpx.MockTransport(handler)},
        )
        cls = SandboxClient if request.param == "async" else SyncSandboxClient
        return cls(internal, default_owner_id="tea-test")

    return make


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


class _Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps: list[float] = []

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


@pytest.fixture
def clock(monkeypatch):
    fake = _Clock()

    async def asleep(seconds):
        fake.sleep(seconds)

    monkeypatch.setattr(_wait, "monotonic", lambda: fake.now)
    monkeypatch.setattr(_wait, "asleep", asleep)
    monkeypatch.setattr(_wait, "sleep", fake.sleep)
    return fake


@pytest.mark.asyncio
async def test_wait_until_running_polls_until_the_sandbox_runs(make_client, clock):
    api = _Api("creating", "resuming", "running")
    client = make_client(api)

    sandbox = await _resolve(client.wait_until_running("sbx-abc", owner_id="tea-x"))

    assert sandbox.status == "running"
    assert len(api.gets) == 3
    assert api.gets[0].url.params["ownerId"] == "tea-x"
    assert clock.sleeps == [0.25, 0.5]


# Doubling from 250 ms keeps short waits fast while a slow one stays under the
# API rate limit.
@pytest.mark.asyncio
async def test_doubles_the_interval_up_to_2_seconds(make_client, clock):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxWaitTimeoutError):
        await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=10))

    assert clock.sleeps == [0.25, 0.5, 1.0, 2.0, 2.0, 2.0, 2.0, 0.25]


@pytest.mark.asyncio
async def test_keeps_a_fixed_interval_longer_than_2_seconds(make_client, clock):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxWaitTimeoutError):
        await _resolve(
            client.wait_until_running("sbx-abc", timeout_seconds=12, interval_seconds=5)
        )

    assert clock.sleeps == [5, 5, 2]


# A sandbox that errored or was suspended never becomes running, so waiting out
# the timeout would only delay the failure.
@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["errored", "terminated", "suspending", "suspended"])
async def test_raises_as_soon_as_the_sandbox_cant_run(make_client, clock, status):
    api = _Api(status)
    client = make_client(api)

    with pytest.raises(SandboxNotRunningError) as excinfo:
        await _resolve(client.wait_until_running("sbx-abc"))

    assert str(excinfo.value) == f"sandbox sbx-abc is {status}, not running"
    assert excinfo.value.sandbox_id == "sbx-abc"
    assert excinfo.value.sandbox_status == status
    assert len(api.gets) == 1


@pytest.mark.asyncio
async def test_times_out_with_the_sandbox_id_and_last_status(make_client, clock):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxWaitTimeoutError) as excinfo:
        await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=1))

    error = excinfo.value
    assert isinstance(error, TimeoutError)
    assert error.sandbox_id == "sbx-abc"
    assert error.timeout_seconds == 1
    assert error.last_status == "creating"
    assert clock.now == pytest.approx(1)


# Matches the CLI's `sandboxes create --wait`.
@pytest.mark.asyncio
async def test_times_out_after_60_seconds_by_default(make_client, clock):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxWaitTimeoutError) as excinfo:
        await _resolve(client.wait_until_running("sbx-abc"))

    assert excinfo.value.timeout_seconds == 60
    assert clock.now == pytest.approx(60)


@pytest.mark.asyncio
async def test_a_zero_timeout_is_an_immediate_deadline(make_client, clock):
    api = _Api("running")
    client = make_client(api)

    with pytest.raises(SandboxWaitTimeoutError) as excinfo:
        await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=0))

    assert excinfo.value.last_status is None
    assert api.requests == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "options",
    [
        {"timeout_seconds": -1},
        {"timeout_seconds": float("nan")},
        {"timeout_seconds": float("inf")},
        {"interval_seconds": 0},
        {"interval_seconds": -1},
        {"interval_seconds": float("nan")},
        {"interval_seconds": float("inf")},
    ],
)
async def test_rejects_invalid_options_without_a_request(make_client, options):
    api = _Api("running")
    client = make_client(api)

    with pytest.raises(ValueError):
        await _resolve(client.wait_until_running("sbx-abc", **options))
    with pytest.raises(ValueError):
        await _resolve(client.create(wait=SandboxWaitOptions(**options)))

    assert api.requests == []


def _late(clock, *statuses):
    """A handler whose status checks each return after the deadline has passed."""
    queue = list(statuses)

    def handler(request):
        if request.method == "POST":
            return httpx.Response(201, json=_sandbox_json("creating"))
        clock.now += 2
        return httpx.Response(200, json=_sandbox_json(queue.pop(0)))

    return handler


# Timing out here would tell create(wait=...) callers to terminate a sandbox
# that just started.
@pytest.mark.asyncio
async def test_a_late_check_that_finds_the_sandbox_running_returns_it(
    make_client, clock
):
    client = make_client(_late(clock, "running"))

    sandbox = await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=1))

    assert sandbox.status == "running"


@pytest.mark.asyncio
async def test_create_with_wait_returns_a_sandbox_that_runs_just_past_the_deadline(
    make_client, clock
):
    client = make_client(_late(clock, "running"))

    sandbox = await _resolve(client.create(wait=SandboxWaitOptions(timeout_seconds=1)))

    assert sandbox.status == "running"


@pytest.mark.asyncio
async def test_a_late_check_that_finds_the_sandbox_errored_says_so(make_client, clock):
    client = make_client(_late(clock, "errored"))

    with pytest.raises(SandboxNotRunningError):
        await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=1))


@pytest.mark.asyncio
async def test_a_late_check_that_finds_the_sandbox_creating_times_out(
    make_client, clock
):
    api_calls = []

    def handler(request):
        api_calls.append(request)
        return _late(clock, "creating")(request)

    client = make_client(handler)

    with pytest.raises(SandboxWaitTimeoutError) as excinfo:
        await _resolve(client.wait_until_running("sbx-abc", timeout_seconds=1))

    assert excinfo.value.last_status == "creating"
    assert len(api_calls) == 1


@pytest.mark.asyncio
async def test_the_async_deadline_cancels_a_status_check_that_hangs():
    async def handler(request):
        await asyncio.sleep(60)

    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    client = SandboxClient(internal, default_owner_id="tea-test")

    with pytest.raises(SandboxWaitTimeoutError) as excinfo:
        await asyncio.wait_for(
            client.wait_until_running("sbx-abc", timeout_seconds=0.05), 5
        )

    assert excinfo.value.last_status is None


@pytest.mark.asyncio
async def test_status_check_errors_propagate_unchanged(make_client, clock):
    client = make_client(_Api(httpx.Response(404, json={"message": "not found"})))

    with pytest.raises(SandboxNotFoundError):
        await _resolve(client.wait_until_running("sbx-abc"))


@pytest.mark.asyncio
async def test_wait_until_available_polls_until_the_snapshot_is_available(
    make_client, clock
):
    api = _Api(("creating",), ("available",), snapshot=True)
    client = make_client(api)

    snapshot = await _resolve(
        client.snapshots.wait_until_available(
            sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
        )
    )

    assert snapshot.status == "available"
    assert api.gets[0].url.path == "/v1/sandbox-groups/sbg-abc/snapshots/snp-abc"
    assert len(api.gets) == 2


@pytest.mark.asyncio
async def test_wait_until_available_raises_with_the_reason_a_capture_failed(
    make_client, clock
):
    client = make_client(_Api(("failed", "capture timed out"), snapshot=True))

    with pytest.raises(SnapshotFailedError) as excinfo:
        await _resolve(
            client.snapshots.wait_until_available(
                sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
            )
        )

    assert str(excinfo.value) == "snapshot snp-abc failed to capture: capture timed out"
    assert excinfo.value.snapshot_id == "snp-abc"
    assert excinfo.value.snapshot_error == "capture timed out"


@pytest.mark.asyncio
async def test_wait_until_available_times_out_after_5_minutes_by_default(
    make_client, clock
):
    client = make_client(_Api(("creating",), snapshot=True))

    with pytest.raises(SnapshotWaitTimeoutError) as excinfo:
        await _resolve(
            client.snapshots.wait_until_available(
                sandbox_group_id="sbg-abc", snapshot_id="snp-abc"
            )
        )

    error = excinfo.value
    assert isinstance(error, TimeoutError)
    assert error.snapshot_id == "snp-abc"
    assert error.timeout_seconds == 300
    assert error.last_status == "creating"
    assert clock.now == pytest.approx(300)


@pytest.mark.asyncio
async def test_create_without_wait_returns_without_polling(make_client):
    api = _Api("running")
    client = make_client(api)

    sandbox = await _resolve(client.create())

    assert sandbox.status == "creating"
    assert api.gets == []


@pytest.mark.asyncio
async def test_create_with_wait_polls_and_keeps_wait_out_of_the_body(
    make_client, clock
):
    api = _Api("creating", "running")
    client = make_client(api)

    sandbox = await _resolve(client.create(owner_id="tea-x", wait=True))

    assert sandbox.status == "running"
    body = json.loads(api.requests[0].content)
    assert body["ownerId"] == "tea-x"
    assert not any("wait" in key.lower() for key in body)
    assert len(api.gets) == 2
    assert api.gets[0].url.params["ownerId"] == "tea-x"


@pytest.mark.asyncio
async def test_create_with_wait_skips_polling_when_already_running(make_client):
    api = _Api("running", created="running")
    client = make_client(api)

    sandbox = await _resolve(client.create(wait=True))

    assert sandbox.status == "running"
    assert api.gets == []


@pytest.mark.asyncio
async def test_create_with_wait_passes_options_through(make_client, clock):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxCreateWaitError) as excinfo:
        await _resolve(
            client.create(
                wait=SandboxWaitOptions(timeout_seconds=5, interval_seconds=1)
            )
        )

    cause = excinfo.value.cause
    assert isinstance(cause, SandboxWaitTimeoutError)
    assert cause.timeout_seconds == 5
    assert clock.sleeps[:3] == [1, 2, 2]


@pytest.mark.asyncio
async def test_create_with_wait_wraps_a_sandbox_that_comes_back_errored(
    make_client,
):
    api = _Api("running", created="errored")
    client = make_client(api)

    with pytest.raises(SandboxCreateWaitError) as excinfo:
        await _resolve(client.create(wait=True))

    error = excinfo.value
    assert str(error) == (
        "created sandbox sbx-abc, but it is not running: "
        "sandbox sbx-abc is errored, not running"
    )
    assert error.sandbox_id == "sbx-abc"
    assert isinstance(error.cause, SandboxNotRunningError)
    assert error.__cause__ is error.cause
    assert api.gets == []


# Without the id, the caller can't terminate a sandbox it is billed for.
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("polled", "cause"),
    [
        (lambda: httpx.Response(503, json={"message": "unavailable"}), ServerError),
        (
            lambda: httpx.Response(404, json={"message": "not found"}),
            SandboxNotFoundError,
        ),
        (lambda: httpx.ConnectError("connection refused"), RenderError),
        (lambda: httpx.Response(200, content=b"not json"), RenderError),
        (lambda: "suspended", SandboxNotRunningError),
    ],
    ids=["5xx", "404", "connection", "non-json", "suspended"],
)
async def test_create_with_wait_gives_the_id_when_the_wait_fails(
    make_client, clock, polled, cause
):
    # Built per test: a response is consumed once read.
    client = make_client(_Api(polled()))

    with pytest.raises(SandboxCreateWaitError) as excinfo:
        await _resolve(client.create(wait=True))

    assert excinfo.value.sandbox_id == "sbx-abc"
    assert isinstance(excinfo.value.cause, cause)


# Wrapping CancelledError would break asyncio's cancellation.
@pytest.mark.asyncio
async def test_create_with_wait_lets_cancellation_through():
    async def handler(request):
        if request.method == "POST":
            return httpx.Response(201, json=_sandbox_json("creating"))
        await asyncio.sleep(60)

    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    client = SandboxClient(internal, default_owner_id="tea-test")
    task = asyncio.ensure_future(client.create(wait=True))
    await asyncio.sleep(0.01)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_a_wait_options_timeout_of_none_uses_the_sandbox_default(
    make_client, clock
):
    client = make_client(_Api("creating"))

    with pytest.raises(SandboxCreateWaitError) as excinfo:
        await _resolve(client.create(wait=SandboxWaitOptions(interval_seconds=1)))

    assert excinfo.value.cause.timeout_seconds == 60
    assert clock.now == pytest.approx(60)


def _snapshot_api(*polled, created=("creating",)):
    return _Api(*polled, created=created, snapshot=True)


@pytest.mark.asyncio
async def test_snapshot_create_without_wait_returns_without_polling(make_client):
    api = _snapshot_api(("available",))
    client = make_client(api)

    snapshot = await _resolve(client.snapshots.create("sbx-abc"))

    assert snapshot.status == "creating"
    assert api.gets == []


@pytest.mark.asyncio
async def test_snapshot_create_with_wait_polls_the_new_snapshot(make_client, clock):
    api = _snapshot_api(("creating",), ("available",))
    client = make_client(api)

    snapshot = await _resolve(
        client.snapshots.create("sbx-abc", name="gold", owner_id="tea-x", wait=True)
    )

    assert snapshot.status == "available"
    body = json.loads(api.requests[0].content)
    assert not any("wait" in key.lower() for key in body)
    assert len(api.gets) == 2
    assert api.gets[0].url.path == "/v1/sandbox-groups/sbg-abc/snapshots/snp-abc"
    assert api.gets[0].url.params["ownerId"] == "tea-x"


@pytest.mark.asyncio
async def test_snapshot_create_with_wait_skips_polling_when_already_available(
    make_client,
):
    api = _snapshot_api(("available",), created=("available",))
    client = make_client(api)

    snapshot = await _resolve(client.snapshots.create("sbx-abc", wait=True))

    assert snapshot.status == "available"
    assert api.gets == []


# Matches the CLI's `sandboxes snapshots create --wait`.
@pytest.mark.asyncio
async def test_snapshot_create_with_wait_times_out_after_5_minutes_by_default(
    make_client, clock
):
    client = make_client(_snapshot_api(("creating",)))

    with pytest.raises(SnapshotCreateWaitError) as excinfo:
        await _resolve(client.snapshots.create("sbx-abc", wait=True))

    cause = excinfo.value.cause
    assert isinstance(cause, SnapshotWaitTimeoutError)
    assert cause.timeout_seconds == 300
    assert cause.last_status == "creating"
    assert clock.now == pytest.approx(300)


@pytest.mark.asyncio
async def test_snapshot_create_with_wait_gives_both_ids_when_the_capture_fails(
    make_client,
):
    api = _snapshot_api(("available",), created=("failed", "capture timed out"))
    client = make_client(api)

    with pytest.raises(SnapshotCreateWaitError) as excinfo:
        await _resolve(client.snapshots.create("sbx-abc", wait=True))

    error = excinfo.value
    assert str(error) == (
        "created snapshot snp-abc, but it is not available: "
        "snapshot snp-abc failed to capture: capture timed out"
    )
    assert error.snapshot_id == "snp-abc"
    assert error.sandbox_group_id == "sbg-abc"
    assert isinstance(error.cause, SnapshotFailedError)
    assert error.__cause__ is error.cause
    assert api.gets == []


# Without the ids, the caller can't delete a snapshot it didn't want.
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("polled", "cause"),
    [
        (lambda: httpx.Response(503, json={"message": "unavailable"}), ServerError),
        (lambda: httpx.ConnectError("connection refused"), RenderError),
    ],
    ids=["5xx", "connection"],
)
async def test_snapshot_create_with_wait_gives_both_ids_when_the_wait_fails(
    make_client, clock, polled, cause
):
    client = make_client(_snapshot_api(polled()))

    with pytest.raises(SnapshotCreateWaitError) as excinfo:
        await _resolve(client.snapshots.create("sbx-abc", wait=True))

    assert excinfo.value.snapshot_id == "snp-abc"
    assert excinfo.value.sandbox_group_id == "sbg-abc"
    assert isinstance(excinfo.value.cause, cause)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "options",
    [{"timeout_seconds": -1}, {"interval_seconds": 0}],
)
async def test_snapshot_create_rejects_bad_wait_options_without_a_request(
    make_client, options
):
    api = _snapshot_api(("available",), created=("available",))
    client = make_client(api)

    with pytest.raises(ValueError):
        await _resolve(
            client.snapshots.create("sbx-abc", wait=SandboxWaitOptions(**options))
        )

    assert api.requests == []
