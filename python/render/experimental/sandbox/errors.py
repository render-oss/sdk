"""Sandbox-specific exceptions."""

from render.client.errors import ClientError, RenderError


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
