"""Polling a sandbox, snapshot, or image until it is ready.

The async and sync clients share this module, and unasync leaves it alone.
apoll_until and poll_until live here for the same reason as
files.arun_blocking: a transformed module can't hold both.
"""

from __future__ import annotations

import asyncio
import math
import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, NamedTuple, TypeVar

from render.experimental.sandbox.errors import (
    ImageFailedError,
    SandboxNotRunningError,
    SnapshotFailedError,
)

if TYPE_CHECKING:
    from render.experimental.sandbox.types import (
        Image,
        Sandbox,
        SandboxWaitOptions,
        Snapshot,
    )

# Matches the CLI's `sandboxes create --wait`.
DEFAULT_SANDBOX_TIMEOUT_SECONDS = 60.0
DEFAULT_SNAPSHOT_TIMEOUT_SECONDS = 300.0
# Matches the CLI's `sandbox-groups images import --wait`.
DEFAULT_IMAGE_TIMEOUT_SECONDS = 600.0
DEFAULT_INTERVAL_SECONDS = 0.25
# The longest delay between checks once the backoff has grown.
MAX_BACKOFF_INTERVAL_SECONDS = 2.0

_T = TypeVar("_T")
_R = TypeVar("_R")


def monotonic() -> float:
    return time.monotonic()


async def asleep(seconds: float) -> None:
    await asyncio.sleep(seconds)


def sleep(seconds: float) -> None:
    time.sleep(seconds)


def validate(timeout_seconds: float, interval_seconds: float) -> None:
    if not math.isfinite(timeout_seconds) or timeout_seconds < 0:
        raise ValueError("timeout_seconds must be a finite number of at least 0")
    if not math.isfinite(interval_seconds) or interval_seconds <= 0:
        raise ValueError("interval_seconds must be a positive finite number")


class WaitSettings(NamedTuple):
    timeout_seconds: float
    interval_seconds: float


def resolve_create_wait(
    wait: bool | SandboxWaitOptions, default_timeout_seconds: float
) -> WaitSettings | None:
    """Fill in the defaults for a create(wait=...), or return None if not waiting.

    Raise ValueError for bad options. Call it before the create request, so bad
    options create nothing.
    """
    if wait is False:
        return None
    timeout_seconds = default_timeout_seconds
    interval_seconds = DEFAULT_INTERVAL_SECONDS
    if wait is not True:
        if wait.timeout_seconds is not None:
            timeout_seconds = wait.timeout_seconds
        interval_seconds = wait.interval_seconds
    validate(timeout_seconds, interval_seconds)
    return WaitSettings(timeout_seconds, interval_seconds)


def running_sandbox(sandbox: Sandbox) -> Sandbox | None:
    """Return the sandbox if it is running, or None if it may still get there.

    Raise SandboxNotRunningError if it can't.
    """
    if sandbox.status == "running":
        return sandbox
    if sandbox.status in ("creating", "resuming"):
        return None
    raise SandboxNotRunningError(
        f"sandbox {sandbox.id} is {sandbox.status}, not running",
        sandbox_id=sandbox.id,
        sandbox_status=sandbox.status,
    )


def available_snapshot(snapshot: Snapshot) -> Snapshot | None:
    """Return the snapshot if it is available, or None if it is still creating.

    Raise SnapshotFailedError if its capture failed.
    """
    if snapshot.status == "available":
        return snapshot
    if snapshot.status == "failed":
        reason = f": {snapshot.error}" if snapshot.error else ""
        raise SnapshotFailedError(
            f"snapshot {snapshot.id} failed to capture{reason}",
            snapshot_id=snapshot.id,
            snapshot_error=snapshot.error,
        )
    return None


def ready_image(image: Image) -> Image | None:
    """Return the image if it has succeeded, or None if its import is pending or running.

    Raise ImageFailedError if the import failed.
    """
    if image.status == "succeeded":
        return image
    if image.status == "failed":
        reason = f": {image.failure_reason}" if image.failure_reason else ""
        raise ImageFailedError(
            f"image {image.id} failed to import{reason}",
            image_id=image.id,
            failure_reason=image.failure_reason,
        )
    return None


class _Schedule:
    """The deadline and backoff for one wait."""

    def __init__(self, timeout_seconds: float, interval_seconds: float) -> None:
        validate(timeout_seconds, interval_seconds)
        self._deadline = monotonic() + timeout_seconds
        self._interval = interval_seconds
        self._max_interval = max(interval_seconds, MAX_BACKOFF_INTERVAL_SECONDS)

    def remaining(self) -> float:
        return self._deadline - monotonic()

    def next_delay(self) -> float:
        """Return the delay before the next check, and double the one after."""
        delay = min(self._interval, max(self.remaining(), 0.0))
        self._interval = min(self._interval * 2, self._max_interval)
        return delay


async def apoll_until(
    load: Callable[[], Awaitable[_T]],
    check: Callable[[_T], _R | None],
    *,
    timeout_seconds: float,
    interval_seconds: float,
    timeout_error: Callable[[_T | None], Exception],
) -> _R:
    """Call load until check returns a value, or raises because it never will.

    The deadline also bounds each load, which is cancelled when it runs out.
    """
    schedule = _Schedule(timeout_seconds, interval_seconds)
    last: _T | None = None
    while True:
        remaining = schedule.remaining()
        if remaining <= 0:
            raise timeout_error(last)
        try:
            value = await asyncio.wait_for(load(), remaining)
        except asyncio.TimeoutError:
            raise timeout_error(last) from None
        last = value
        # Check the status before the deadline, so a resource that is ready by
        # the time a late check returns is returned, not discarded.
        result = check(value)
        if result is not None:
            return result
        if schedule.remaining() <= 0:
            raise timeout_error(last)
        await asleep(schedule.next_delay())


def poll_until(
    load: Callable[[], _T],
    check: Callable[[_T], _R | None],
    *,
    timeout_seconds: float,
    interval_seconds: float,
    timeout_error: Callable[[_T | None], Exception],
) -> _R:
    """Call load until check returns a value, or raises because it never will.

    A blocking load can't be cancelled, so one already running when the
    deadline passes finishes first, within the HTTP client's own timeout.
    """
    schedule = _Schedule(timeout_seconds, interval_seconds)
    last: _T | None = None
    while True:
        if schedule.remaining() <= 0:
            raise timeout_error(last)
        value = load()
        last = value
        # Check the status before the deadline, so a resource that is ready by
        # the time a late check returns is returned, not discarded.
        result = check(value)
        if result is not None:
            return result
        if schedule.remaining() <= 0:
            raise timeout_error(last)
        sleep(schedule.next_delay())
