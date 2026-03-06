"""Server-Sent Events (SSE) utilities

This module provides SSE stream parsing functionality for task run events.
"""

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from render_sdk.client.types import TaskRunDetails

logger = logging.getLogger(__name__)


class SSEParser:
    """Stateful parser for Server-Sent Events byte streams.

    Accepts raw byte chunks via feed() and returns any complete
    TaskRunDetails events parsed from the stream. Shared by both
    the async and sync parse_stream entry points.
    """

    def __init__(self) -> None:
        self._buffer = ""
        self._event_data: dict[str, Any] = {}

    def feed(self, chunk: bytes) -> list[TaskRunDetails]:
        """Feed a chunk of bytes and return any completed events."""
        results: list[TaskRunDetails] = []
        self._buffer += chunk.decode("utf-8", errors="ignore")

        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            line = line.rstrip("\r")

            # Empty line indicates end of event
            if not line:
                if "data" in self._event_data and "event" in self._event_data:
                    try:
                        # NOTE: right now, the API emits all terminal events as
                        # "task.completed" events regardless of status. The true
                        # event status is contained elsewhere in the event data.
                        # These are here for forward compatibility.
                        if self._event_data["event"] in (
                            "task.canceled",
                            "task.completed",
                            "task.failed",
                            "task.succeeded",
                        ):
                            data = json.loads(self._event_data["data"])
                            results.append(_convert_to_task_run_details(data))
                    except Exception as e:
                        logger.error(f"Error parsing event: {e}")

                self._event_data = {}
                continue

            # Parse SSE fields
            if ":" in line:
                field, value = line.split(":", 1)
                self._event_data[field.strip()] = value.strip()

        return results


async def parse_stream(
    bytes_iter: AsyncIterator[bytes],
) -> AsyncIterator[TaskRunDetails]:
    """Parse an async stream of bytes into TaskRunDetails."""
    parser = SSEParser()
    async for chunk in bytes_iter:
        for event in parser.feed(chunk):
            yield event


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
