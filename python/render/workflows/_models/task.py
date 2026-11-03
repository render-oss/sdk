"""A task run's input and the callback that reports its result."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from render.workflows._models.history import History
from render.workflows._models.step import StepKey
from render.workflows._models.wire import UNSET, Unset, Wire


@dataclass
class InputResponse(Wire):
    task_name: str
    input_: str = field(metadata={"wire_name": "input"})
    task_run_id: str | Unset = UNSET
    root_task_run_id: str | Unset = UNSET
    parent_task_run_id: str | Unset = UNSET
    is_workflow: bool | Unset = UNSET
    # Workflows only. 0 is the run's first attempt.
    attempt: int | Unset = UNSET
    # Workflows only. Empty until the workflow records a step.
    history: History = field(default_factory=History)
    # Workflows only. Who retries a failed inline step; absent means local.
    inline_retry_mode: str | Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InputResponse:
        return cls(
            task_name=d["task_name"],
            input_=d.get("input", ""),
            task_run_id=d.get("task_run_id", UNSET),
            root_task_run_id=d.get("root_task_run_id", UNSET),
            parent_task_run_id=d.get("parent_task_run_id", UNSET),
            is_workflow=d.get("is_workflow", UNSET),
            attempt=d.get("attempt", UNSET),
            history=History.from_dict(d.get("history") or {}),
            inline_retry_mode=d.get("inline_retry_mode", UNSET),
        )


@dataclass
class TaskComplete(Wire):
    output: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskComplete:
        return cls(output=d["output"])


class DeterminismKind(str, Enum):
    """How a replayed step differs from the step recorded in history."""

    INPUT_HASH = "input_hash"
    """The step's name or arguments changed."""
    TYPE = "type"
    """The flow made a different kind of ctx call, or finished early."""
    UNKNOWN_TYPE = "unknown_type"
    """History recorded a step type this SDK doesn't know."""

    @property
    def description(self) -> str:
        """What changed, as a DeterminismError message puts it."""
        match self:
            case DeterminismKind.INPUT_HASH:
                return "the step's name or input changed"
            case DeterminismKind.TYPE:
                return "the step type changed"
            case DeterminismKind.UNKNOWN_TYPE:
                return "the recorded step type is unknown"


@dataclass
class DeterminismDetails(Wire):
    """Where and how a flow replay diverged from its recorded history."""

    step_key: StepKey
    kind: DeterminismKind
    workflow_attempt: int | Unset = UNSET
    # Human-readable calls: what the history recorded, and what this replay did.
    expected: str | Unset = UNSET
    actual: str | Unset = UNSET


class TaskErrorReason(str, Enum):
    """Why a task failed, when it's more than an ordinary task error."""

    DETERMINISM = "DeterminismError"
    """A flow replay diverged from its recorded history."""

    SYSTEM = "system_error"
    """Render caused the failure, such as the SDK being unable to reach a Render
    service. The run is retried as a system failure."""

    WORKFLOW_STEP_LIMIT_EXCEEDED = "workflow_step_limit_exceeded"
    """The flow run recorded more steps than its limit allows."""

    WORKFLOW_PAYLOAD_TOO_LARGE = "workflow_payload_too_large"
    """A step's input or output was larger than the limit allows."""


@dataclass
class TaskError(Wire):
    details: str
    stack_trace: str | Unset = UNSET
    # Absent for an ordinary task error.
    reason: TaskErrorReason | Unset = UNSET
    determinism: DeterminismDetails | Unset = UNSET
    # For a flow limit: the limit, and the value that exceeded it.
    limit: int | Unset = UNSET
    value: int | Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskError:
        return cls(details=d["details"], stack_trace=d.get("stack_trace", UNSET))


@dataclass
class CallbackRequest(Wire):
    error: TaskError | Unset = UNSET
    complete: TaskComplete | Unset = UNSET
