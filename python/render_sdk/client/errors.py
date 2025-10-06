class RenderError(Exception):
    """Base exception for all Render errors."""

    pass


class ClientError(RenderError):
    """Exception for client errors. This is returned when
    the client makes a request to the API and the API returns a 4xx error."""

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
