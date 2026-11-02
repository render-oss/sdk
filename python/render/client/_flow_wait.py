"""Waiting for a flow run to finish.

The async and sync workflows clients share this module. A wait checks the
flow run's status with exponential backoff until the run succeeds, fails, or
is canceled. FlowRunWaiter decides what each check means, so the async and
sync loops only load and sleep.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable

from render.client.errors import (
    ClientError,
    FlowRunError,
    RateLimitError,
    RenderError,
    ServerError,
    TimeoutError,
)
from render.client.types import FlowRunDetails, FlowRunStatus

# The first delay between checks. It doubles after each check.
INITIAL_INTERVAL_SECONDS = 1.0
# The longest delay between checks once the backoff has grown.
MAX_INTERVAL_SECONDS = 60.0
# How many checks in a row can fail with a transient error before the wait
# gives up and raises the last one.
MAX_CONSECUTIVE_ERRORS = 5


def finished_flow_run(details: FlowRunDetails) -> FlowRunDetails | None:
    """Return the details if the flow run succeeded, or None if it may still run.

    Raise FlowRunError if it failed or was canceled.
    """
    if details.status in (FlowRunStatus.FAILED, FlowRunStatus.CANCELED):
        outcome = "failed" if details.status == FlowRunStatus.FAILED else "was canceled"
        reason = f": {details.error}" if details.error else ""
        raise FlowRunError(
            f"flow run {details.id} {outcome}{reason}",
            flow_run_id=details.id,
            details=details,
        )
    if details.status == FlowRunStatus.SUCCEEDED:
        return details
    return None


def is_transient(exc: Exception) -> bool:
    """Return whether a status check that raised exc is worth trying again."""
    if isinstance(exc, ClientError) and exc.status_code == 408:
        return True
    return isinstance(exc, (ServerError, TimeoutError, RateLimitError))


class FlowRunWaiter:
    """The backoff and error count of one wait."""

    def __init__(self) -> None:
        self._interval = INITIAL_INTERVAL_SECONDS
        self._errors = 0

    def checked(self, details: FlowRunDetails) -> FlowRunDetails | None:
        """Record a status check. Return the details if the flow run succeeded.

        Raise FlowRunError if it failed or was canceled.
        """
        self._errors = 0
        return finished_flow_run(details)

    def should_retry(self, exc: Exception) -> bool:
        """Record a status check that raised exc, and return whether to check again."""
        self._errors += 1
        return is_transient(exc) and self._errors < MAX_CONSECUTIVE_ERRORS

    def next_delay(self) -> float:
        """Return the delay before the next check, and double the one after."""
        delay = self._interval
        self._interval = min(self._interval * 2, MAX_INTERVAL_SECONDS)
        return delay


async def await_flow_run(
    load: Callable[[], Awaitable[FlowRunDetails]],
    *,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> FlowRunDetails:
    """Call load until the flow run it returns finishes."""
    waiter = FlowRunWaiter()
    while True:
        try:
            details = await load()
        except RenderError as exc:
            if not waiter.should_retry(exc):
                raise
        else:
            finished = waiter.checked(details)
            if finished is not None:
                return finished
        await sleep(waiter.next_delay())


def wait_flow_run(
    load: Callable[[], FlowRunDetails],
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> FlowRunDetails:
    """Call load until the flow run it returns finishes."""
    waiter = FlowRunWaiter()
    while True:
        try:
            details = load()
        except RenderError as exc:
            if not waiter.should_retry(exc):
                raise
        else:
            finished = waiter.checked(details)
            if finished is not None:
                return finished
        sleep(waiter.next_delay())
