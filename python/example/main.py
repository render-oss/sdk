"""Example usage of the Render Tasks Python SDK."""

import sys
import os
import logging

# Add the parent directory to Python path so we can import render_tasks
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from render_tasks import task, start, Options, Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task
def square(a: int) -> int:
    """Square a number."""
    logger.info(f"Computing square of {a}")
    return a * a

@task
def add_squares(a: int, b: int) -> int:
    """Add the squares of two numbers."""
    logger.info(f"Computing add_squares: {a}, {b}")

    # Execute subtasks
    result1 = square(a)
    result2 = square(b)

    logger.info(f"Square results: {result1.result}, {result2.result}")

    return result1.result + result2.result

@task(name="custom_add", options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000)))
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
