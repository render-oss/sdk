"""Unit tests for waiting on a flow run to finish."""

import asyncio
from typing import Any

import pytest

from render.client import _flow_wait
from render.client.errors import (
    ClientError,
    FlowRunError,
    RateLimitError,
    ServerError,
    TimeoutError,
)
from render.public_api.models.flow_run_details import FlowRunDetails
from render.public_api.models.flow_run_status import FlowRunStatus


def new_details(status: FlowRunStatus, **overrides) -> FlowRunDetails:
    """Build a FlowRunDetails, overriding only the fields a test cares about."""
    fields: dict[str, Any] = {
        "id": "frn-test123",
        "flow_id": "flw-test123",
        "status": status,
        "input_": [42],
        "results": [],
        "attempts": [],
    }
    fields.update(overrides)
    return FlowRunDetails(**fields)


class FakeSleep:
    """Records each delay instead of sleeping."""

    def __init__(self):
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)

    async def asleep(self, seconds: float) -> None:
        self(seconds)


class FakeLoad:
    """Returns, or raises, each queued outcome in turn. The last one repeats."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def __call__(self) -> FlowRunDetails:
        self.calls += 1
        outcome = self.outcomes.pop(0) if len(self.outcomes) > 1 else self.outcomes[0]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    async def aload(self) -> FlowRunDetails:
        return self()


def wait(mode: str, load: FakeLoad, sleep: FakeSleep) -> FlowRunDetails:
    """Run the async or sync wait with fake sleeps."""
    if mode == "async":
        return asyncio.run(_flow_wait.await_flow_run(load.aload, sleep=sleep.asleep))
    return _flow_wait.wait_flow_run(load, sleep=sleep)


modes = pytest.mark.parametrize("mode", ["async", "sync"])

RUNNING = new_details(FlowRunStatus.RUNNING)
PAUSED = new_details(FlowRunStatus.PAUSED)
SUCCEEDED = new_details(FlowRunStatus.SUCCEEDED, results=[84])


@modes
def test_polls_with_backoff_until_the_run_finishes(mode):
    sleep = FakeSleep()
    load = FakeLoad(RUNNING, PAUSED, RUNNING, SUCCEEDED)

    result = wait(mode, load, sleep)

    assert result is SUCCEEDED
    assert load.calls == 4
    assert sleep.delays == [1, 2, 4]


@modes
def test_returns_a_run_that_has_already_finished_without_sleeping(mode):
    sleep = FakeSleep()

    result = wait(mode, FakeLoad(SUCCEEDED), sleep)

    assert result is SUCCEEDED
    assert sleep.delays == []


@modes
@pytest.mark.parametrize(
    "finished,message",
    [
        (
            new_details(FlowRunStatus.FAILED, error="boom"),
            "flow run frn-test123 failed: boom",
        ),
        (new_details(FlowRunStatus.FAILED), "flow run frn-test123 failed"),
        (new_details(FlowRunStatus.CANCELED), "flow run frn-test123 was canceled"),
    ],
)
def test_raises_when_the_run_fails_or_is_canceled(mode, finished, message):
    load = FakeLoad(RUNNING, finished)

    with pytest.raises(FlowRunError, match=f"^{message}$") as exc_info:
        wait(mode, load, FakeSleep())

    assert exc_info.value.flow_run_id == "frn-test123"
    assert exc_info.value.details is finished


@modes
def test_retries_transient_errors_with_backoff(mode):
    sleep = FakeSleep()
    load = FakeLoad(
        ServerError("down"),
        RateLimitError("busy", status_code=429),
        TimeoutError("slow"),
        ClientError("request timeout", status_code=408),
        SUCCEEDED,
    )

    result = wait(mode, load, sleep)

    assert result is SUCCEEDED
    assert sleep.delays == [1, 2, 4, 8]


@modes
def test_raises_a_client_error_without_retrying(mode):
    load = FakeLoad(ClientError("not found", status_code=404))

    with pytest.raises(ClientError):
        wait(mode, load, FakeSleep())

    assert load.calls == 1


@modes
def test_raises_the_last_of_5_transient_errors_in_a_row(mode):
    load = FakeLoad(ServerError("down"))

    with pytest.raises(ServerError):
        wait(mode, load, FakeSleep())

    assert load.calls == 5
