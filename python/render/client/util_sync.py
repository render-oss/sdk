"""Synchronous utility functions for the Render SDK.

Only retry_with_backoff and handle_http_errors need sync variants.
All other functions in util.py are already synchronous and are imported directly.
"""

import functools
import logging
from collections.abc import Callable
from typing import Any

from render.client.util import (
    _handle_wrapper_exception,
    handle_api_error,
    handle_http_error,
    handle_httpx_exception,
    handle_storage_http_error,
    request_errors,
)
from render.public_api.models.error import Error
from render.public_api.types import Response
from render.retry import retry_with_backoff_sync as retry_with_backoff

# Re-export sync functions so unasync'd imports from util_sync work
__all__ = [
    "retry_with_backoff",
    "handle_http_errors",
    "_handle_wrapper_exception",
    "handle_api_error",
    "handle_http_error",
    "handle_httpx_exception",
    "request_errors",
    "handle_storage_http_error",
]

logger = logging.getLogger(__name__)


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
