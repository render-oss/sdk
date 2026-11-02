from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render.client.types import FlowRunDetails


class RenderError(Exception):
    """Base exception for all Render errors."""

    pass


class ClientError(RenderError):
    """Exception for client errors. This is returned when
    the client makes a request to the API and the API returns a 4xx error.

    code is the machine-readable code from the error body, or None when the
    API did not send one. status_code is the HTTP status, or None when the
    error did not come from an HTTP response."""

    def __init__(
        self,
        *args: object,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(*args)
        self.code = code
        self.status_code = status_code


class RateLimitError(ClientError):
    """Exception for rate limit errors. This is returned when
    the client makes a request to the API and the API returns a 429 error."""

    pass


class TimeoutError(RenderError):
    """Exception for timeout errors. This is returned when the
    client makes a request to the API and the request times out."""

    pass


class ServerError(RenderError):
    """Exception for server errors. This is returned when the
    client makes a request to the API and the API returns a 5xx error."""

    pass


class TaskRunError(RenderError):
    """Exception for task run errors. This is returned when a running
    task fails."""

    pass


class FlowRunError(RenderError):
    """Exception for flow run errors. This is raised when a flow run
    being waited on fails or is canceled.

    flow_run_id is the ID of the flow run, and details are its final details,
    whose status says whether it failed or was canceled."""

    def __init__(
        self,
        *args: object,
        flow_run_id: str | None = None,
        details: "FlowRunDetails | None" = None,
    ) -> None:
        super().__init__(*args)
        self.flow_run_id = flow_run_id
        self.details = details
