"""Type aliases and imports

This module provides type aliases that mirror the Go client types,
re-exporting from the generated client for convenience.
"""

from typing import Any, Optional, Union

# Re-export commonly used types from generated client
from render.client.render_public_api_client.models.task_run import TaskRun as _TaskRun
from render.client.render_public_api_client.models.task_run_details import (
    TaskRunDetails as _TaskRunDetails,
)
from render.client.render_public_api_client.models.task_run_status import (
    TaskRunStatus as _TaskRunStatus,
)

# Type aliases to match Go client interface
TaskIdentifier = str
TaskData = Union[dict[str, Any], list[Any], str, int, float, bool, None]

# Re-export model classes with cleaner names
TaskRun = _TaskRun
TaskRunDetails = _TaskRunDetails
TaskRunStatus = _TaskRunStatus


# Parameter types for API calls
class ListTaskRunsParams:
    """Parameters for listing task runs."""

    def __init__(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        owner_id: Optional[str] = None,
    ):
        self.limit = limit
        self.cursor = cursor
        self.owner_id = owner_id


# Individual parameter types
LimitParam = Optional[int]
CursorParam = Optional[str]
OwnerIdParam = Optional[str]


# Constants for TaskRunStatus values (matching the Go client)
class TaskRunStatusValues:
    """Constants for task run status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
