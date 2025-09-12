"""Typed models for API requests and responses."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


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
    retry: Optional[RetryOptions] = None


@dataclass
class TaskDefinition:
    """Definition of a task to be registered."""
    name: str
    options: Optional[Dict[str, Any]] = None


@dataclass
class TaskRegistrationRequest:
    """Request payload for registering tasks."""
    tasks: List[TaskDefinition]


@dataclass
class TaskRegistrationResponse:
    """Response from task registration."""
    status: str


# Input/Output models
@dataclass
class TaskInput:
    """Input data for a task execution."""
    task_name: str
    input: Optional[str] = None  # base64 encoded JSON


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
    complete: Optional[TaskCompleteData] = None
    error: Optional[TaskErrorDetails] = None
    subtask: Optional[SubtaskData] = None


@dataclass
class CallbackResponse:
    """Response from a callback."""
    status: str
    task_run_id: Optional[str] = None


# Task result models
@dataclass
class TaskResultResponse:
    """Response when requesting task results."""
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None


# Internal callback data (what the executor passes to client)
@dataclass
class CallbackData:
    """Internal callback data structure used by executor."""
    type: CallbackType
    result: Optional[Any] = None
    error: Optional[str] = None
    name: Optional[str] = None  # For subtasks
    input: Optional[Any] = None  # For subtasks
