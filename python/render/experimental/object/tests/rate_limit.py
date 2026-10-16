"""Retry 429s in the object storage e2e tests.

Every PR's E2E job shares one staging account, so concurrent runs trip the API
rate limit. RateLimitError doesn't carry the Retry-After header, so back off
exponentially with jitter instead.
"""

import asyncio
import functools
import random
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

from render.client.errors import RateLimitError
from render.experimental.object.client import ObjectClient

P = ParamSpec("P")
R = TypeVar("R")

# Total window is ~60 seconds before jitter
MAX_ATTEMPTS = 7
INITIAL_DELAY_S = 1.0
MAX_DELAY_S = 16.0


def retry_rate_limited(
    func: Callable[P, Awaitable[R]],
    *,
    initial_delay_s: float = INITIAL_DELAY_S,
) -> Callable[P, Awaitable[R]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for attempt in range(MAX_ATTEMPTS):
            try:
                return await func(*args, **kwargs)
            except RateLimitError:
                if attempt >= MAX_ATTEMPTS - 1:
                    raise
                delay = min(initial_delay_s * 2**attempt, MAX_DELAY_S)
                await asyncio.sleep(delay * random.uniform(0.5, 1.5))  # noqa: S311
        raise AssertionError("unreachable")  # pragma: no cover

    return wrapper


def patch_rate_limit_retries(
    client: ObjectClient, *, initial_delay_s: float = INITIAL_DELAY_S
) -> None:
    """Wrap the client's API methods in place.

    ScopedObjectClient delegates to these, so scoped() is covered too.
    """
    for name in ("put", "get", "delete", "list"):
        method = getattr(client, name)
        setattr(
            client,
            name,
            retry_rate_limited(method, initial_delay_s=initial_delay_s),
        )
