"""Render REST API Client

A Python client library for interacting with Render's REST API.
This module mirrors the functionality of the Go client in go/pkg/render.
"""

from .client import Client
from .types import (
    CursorParam,
    LimitParam,
    ListTaskRunsParams,
    OwnerIdParam,
    TaskData,
    TaskIdentifier,
    TaskRun,
    TaskRunDetails,
    TaskRunStatus,
)
from .workflows import WorkflowsService

# Constants for TaskRunStatus
TASK_RUN_STATUS_PENDING = "pending"
TASK_RUN_STATUS_RUNNING = "running"
TASK_RUN_STATUS_COMPLETED = "completed"
TASK_RUN_STATUS_FAILED = "failed"

__all__ = [
    "Client",
    "WorkflowsService",
    "TaskData",
    "TaskIdentifier",
    "TaskRun",
    "TaskRunDetails",
    "TaskRunStatus",
    "ListTaskRunsParams",
    "LimitParam",
    "CursorParam",
    "OwnerIdParam",
    "TASK_RUN_STATUS_PENDING",
    "TASK_RUN_STATUS_RUNNING",
    "TASK_RUN_STATUS_COMPLETED",
    "TASK_RUN_STATUS_FAILED",
]
