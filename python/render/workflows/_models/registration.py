"""The task definitions a worker registers on startup."""

from __future__ import annotations

from dataclasses import dataclass, field

from render.workflows._models.wire import UNSET, Unset, Wire


@dataclass
class RetryConfig(Wire):
    max_retries: int | Unset = UNSET
    wait_duration_ms: int | Unset = UNSET
    factor: float | Unset = UNSET


@dataclass
class TaskOptions(Wire):
    retry: RetryConfig | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    plan: str | Unset = UNSET


@dataclass
class TaskParameter(Wire):
    name: str
    has_default: bool
    type_: str | Unset = field(default=UNSET, metadata={"wire_name": "type"})
    default_value: str | Unset = UNSET


@dataclass
class Task(Wire):
    name: str
    options: TaskOptions | Unset = UNSET
    parameters: list[TaskParameter] | Unset = UNSET
    # Registered with Workflows.flow. A flow may not set options.retry.
    workflow: bool | Unset = UNSET


@dataclass
class Tasks(Wire):
    tasks: list[Task]
