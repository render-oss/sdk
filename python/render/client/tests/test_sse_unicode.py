"""Network chunk boundaries must not alter UTF-8 task results."""

import json

import pytest

from render.client import TaskRunDetails, TaskRunStatus
from render.client.sse import parse_stream
from render.client.sse_sync import parse_stream as parse_stream_sync

_RESULT = "café 中文 🚀"
_DETAILS = TaskRunDetails(
    id="trn-unicode",
    task_id="tsk-unicode",
    status=TaskRunStatus.COMPLETED,
    results=[_RESULT],
    input_=[],
    parent_task_run_id="trn-unicode",
    root_task_run_id="trn-unicode",
    retries=0,
    attempts=[],
)
_EVENT = (
    b"event: task.completed\ndata: "
    + json.dumps(_DETAILS.to_dict(), ensure_ascii=False).encode()
    + b"\n\n"
)
_START = _EVENT.index(_RESULT.encode())
_CHUNKS = [
    [_EVENT[:split], _EVENT[split:]]
    for split in range(_START + 1, _START + len(_RESULT.encode()))
] + [[bytes([byte]) for byte in _EVENT]]


@pytest.mark.parametrize("chunks", _CHUNKS)
def test_sync_stream_preserves_split_utf8(chunks):
    events = list(parse_stream_sync(iter(chunks)))
    assert len(events) == 1
    assert events[0].results == [_RESULT]


@pytest.mark.parametrize("chunks", _CHUNKS)
@pytest.mark.asyncio
async def test_async_stream_preserves_split_utf8(chunks):
    async def stream():
        for chunk in chunks:
            yield chunk

    events = [event async for event in parse_stream(stream())]
    assert len(events) == 1
    assert events[0].results == [_RESULT]
