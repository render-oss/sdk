"""Task definition example.

This demonstrates the Workflows class pattern for defining durable tasks.
"""

import asyncio
import logging

from render_sdk import Retry, TaskContext, Workflows

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Workflows(
    default_retry=Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0),
    default_timeout=300,
    default_plan="standard",
)


@app.task
def square(ctx: TaskContext, a: int) -> int:
    """Square a number."""
    logger.info(f"Computing square of {a}")
    return a * a


@app.task
async def add_squares(ctx: TaskContext, a: int, b: int) -> int:
    """Add the squares of two numbers."""
    logger.info(f"Computing add_squares: {a}, {b}")

    result1 = await ctx.run(square, a)
    logger.info(f"Square result: {result1}")
    result2 = await ctx.run(square, b)
    logger.info(f"Square result: {result2}")

    return result1 + result2


@app.task(name="custom_add", retry=Retry(max_retries=3, wait_duration_ms=1000))
def add_numbers(ctx: TaskContext, a: int, b: int) -> int:
    """Add two numbers with custom retry configuration."""
    logger.info(f"Adding {a} + {b}")
    return a + b


@app.task
def greet(ctx: TaskContext, name: str) -> str:
    """Greet someone."""
    logger.info(f"Greeting {name}")
    return f"Hello, {name}!"


@app.task
async def fan_out(ctx: TaskContext, n: int) -> list[int]:
    """Fan out a number into a list of squares."""
    squares = [ctx.run(square, i) for i in range(n)]
    results = await asyncio.gather(*squares)
    return list(results)


# Start via CLI: render-workflows example.task.main:app
# Or call app.start() directly
app.start()
