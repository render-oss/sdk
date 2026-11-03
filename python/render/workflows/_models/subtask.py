"""Starting a subtask run and polling for its result."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from render.workflows._models.task import TaskComplete, TaskError
from render.workflows._models.wire import UNSET, Unset, Wire


@dataclass
class RunSubtaskRequest(Wire):
    task_name: str
    input_: str | Unset = field(default=UNSET, metadata={"wire_name": "input"})
    # Deduplicates subtask creation across retries. Generated once per logical
    # subtask call and resent on every retry, so the scheduler resolves a
    # retried submission to the original subtask instead of creating a duplicate.
    #
    # This key should uniquely identify the task run within a workflow version.
    # The SDK uses a UUID v4.
    idempotency_key: str | Unset = UNSET
    # Caller-pinned creation time (RFC 3339). Must be stable across retries: the
    # scheduler deduplicates on (idempotency_key, created_at).
    created_at: str | Unset = UNSET


@dataclass
class RunSubtaskResponse(Wire):
    task_run_id: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RunSubtaskResponse:
        return cls(task_run_id=d["task_run_id"])


@dataclass
class SubtaskResultRequest(Wire):
    task_run_id: str


@dataclass
class SubtaskResultResponse(Wire):
    still_running: bool
    error: TaskError | Unset = UNSET
    complete: TaskComplete | Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SubtaskResultResponse:
        error: TaskError | Unset = UNSET
        if d.get("error") is not None:
            error = TaskError.from_dict(d["error"])
        complete: TaskComplete | Unset = UNSET
        if d.get("complete") is not None:
            complete = TaskComplete.from_dict(d["complete"])
        return cls(
            still_running=bool(d["still_running"]),
            error=error,
            complete=complete,
        )
