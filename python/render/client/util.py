import logging
from asyncio import sleep
from collections.abc import Awaitable, Callable
from typing import Any

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
