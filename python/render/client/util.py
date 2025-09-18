from asyncio import sleep
from typing import Callable, Awaitable, Any, Tuple

async def poll_fn(fn: Callable[[],Awaitable[Tuple[Any, bool]]], poll_interval: float = 1.0) -> Any:
    """Poll a function until it returns a non-None value."""
    while True:
        result, done = await fn()
        if done:
            return result

        sleep(poll_interval)
