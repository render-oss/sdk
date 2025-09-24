"""Type aliases and imports"""

from typing import Any

# Re-export commonly used types from generated client
from render.public_api.models.task_run import TaskRun as _TaskRun
from render.public_api.models.task_run_details import TaskRunDetails as _TaskRunDetails
from render.public_api.models.task_run_status import TaskRunStatus as _TaskRunStatus
from render.public_api.types import Unset

# Type aliases to match Go client interface
TaskIdentifier = str
TaskData = list[Any]

# Re-export model classes with cleaner names
TaskRun = _TaskRun
TaskRunDetails = _TaskRunDetails
TaskRunStatus = _TaskRunStatus

# Individual parameter types
LimitParam = int | None
CursorParam = str | None
OwnerIDParam = list[str] | None


# Parameter types for API calls
class ListTaskRunsParams:
    """Parameters for listing task runs."""

    limit: int | Unset
    cursor: str | Unset
    owner_id: list[str] | Unset

    def __init__(
        self,
        limit: LimitParam = None,
        cursor: CursorParam = None,
        owner_id: OwnerIDParam = None,
    ):
        if limit is None:
            self.limit = Unset()
        else:
            self.limit = limit

        if cursor is None:
            self.cursor = Unset()
        else:
            self.cursor = cursor

        if owner_id is None:
            self.owner_id = Unset()
        else:
            self.owner_id = owner_id


# Constants for TaskRunStatus values
class TaskRunStatusValues:
    """Constants for task run status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
