"""Example usage of the Render Tasks Python SDK."""

import logging

from render_sdk.workflows import start, task

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@task
async def deadlock_test(n: int) -> int:
    """
    Deadlock test example.

    If we don't properly mark parent tasks waiting on subtasks, we can
    deadlock the workflow. This will spawn a chain of n tasks that will 
    each wait for the next sub task to complete. If n > the max concurrency limit
    we will deadlock the workflow if our pause logic is not working.
    """

    if n > 0:
        await deadlock_test(n - 1)
    
    logger.info(f"Deadlock test {n} complete")

    return n

if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        logger.error(f"Error starting Render Tasks example: {e}")
        raise
