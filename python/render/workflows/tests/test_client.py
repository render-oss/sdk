"""Tests for the UDS client's subtask submission."""

import uuid
from datetime import datetime

import pytest

from render import _startup
from render.workflows._callback_models import RunSubtaskRequest, RunSubtaskResponse
from render.workflows.client import Status, TaskResultResponse, UDSClient


def _new_client(monkeypatch, tmp_path) -> tuple[UDSClient, list[RunSubtaskRequest]]:
    """Build a UDSClient whose subtask calls are stubbed out.

    Returns the client and the list of requests it submits, in call order.
    """
    client = UDSClient(str(tmp_path / "test.sock"))
    captured: list[RunSubtaskRequest] = []

    async def fake_start_subtask(request: RunSubtaskRequest) -> RunSubtaskResponse:
        captured.append(request)
        return RunSubtaskResponse(task_run_id="trn-1")

    async def fake_get_task_result(task_run_id: str) -> TaskResultResponse:
        return TaskResultResponse(status=Status.SUCCESS, result=["ok"])

    monkeypatch.setattr(client, "_start_subtask", fake_start_subtask)
    monkeypatch.setattr(client, "get_task_result", fake_get_task_result)

    return client, captured


@pytest.mark.asyncio
async def test_run_subtask_sets_idempotency_key_and_created_at(monkeypatch, tmp_path):
    client, captured = _new_client(monkeypatch, tmp_path)

    result = await client.run_subtask("my-task", ["arg"])
    assert result == "ok"

    request = captured[0]
    assert isinstance(request.idempotency_key, str)
    # The key must be a well-formed UUID v4.
    assert uuid.UUID(request.idempotency_key).version == 4
    assert isinstance(request.created_at, str)
    # created_at must be a valid ISO-8601 / RFC 3339 timestamp.
    datetime.fromisoformat(request.created_at)


@pytest.mark.asyncio
async def test_run_subtask_generates_a_distinct_key_per_call(monkeypatch, tmp_path):
    client, captured = _new_client(monkeypatch, tmp_path)

    await client.run_subtask("my-task", ["arg"])
    await client.run_subtask("my-task", ["arg"])

    keys = [request.idempotency_key for request in captured]
    assert len(keys) == 2
    assert all(uuid.UUID(key).version == 4 for key in keys)
    assert keys[0] != keys[1]


@pytest.mark.parametrize(
    ("started", "finished", "sdk_started", "query"),
    [
        (1, 2, 3, "?sdk_import_started_at=1&sdk_import_finished_at=2&sdk_started_at=3"),
        (None, None, 3, "?sdk_started_at=3"),
        (None, None, None, ""),
    ],
)
@pytest.mark.asyncio
async def test_get_input_sends_captured_startup_timestamps(
    monkeypatch, tmp_path, started, finished, sdk_started, query
):
    monkeypatch.setattr(_startup, "_import_started_ns", started)
    monkeypatch.setattr(_startup, "_import_finished_ns", finished)
    monkeypatch.setattr(_startup, "_sdk_started_ns", sdk_started)
    client = UDSClient(str(tmp_path / "test.sock"))
    paths: list[str] = []

    async def fake_request(method, path, body):
        paths.append(path)
        return {"task_name": "t", "input": ""}

    monkeypatch.setattr(client, "_request", fake_request)

    await client.get_input()

    assert paths == ["/input" + query]
