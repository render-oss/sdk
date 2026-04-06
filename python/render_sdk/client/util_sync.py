"""Synchronous utility functions for the Render SDK.

Only retry_with_backoff and handle_http_errors need sync variants.
All other functions in util.py are already synchronous and are imported directly.
"""

import functools
import logging
from collections.abc import Callable
from time import sleep
from typing import Any

from render_sdk.client.util import (
    _handle_wrapper_exception,
    handle_api_error,
    handle_http_error,
    handle_httpx_exception,
    handle_storage_http_error,
)
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.types import Response

# Re-export sync functions so unasync'd imports from util_sync work
__all__ = [
    "retry_with_backoff",
    "handle_http_errors",
    "_handle_wrapper_exception",
    "handle_api_error",
    "handle_http_error",
    "handle_httpx_exception",
    "handle_storage_http_error",
]

logger = logging.getLogger(__name__)


def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 5,
    poll_interval: float = 1.0,
    backoff_factor: float = 2.0,
    exempted_exceptions: tuple[type[Exception], ...] = (),
) -> Any:
    """Retry a function until it returns a non-None value."""
    for i in range(max_retries):
        logger.debug(f"Retrying {fn.__name__} (attempt {i + 1}/{max_retries})")
        try:
            result = fn()
        except exempted_exceptions:
            raise
        except Exception as e:
            if i == max_retries - 1:
                raise e
            sleep(poll_interval * backoff_factor**i)
            continue
        if result is not None:
            return result
    return None


def handle_http_errors(operation: str):
    """
    Decorator that handles HTTPX exceptions and HTTP error responses.

    Sync version of the decorator in util.py.

    Args:
        operation: Description of the operation for error messages.
    """

    def decorator(func: Callable[..., Response[Any | Error]]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                _handle_wrapper_exception(exc, operation)
            handle_api_error(result, operation)
            return result

        return wrapper

    return decorator
