"""Type aliases and imports

This module provides type aliases that mirror the Go client types,
re-exporting from the generated client for convenience.
"""

from typing import Any

# Re-export commonly used types from generated client
from render.public_api.models.task_run import TaskRun as _TaskRun
from render.public_api.models.task_run_details import (
    TaskRunDetails as _TaskRunDetails,
)
from render.public_api.models.task_run_status import (
    TaskRunStatus as _TaskRunStatus,
)

# Type aliases to match Go client interface
TaskIdentifier = str
TaskData = dict[str, Any] | list[Any] | str | int | float | bool | None

# Re-export model classes with cleaner names
TaskRun = _TaskRun
TaskRunDetails = _TaskRunDetails
TaskRunStatus = _TaskRunStatus

# Individual parameter types
LimitParam = int | None
CursorParam = str | None
OwnerIDParam = str | None


# Parameter types for API calls
class ListTaskRunsParams:
    """Parameters for listing task runs."""

    def __init__(
        self,
        limit: LimitParam = None,
        cursor: CursorParam = None,
        owner_id: OwnerIDParam = None,
    ):
        self.limit = limit
        self.cursor = cursor
        self.owner_id = owner_id





# Constants for TaskRunStatus values (matching the Go client)
class TaskRunStatusValues:
    """Constants for task run status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
