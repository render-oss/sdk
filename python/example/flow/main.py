"""Inline retries for a transient operation."""

import logging

from render import FlowContext, Retry, Workflows

logger = logging.getLogger(__name__)
app = Workflows()


@app.flow
def inline_retry(ctx: FlowContext) -> int:
    """Return 3 after two local retries within one flow attempt."""
    attempts = 0

    def fail_twice() -> int:
        """Stand in for an operation that has two transient failures."""
        nonlocal attempts
        attempts += 1
        logger.info("Inline step attempt %s", attempts)
        if attempts < 3:
            raise ValueError("Example transient failure")
        return attempts

    # Inline step: retries in this process and returns its recorded result on replay.
    return ctx.step(
        "transient_operation",
        fail_twice,
        retry=Retry(max_retries=2, wait_duration_ms=100, backoff_scaling=2),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.start()
