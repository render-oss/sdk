"""Type aliases and imports"""

from typing import Any

# Re-export commonly used types from generated client
from render.public_api.models.flow_run import FlowRun as _FlowRun
from render.public_api.models.flow_run_details import (
    FlowRunDetails as _FlowRunDetails,
)
from render.public_api.models.flow_run_status import FlowRunStatus as _FlowRunStatus
from render.public_api.models.task_run import TaskRun as _TaskRun
from render.public_api.models.task_run_details import (
    TaskRunDetails as _TaskRunDetails,
)
from render.public_api.models.task_run_status import TaskRunStatus as _TaskRunStatus

# Type aliases to match Go client interface
TaskSlug = str
# TaskData can be either positional (list) or named (dict) parameters
TaskData = list[Any] | dict[str, Any]
# FlowSlug is workflow-slug/flow-name, optionally suffixed with :version
FlowSlug = str
# FlowData can be either positional (list) or named (dict) parameters
FlowData = list[Any] | dict[str, Any]

# Re-export model classes with cleaner names
TaskRun = _TaskRun
TaskRunDetails = _TaskRunDetails
TaskRunStatus = _TaskRunStatus
FlowRun = _FlowRun
FlowRunDetails = _FlowRunDetails
FlowRunStatus = _FlowRunStatus

# Individual parameter types
LimitParam = int | None
CursorParam = str | None
OwnerIDParam = list[str] | None
FlowRunStatusParam = list[FlowRunStatus | str] | None


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


class ListFlowRunsParams:
    """Parameters for listing flow runs.

    Every list filter matches runs whose value is any of the given values.
    """

    def __init__(
        self,
        limit: LimitParam = None,
        cursor: CursorParam = None,
        flow_slug: list[str] | None = None,
        flow_id: list[str] | None = None,
        status: FlowRunStatusParam = None,
        owner_id: OwnerIDParam = None,
        workflow_version_id: list[str] | None = None,
        workflow_id: list[str] | None = None,
    ):
        self.limit = limit
        self.cursor = cursor
        self.flow_slug = flow_slug
        self.flow_id = flow_id
        self.status = status
        self.owner_id = owner_id
        self.workflow_version_id = workflow_version_id
        self.workflow_id = workflow_id


# Constants for TaskRunStatus values
class TaskRunStatusValues:
    """Constants for task run status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"  # deprecated, use SUCCEEDED instead
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


# Constants for FlowRunStatus values
class FlowRunStatusValues:
    """Constants for flow run status values."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
