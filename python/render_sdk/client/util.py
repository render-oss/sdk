import functools
import logging
from asyncio import sleep
from collections.abc import Awaitable, Callable
from typing import Any, NoReturn

import httpx

from render_sdk.client.errors import ClientError, RenderError, ServerError, TimeoutError
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.types import Response, Unset

logger = logging.getLogger(__name__)


async def retry_with_backoff(
    fn: Callable[[], Awaitable[Any]],
    max_retries: int = 5,
    poll_interval: float = 1.0,
    backoff_factor: float = 2.0,
    exempted_exceptions: tuple[type[Exception], ...] = (),
) -> Any:
    """Retry a function until it returns a non-None value."""
    for i in range(max_retries):
        logger.debug(f"Retrying {fn.__name__} (attempt {i + 1}/{max_retries})")
        try:
            result = await fn()
        except exempted_exceptions:
            raise
        except Exception as e:
            if i == max_retries - 1:
                raise e
            await sleep(poll_interval * backoff_factor**i)
            continue
        if result is not None:
            return result
    return None


def handle_http_error(response: httpx.Response, operation: str) -> None:
    """
    Translate HTTP response errors into appropriate custom exceptions.

    Args:
        response: The HTTPX response object
        operation: Description of the operation that failed (for error messages)

    Raises:
        ClientError: For 4xx client errors
        ServerError: For 5xx server errors
    """
    if response.status_code >= 400:
        try:
            # Try to get error message from JSON response
            error_data = response.json()
            if isinstance(error_data, dict):
                error_message = error_data.get(
                    "message", error_data.get("error", response.text)
                )
            else:
                error_message = response.text
        except Exception:
            # Fallback to raw response text if JSON parsing fails
            error_message = response.text

        base_message = f"{operation} failed with status {response.status_code}"
        full_message = (
            f"{base_message}: {error_message}" if error_message else base_message
        )

        if 400 <= response.status_code < 500:
            raise ClientError(full_message)
        elif response.status_code >= 500:
            raise ServerError(full_message)


def storage_error_message(status_code: int) -> str:
    """
    Get a sanitized error message for storage operations based on HTTP status code.

    This function maps common HTTP status codes to user-friendly error messages
    without exposing implementation details from storage providers.

    Args:
        status_code: The HTTP status code from the storage response

    Returns:
        A sanitized error message suitable for user display
    """
    if status_code == 400:
        return "bad request"
    if status_code in (401, 403):
        return "access denied"
    if status_code == 404:
        return "object not found"
    if status_code == 409:
        return "conflict"
    if status_code == 413:
        return "object too large"
    if status_code == 429:
        return "rate limited, please try again later"
    if status_code in (500, 502, 503, 504):
        return "storage service temporarily unavailable"
    return "unexpected error"


def handle_storage_http_error(response: httpx.Response, operation: str) -> None:
    """
    Translate HTTP response errors from storage operations into appropriate exceptions.

    Unlike handle_http_error, this function uses sanitized error messages instead of
    raw response content to avoid exposing storage provider implementation details
    (e.g., S3 XML error responses with internal keys and request IDs).

    Args:
        response: The HTTPX response object from a storage operation
        operation: Description of the operation that failed (for error messages)

    Raises:
        ClientError: For 4xx client errors
        ServerError: For 5xx server errors
    """
    if response.status_code >= 400:
        message = storage_error_message(response.status_code)
        full_message = (
            f"{operation} failed with status {response.status_code}: {message}"
        )

        if 400 <= response.status_code < 500:
            raise ClientError(full_message)
        elif response.status_code >= 500:
            raise ServerError(full_message)


def handle_httpx_exception(exc: Exception, operation: str = "HTTP request") -> NoReturn:
    """
    Translate HTTPX exceptions into appropriate custom exceptions.

    Args:
        exc: The HTTPX exception
        operation: Description of the operation that failed (for error messages)

    Raises:
        TimeoutError: For timeout-related errors
        ClientError: For other client-side errors
        ServerError: For connection errors that might indicate server issues
    """
    if isinstance(exc, httpx.TimeoutException):
        raise TimeoutError(f"{operation} timed out: {exc}") from exc
    elif isinstance(exc, (httpx.ConnectError, httpx.NetworkError)):
        raise ServerError(f"{operation} failed due to network error: {exc}") from exc
    elif isinstance(exc, httpx.RequestError):
        raise ClientError(f"{operation} failed: {exc}") from exc
    else:
        # Fallback for other exceptions
        raise RenderError(f"{operation} failed with unexpected error: {exc}") from exc


def handle_api_error(
    response: Response[Any | Error], operation: str = "API request"
) -> None:
    """
    Convert an API Error object into the appropriate custom exception.

    Args:
        response: The API Response object that may contain an error
        operation: Description of the operation that failed (for error messages)

    Raises:
        ClientError: For client errors (typically 4xx equivalent)
        ServerError: For server errors (typically 5xx equivalent)
        RenderError: For unknown errors
    """
    message: str | None = None
    error_id: str | None = None

    # Try to extract error info from parsed response
    if isinstance(response.parsed, Error):
        raw_message = getattr(response.parsed, "message", None)
        if raw_message is not None and not isinstance(raw_message, Unset):
            message = raw_message
        raw_id = getattr(response.parsed, "id", None)
        if raw_id is not None and not isinstance(raw_id, Unset):
            error_id = raw_id
    elif response.parsed is None and response.content:
        # Parsed is None (e.g., 400 not handled) - try to extract from raw content
        try:
            import json

            error_data = json.loads(response.content)
            if isinstance(error_data, dict):
                message = error_data.get("message")
                error_id = error_data.get("id")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # Fallback to generic message if not available
    if not message:
        message = "Unknown error occurred"

    # Build full message with error ID if available
    if error_id:
        full_message = f"{operation} failed: {message} (ID: {error_id})"
    else:
        full_message = f"{operation} failed: {message}"

    if response.status_code:
        if response.status_code >= 400 and response.status_code < 500:
            raise ClientError(full_message)
        elif response.status_code >= 500:
            raise ServerError(full_message)
    else:
        raise ClientError(full_message)


def handle_http_errors(operation: str):
    """
    Decorator that handles HTTPX exceptions and HTTP error responses.

    This decorator wraps async functions that make HTTP requests and translates
    any HTTPX exceptions or HTTP error responses into appropriate custom exceptions.

    Args:
        operation: Description of the operation for error messages.

    Example:
        @handle_http_errors("create task")
        async def create_task_api_call():
            async with httpx.AsyncClient() as client:
                response = await client.post("/tasks", json=data)
                return response
    """

    def decorator(func: Callable[..., Awaitable[Response[Any | Error]]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)

                handle_api_error(result, operation)

                return result

            except httpx.RequestError as exc:
                handle_httpx_exception(exc, operation)
            except RenderError:
                raise
            except Exception as exc:
                # Unexpected exception
                raise RenderError(
                    f"{operation} failed with unexpected error: {exc}"
                ) from exc

        return wrapper

    return decorator
