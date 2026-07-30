"""Sandbox-specific exceptions."""

from render_sdk.client.errors import ClientError, RenderError


class SandboxNotFoundError(ClientError):
    """Raised when a sandbox does not exist or is no longer retrievable."""


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
