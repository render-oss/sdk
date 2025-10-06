"""Example usage of the Render Tasks Python SDK."""

import logging

from render_sdk.workflows import Options, Retry, start, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000)),
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


if __name__ == "__main__":
    logger.info("Starting Render Tasks example")
    try:
        start()
    except Exception as e:
        logger.error(f"Error starting Render Tasks example: {e}")
        raise
