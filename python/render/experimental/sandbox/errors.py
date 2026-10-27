"""Sandbox-specific exceptions."""

from render.client.errors import ClientError, RenderError
from render.client.errors import TimeoutError as RenderTimeoutError


class SandboxNotFoundError(ClientError):
    """Raised when a sandbox does not exist or is no longer retrievable."""


class SandboxFileNotFoundError(ClientError):
    """Raised when a file operation names a path the sandbox does not have.

    Distinct from SandboxNotFoundError: the sandbox is alive, the path is not.
    """


class SnapshotNotFoundError(ClientError):
    """Raised when a snapshot does not exist, was deleted, has expired, or belongs
    to another sandbox group."""


class SnapshotNotReadyError(ClientError):
    """Raised when a snapshot is still creating (on delete) or is not available
    to start a sandbox from (on create with snapshot_id). code is
    snapshot_creating or snapshot_not_available."""


class SnapshotPlanMismatchError(ClientError):
    """Raised when a sandbox create names a runtime source snapshot captured on
    a different plan. code is snapshot_plan_mismatch."""


class ImageNotFoundError(ClientError):
    """Raised when an image does not exist or belongs to another sandbox group."""


class ImageNotReadyError(ClientError):
    """Raised when a sandbox create names an image that has not succeeded, whether
    still in progress or failed."""


# Deprecated aliases from when images were called builds.
BuildNotFoundError = ImageNotFoundError
BuildNotReadyError = ImageNotReadyError


class SandboxDownloadError(RenderError):
    """Raised when a download cannot be written to disk safely: a truncated
    archive, an entry that escapes the destination, or a response encoding the
    SDK cannot decode."""


class SandboxExecError(RenderError):
    """Raised when an exec stream ends abnormally: no terminal event, an
    unknown event type, or unparseable event data."""


class SandboxExecStreamError(RenderError):
    """Raised when an exec stream delivers a terminal error event.

    Carries the in-stream status and message reported by the sandbox.
    """

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class SandboxNotRunningError(RenderError):
    """Raised while waiting for a sandbox to be running when it reaches a status
    it can't run from: errored, terminated, suspending, or suspended. The
    sandbox is left as it is."""

    def __init__(self, message: str, *, sandbox_id: str, sandbox_status: str) -> None:
        super().__init__(message)
        self.sandbox_id = sandbox_id
        self.sandbox_status = sandbox_status


class SnapshotFailedError(RenderError):
    """Raised while waiting for a snapshot to be available when its capture
    fails. snapshot_error is the reason the API reports, if any."""

    def __init__(
        self, message: str, *, snapshot_id: str, snapshot_error: str | None
    ) -> None:
        super().__init__(message)
        self.snapshot_id = snapshot_id
        self.snapshot_error = snapshot_error


class ImageFailedError(RenderError):
    """Raised while waiting for an image to be ready when its import fails.
    failure_reason is the reason the API reports, if any."""

    def __init__(
        self, message: str, *, image_id: str, failure_reason: str | None
    ) -> None:
        super().__init__(message)
        self.image_id = image_id
        self.failure_reason = failure_reason


class SandboxWaitTimeoutError(RenderTimeoutError):
    """Raised when a sandbox is not running before the wait times out.

    The sandbox is left as it is and may still become running. last_status is
    None if no status check finished in time.
    """

    def __init__(
        self,
        message: str,
        *,
        sandbox_id: str,
        timeout_seconds: float,
        last_status: str | None,
    ) -> None:
        super().__init__(message)
        self.sandbox_id = sandbox_id
        self.timeout_seconds = timeout_seconds
        self.last_status = last_status


class SnapshotWaitTimeoutError(RenderTimeoutError):
    """Raised when a snapshot is not available before the wait times out.

    It may still become available. last_status is None if no status check
    finished in time.
    """

    def __init__(
        self,
        message: str,
        *,
        snapshot_id: str,
        timeout_seconds: float,
        last_status: str | None,
    ) -> None:
        super().__init__(message)
        self.snapshot_id = snapshot_id
        self.timeout_seconds = timeout_seconds
        self.last_status = last_status


class ImageWaitTimeoutError(RenderTimeoutError):
    """Raised when an image is not ready before the wait times out.

    The import keeps running and may still succeed. last_status is None if no
    status check finished in time.
    """

    def __init__(
        self,
        message: str,
        *,
        image_id: str,
        timeout_seconds: float,
        last_status: str | None,
    ) -> None:
        super().__init__(message)
        self.image_id = image_id
        self.timeout_seconds = timeout_seconds
        self.last_status = last_status


class SandboxCreateWaitError(RenderError):
    """Raised by create(wait=...) when it created the sandbox but the wait for it
    to be running failed.

    The sandbox still exists and is billed until it ends, so call
    terminate(sandbox_id) if you don't want it. cause, also set as __cause__, is
    the error the wait raised, such as SandboxNotRunningError,
    SandboxWaitTimeoutError, or a request error.

    Cancelling the task or interrupting the process is not wrapped, because
    that would break cancellation. That includes the timeout of
    asyncio.wait_for, so bound the wait with
    SandboxWaitOptions(timeout_seconds=...) instead. To keep the id through a
    cancel, call create without wait and then wait_until_running.
    """

    def __init__(self, message: str, *, sandbox_id: str, cause: Exception) -> None:
        super().__init__(message)
        self.sandbox_id = sandbox_id
        self.cause = cause


class SnapshotCreateWaitError(RenderError):
    """Raised by snapshots.create(wait=...) when it created the snapshot but the
    wait for it to be available failed.

    The snapshot still exists, so delete it with snapshot_id and
    sandbox_group_id if you don't want it. Deleting raises SnapshotNotReadyError
    while the capture is still running. cause, also set as __cause__, is the
    error the wait raised, such as SnapshotFailedError,
    SnapshotWaitTimeoutError, or a request error. Cancelling the task or
    interrupting the process is not wrapped, and that includes the timeout of
    asyncio.wait_for, so bound the wait with
    SandboxWaitOptions(timeout_seconds=...) instead.
    """

    def __init__(
        self,
        message: str,
        *,
        snapshot_id: str,
        sandbox_group_id: str,
        cause: Exception,
    ) -> None:
        super().__init__(message)
        self.snapshot_id = snapshot_id
        self.sandbox_group_id = sandbox_group_id
        self.cause = cause
