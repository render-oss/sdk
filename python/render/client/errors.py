class RenderError(Exception):
    """Base exception for all Render errors."""

    pass


class ClientError(RenderError):
    """Exception for client errors. This is returned when
    the client makes a request to the API and the API returns a 4xx error.

    code is the machine-readable code from the error body, or None when the
    API did not send one."""

    def __init__(self, *args: object, code: str | None = None) -> None:
        super().__init__(*args)
        self.code = code


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
