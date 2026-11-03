"""Retry with backoff, shared by the REST client and the workflow worker.

It has no REST dependencies, so the worker can use it without loading the
REST client.
"""

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


async def retry_with_backoff(
    fn: Callable[[], Awaitable[_T]],
    max_retries: int = 5,
    poll_interval: float = 1.0,
    backoff_factor: float = 2.0,
    exempted_exceptions: tuple[type[Exception], ...] = (),
) -> _T:
    """Retry a function until it returns a non-None value, up to max_retries
    times after its first attempt. Returns the last attempt's result, which is
    None only if every attempt returned None."""
    retry = 0
    while True:
        logger.debug(f"Calling {fn.__name__} (retry {retry}/{max_retries})")
        try:
            result = await fn()
        except exempted_exceptions:
            raise
        except Exception:
            if retry >= max_retries:
                raise
            await asyncio.sleep(poll_interval * backoff_factor**retry)
            retry += 1
            continue
        if result is not None or retry >= max_retries:
            return result
        retry += 1


def retry_with_backoff_sync(
    fn: Callable[[], _T],
    max_retries: int = 5,
    poll_interval: float = 1.0,
    backoff_factor: float = 2.0,
    exempted_exceptions: tuple[type[Exception], ...] = (),
) -> _T:
    """Retry a function until it returns a non-None value, up to max_retries
    times after its first attempt. Returns the last attempt's result, which is
    None only if every attempt returned None."""
    retry = 0
    while True:
        logger.debug(f"Calling {fn.__name__} (retry {retry}/{max_retries})")
        try:
            result = fn()
        except exempted_exceptions:
            raise
        except Exception:
            if retry >= max_retries:
                raise
            time.sleep(poll_interval * backoff_factor**retry)
            retry += 1
            continue
        if result is not None or retry >= max_retries:
            return result
        retry += 1
