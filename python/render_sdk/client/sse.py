"""Server-Sent Events (SSE) client

This module provides SSE streaming functionality for task run events.
"""

import json
import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

import httpx

from render_sdk.client.types import TaskRunDetails
from render_sdk.client.util import handle_http_error, handle_httpx_exception
from render_sdk.public_api.api.workflows.stream_task_runs_events import _get_kwargs

if TYPE_CHECKING:
    from render_sdk.client.client import Client

logger = logging.getLogger(__name__)


class SSEClient:
    """Client for Server-Sent Events streaming."""

    def __init__(self, client: "Client"):
        self.client = client

    async def stream_task_run_events(
        self,
        task_run_ids: list[str],
    ) -> AsyncIterator[TaskRunDetails]:
        """Stream task run events via SSE.

        Args:
            task_run_ids: List of task run IDs to stream events for

        Yields:
            TaskRunDetails: Task run event updates

        Raises:
            TimeoutError: For timeout-related errors
            ClientError: For other client-side errors
            ServerError: For connection errors that might indicate server issues
        """
        # Build the request parameters
        kwargs = _get_kwargs(task_run_ids=task_run_ids)

        # Create streaming request with appropriate timeout for SSE
        timeout = httpx.Timeout(
            connect=5.0, write=5.0, read=None, pool=None
        )  # These can be long lived
        async with httpx.AsyncClient(timeout=timeout) as http_client:
            # Set up headers for SSE
            headers = kwargs.get("headers", {})
            headers.update(
                {
                    "Accept": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Authorization": f"Bearer {self.client.token}",
                }
            )

            # Build the full URL
            url = f"{self.client.internal._base_url}{kwargs['url']}"

            try:
                async with http_client.stream(
                    method=kwargs["method"],
                    url=url,
                    params=kwargs.get("params", {}),
                    headers=headers,
                ) as response:
                    handle_http_error(response, "SSE stream")

                    async for event in parse_stream(response.aiter_bytes()):
                        yield event

            except httpx.RequestError as e:
                handle_httpx_exception(e, "SSE connection")


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
