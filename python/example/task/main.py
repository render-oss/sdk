"""Example usage of the Render Tasks Python SDK."""

import asyncio
import logging

from render_sdk.workflows import Options, Retry, start, task

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@task
def square(a: int) -> int:
    """Square a number."""
    logger.info(f"Computing square of {a}")
    return a * a


@task
async def add_squares(a: int, b: int) -> int:
    """Add the squares of two numbers."""
    logger.info(f"Computing add_squares: {a}, {b}")

    # Execute subtasks
    result1 = await square(a)
    logger.info(f"Square result: {result1}")
    result2 = await square(b)
    logger.info(f"Square result: {result2}")

    return result1 + result2


@task(
    name="custom_add",
    options=Options(retry=Retry(max_retries=3, wait_duration=1000)),
)
def add_numbers(a: int, b: int) -> int:
    """Add two numbers with retry configuration."""
    logger.info(f"Adding {a} + {b}")
    return a + b


@task
def greet(name: str) -> str:
    """Greet someone."""
    logger.info(f"Greeting {name}")
    return f"Hello, {name}!"


@task
async def fan_out(n: int) -> list[int]:
    """Fan out a number into a list of numbers."""
    squares = [square(i) for i in range(n)]
    results = await asyncio.gather(*squares)
    return results


if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        logger.error(f"Error starting Render Tasks example: {e}")
        raise
