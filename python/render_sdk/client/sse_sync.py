"""Synchronous Server-Sent Events (SSE) utilities.

Sync entry point for SSE stream parsing. All parsing logic lives
in SSEParser (defined in sse.py); this module only provides the
sync iteration wrapper.
"""

from collections.abc import Iterator

from render_sdk.client.sse import SSEParser
from render_sdk.client.types import TaskRunDetails


def parse_stream(
    bytes_iter: Iterator[bytes],
) -> Iterator[TaskRunDetails]:
    """Parse a sync stream of bytes into TaskRunDetails."""
    parser = SSEParser()
    for chunk in bytes_iter:
        yield from parser.feed(chunk)
