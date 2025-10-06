#!/usr/bin/env python3
"""Unit tests for SSE parsing functionality."""

import json

import pytest

from render_sdk.client import TaskRunDetails, TaskRunStatus
from render_sdk.client.sse import parse_stream


class BytesAiter:
    def __init__(self, data: bytes):
        self.data = data

    def __aiter__(self):
        self.pos = 0
        return self

    async def __anext__(self):
        if self.pos >= len(self.data):
            raise StopAsyncIteration
        chunk = self.data[self.pos]
        self.pos += 1
        return chunk


@pytest.mark.asyncio
async def test_parse_stream_completed():
    """Test parsing of SSE stream."""

    details = TaskRunDetails(
        id="trn-test123",
        task_id="tsk-test123",
        status=TaskRunStatus.COMPLETED,
        results=[42],
        input_=[],
        parent_task_run_id="trn-test123",
        root_task_run_id="trn-test123",
        retries=0,
    )
    sse_data = [
        b"event: task.completed\ndata: "
        + json.dumps(details.to_dict()).encode("utf-8")
        + b"\n\n"
    ]

    count = 0
    async for event in parse_stream(BytesAiter(sse_data)):
        assert event.id == "trn-test123"
        assert event.status.value == TaskRunStatus.COMPLETED
        count += 1

    assert count == 1


@pytest.mark.asyncio
async def test_parse_stream_malformed():
    """Test parsing of SSE malformedstream."""
    sse_data = [b"this is not a valid SSE event\n\n"]

    count = 0
    async for _ in parse_stream(BytesAiter(sse_data)):
        count += 1

    assert count == 0
