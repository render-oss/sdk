"""Task definition example.

This demonstrates the Workflows class pattern for defining durable tasks.
"""

import logging

from render import Retry, TaskContext, Workflows

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Workflows(
    default_retry=Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0),
    default_timeout=300,
    default_plan="standard",
)


@app.task
def not_registered_task(ctx: TaskContext, a: int) -> int:
    """Square a number."""
    logger.info(f"Computing square of {a}")
    return a * a


# Intentionally left commented out. This module only *defines* a task; it is
# imported by main.py, which owns the worker lifecycle.
#
# app.start()
