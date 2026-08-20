"""Example usage of the Render Tasks Python SDK."""

import logging

from not_registered import not_registered_task

from render_sdk.workflows import TaskContext, start, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task
async def call_not_registered_task(ctx: TaskContext, n: int) -> int:
    """Call a not registered task."""
    return await ctx.run(not_registered_task, n)


@task
async def deadlock_test(ctx: TaskContext, n: int) -> int:
    """
    Deadlock test example.

    If we don't properly mark parent tasks waiting on subtasks, we can
    deadlock the workflow. This will spawn a chain of n tasks that will
    each wait for the next sub task to complete. If n > the max concurrency limit
    we will deadlock the workflow if our pause logic is not working.
    """

    if n > 0:
        await ctx.run(deadlock_test, n - 1)

    logger.info(f"Deadlock test {n} complete")

    return n


@task
async def print_hello_world(ctx: TaskContext) -> None:
    """Prints a simple string."""
    print("Hello, world!")


@task
async def emit_logs(ctx: TaskContext) -> None:
    """Emits a series of log messages at different log levels."""
    logger.info("Logging to INFO")
    logger.warning("Logging to WARNING")
    logger.error("Logging to ERROR")
    logger.critical("Logging to CRITICAL")


@task
async def calculate_square(ctx: TaskContext, n: int) -> int:
    """Calculate the square of a number."""
    return n * n


@task
async def add_squares(ctx: TaskContext, a: int, b: int) -> int:
    """Add the squares of two numbers."""
    logger.info(f"Computing add_squares: {a}, {b}")

    # Execute subtasks
    result1 = await ctx.run(calculate_square, a)
    logger.info(f"Square result 1: {result1}")
    result2 = await ctx.run(calculate_square, b)
    logger.info(f"Square result 2: {result2}")

    return result1 + result2


if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        logger.error(f"Error starting Render Tasks example: {e}")
        raise
