"""Server-Sent Events (SSE) utilities

This module provides SSE stream parsing functionality for task run events.
"""

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from render_sdk.client.types import TaskRunDetails

logger = logging.getLogger(__name__)


async def parse_stream(
    bytes_iter: AsyncIterator[bytes],
) -> AsyncIterator[TaskRunDetails]:
    """Parse a stream of bytes into TaskRunDetails."""
    buffer = ""
    event_data: dict[str, Any] = {}

    async for chunk in bytes_iter:
        buffer += chunk.decode("utf-8", errors="ignore")

        # Process complete lines
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.rstrip("\r")

            # Empty line indicates end of event
            if not line:
                if "data" in event_data and "event" in event_data:
                    try:
                        # Yield event if it's a task.completed event
                        if event_data["event"] == "task.completed":
                            data = json.loads(event_data["data"])
                            task_run_details = _convert_to_task_run_details(data)
                            yield task_run_details

                    except Exception as e:
                        logger.error(f"Error parsing event: {e}")
                        # Skip invalid events
                        pass

                # Reset for next event
                event_data = {}
                continue

            # Parse SSE fields
            if ":" in line:
                field, value = line.split(":", 1)
                field = field.strip()
                value = value.strip()
                event_data[field] = value


def _convert_to_task_run_details(data: dict) -> TaskRunDetails:
    """Convert JSON event data to TaskRunDetails object.

    Args:
        data: Raw JSON event data

    Returns:
        TaskRunDetails: Converted task run details

    Raises:
        KeyError: If required fields are missing
        TypeError: If data types are incorrect
    """
    return TaskRunDetails.from_dict(data)
