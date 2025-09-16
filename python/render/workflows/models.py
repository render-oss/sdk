"""Typed models for API requests and responses."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


# Enums for callback status types
class CallbackStatus(str, Enum):
    COMPLETE = "complete"
    ERROR = "error"
    SUBTASK = "subtask"


class CallbackType(str, Enum):
    COMPLETE = "complete"
    ERROR = "error"
    SUBTASK = "subtask"


# Task-related models
@dataclass
class RetryOptions:
    """Retry configuration for a task."""

    max_retries: int
    wait_duration_ms: int
    factor: float


@dataclass
class TaskOptions:
    """Options for a task."""

    retry: RetryOptions | None = None


@dataclass
class TaskDefinition:
    """Definition of a task to be registered."""

    name: str
    options: dict[str, Any] | None = None


@dataclass
class TaskRegistrationRequest:
    """Request payload for registering tasks."""

    tasks: list[TaskDefinition]


@dataclass
class TaskRegistrationResponse:
    """Response from task registration."""

    status: str


# Input/Output models
@dataclass
class TaskInput:
    """Input data for a task execution."""

    task_name: str
    input: str | None = None  # base64 encoded JSON


# Callback models
@dataclass
class TaskCompleteData:
    """Data for a completed task callback."""

    output: str  # base64 encoded JSON array


@dataclass
class TaskErrorDetails:
    """Error details for a failed task callback."""

    details: str
    exit_code: int = 1
    is_reported_by_sdk: bool = True
    is_system_err: bool = False
    is_oom: bool = False
    is_timeout: bool = False


@dataclass
class SubtaskData:
    """Data for a subtask callback."""

    name: str
    input: str  # base64 encoded JSON


@dataclass
class CallbackRequest:
    """Base callback request structure."""

    status: CallbackStatus
    complete: TaskCompleteData | None = None
    error: TaskErrorDetails | None = None
    subtask: SubtaskData | None = None


@dataclass
class CallbackResponse:
    """Response from a callback."""

    status: str
    task_run_id: str | None = None


# Task result models
@dataclass
class TaskResultResponse:
    """Response when requesting task results."""

    status: str
    result: Any | None = None
    error: str | None = None


# Internal callback data (what the executor passes to client)
@dataclass
class CallbackData:
    """Internal callback data structure used by executor."""

    type: CallbackType
    result: Any | None = None
    error: str | None = None
    name: str | None = None  # For subtasks
    input: Any | None = None  # For subtasks
