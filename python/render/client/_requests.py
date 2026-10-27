"""Request builders shared by the async and sync workflows clients.

These are pure functions that turn SDK arguments into generated API request
bodies and query arguments, so both clients build requests the same way.
"""

from typing import Any

from render.client.types import (
    FlowData,
    FlowRunStatus,
    FlowSlug,
    ListFlowRunsParams,
    TaskData,
    TaskSlug,
)
from render.public_api.models.flow_input_type_1 import FlowInputType1
from render.public_api.models.run_task import RunTask
from render.public_api.models.start_flow_run import StartFlowRun
from render.public_api.models.task_data_type_1 import TaskDataType1
from render.public_api.types import UNSET


def run_task_body(
    task_slug: TaskSlug,
    input_data: TaskData,
    idempotency_key: str | None,
) -> RunTask:
    """Build the request body for running a task."""
    task_input: TaskDataType1 | list[Any]
    if isinstance(input_data, dict):
        task_input = TaskDataType1.from_dict(input_data)
    else:
        task_input = input_data

    return RunTask(
        task=task_slug,
        input_=task_input,
        idempotency_key=idempotency_key if idempotency_key is not None else UNSET,
    )


def start_flow_run_body(
    flow_slug: FlowSlug,
    input_data: FlowData,
    idempotency_key: str | None,
) -> StartFlowRun:
    """Build the request body for starting a flow run."""
    flow_input: FlowInputType1 | list[Any]
    if isinstance(input_data, dict):
        flow_input = FlowInputType1.from_dict(input_data)
    else:
        flow_input = input_data

    return StartFlowRun(
        flow=flow_slug,
        input_=flow_input,
        idempotency_key=idempotency_key if idempotency_key is not None else UNSET,
    )


def list_flow_runs_query(params: ListFlowRunsParams | None) -> dict[str, Any]:
    """Translate ListFlowRunsParams into keyword arguments for list_flow_runs.

    Unset filters become UNSET so they are left out of the query string.
    """
    if params is None:
        params = ListFlowRunsParams()

    def or_unset(value: Any) -> Any:
        return value if value is not None else UNSET

    status = (
        [FlowRunStatus(s) for s in params.status]
        if params.status is not None
        else UNSET
    )

    return {
        "limit": or_unset(params.limit),
        "cursor": or_unset(params.cursor),
        "flow_slug": or_unset(params.flow_slug),
        "flow_id": or_unset(params.flow_id),
        "status": status,
        "owner_id": or_unset(params.owner_id),
        "workflow_version_id": or_unset(params.workflow_version_id),
        "workflow_id": or_unset(params.workflow_id),
    }
