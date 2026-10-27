"""Synchronous Workflows service.

This module provides the SyncWorkflowsService class for workflow-related API operations.
All methods are synchronous (blocking).
"""

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

import httpx

from render.client._requests import (
    list_flow_runs_query,
    run_task_body,
    start_flow_run_body,
)
from render.client.errors import RenderError, TaskRunError
from render.client.sse_sync import parse_stream
from render.client.types import (
    FlowData,
    FlowRun,
    FlowRunDetails,
    FlowSlug,
    ListFlowRunsParams,
    ListTaskRunsParams,
    TaskData,
    TaskRun,
    TaskRunDetails,
    TaskRunStatusValues,
    TaskSlug,
)
from render.client.util import handle_http_error, handle_httpx_exception
from render.client.util_sync import handle_http_errors, retry_with_backoff
from render.public_api.api.workflow_flows import (
    cancel_flow_run,
    get_flow_run,
    list_flow_runs,
    start_flow_run,
)
from render.public_api.api.workflow_tasks import (
    cancel_task_run,
    create_task,
    get_task_run,
    list_task_runs,
)
from render.public_api.api.workflow_tasks.stream_task_runs_events import (
    _get_kwargs,
)
from render.public_api.models.error import Error
from render.public_api.models.flow_run_with_cursor import FlowRunWithCursor
from render.public_api.models.task_run_with_cursor import TaskRunWithCursor
from render.public_api.types import UNSET, Response
from render.version import get_user_agent

if TYPE_CHECKING:
    from render.client.client import Client


class SyncWorkflowsService:
    """Synchronous service for workflow-related API operations.

    This class provides methods for running tasks and flows, getting run
    details, canceling runs, and listing runs. All methods are synchronous
    (blocking).
    """

    def __init__(self, client: "Client"):
        self.client = client

    def task_run_events(
        self,
        task_run_ids: list[str],
    ) -> Iterator[TaskRunDetails]:
        """Stream task run events via SSE.

        Args:
            task_run_ids: List of task run IDs to stream events for

        Yields:
            TaskRunDetails: Task run event updates

        Raises:
            TimeoutError: For timeout-related errors
            ClientError: For other client-side errors
            ServerError: For connection errors that might indicate server issues
        """
        kwargs = _get_kwargs(task_run_ids=task_run_ids)

        timeout = httpx.Timeout(
            connect=5.0, write=5.0, read=None, pool=None
        )  # These can be long lived
        with httpx.Client(timeout=timeout) as http_client:
            headers = kwargs.get("headers", {})
            headers.update(
                {
                    "Accept": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "User-Agent": get_user_agent(),
                }
            )
            if self.client.token:
                headers["Authorization"] = f"Bearer {self.client.token}"

            url = f"{self.client.internal._base_url}{kwargs['url']}"

            try:
                with http_client.stream(
                    method=kwargs["method"],
                    url=url,
                    params=kwargs.get("params", {}),
                    headers=headers,
                ) as response:
                    handle_http_error(response, "SSE stream")

                    yield from parse_stream(response.iter_bytes())

            except httpx.RequestError as e:
                handle_httpx_exception(e, "SSE connection")

    def start_task(
        self,
        task_slug: TaskSlug,
        input_data: TaskData,
        *,
        idempotency_key: str | None = None,
    ) -> TaskRun:
        """Start a task and return the task run without waiting for completion.

        The returned TaskRun provides the task run ID immediately.
        To wait for the result, call run_task() instead, or poll with get_task_run().

        This corresponds to POST /task-runs in the API.

        Args:
            task_slug: The task slug (workflow-slug/task-name)
            input_data: The input data for the task. Can be either:
                - A list for positional arguments: [arg1, arg2, arg3]
                - A dict for named parameters: {"param1": value1, "param2": value2}
            idempotency_key: Optional client-generated key that makes this call safe
                to retry. Repeating a call with the same key within 24 hours returns
                the task run the first call started instead of starting another one.

        Returns:
            TaskRun: The created task run

        Raises:
            ClientError: For 4xx client errors (invalid task, malformed input, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._create_task_api_call(
            task_slug, input_data, idempotency_key=idempotency_key
        ).parsed

    def run_task(
        self,
        task_slug: TaskSlug,
        input_data: TaskData,
        *,
        idempotency_key: str | None = None,
    ) -> TaskRunDetails:
        """Start a task and wait for it to complete, returning the result.

        This corresponds to POST /task-runs in the API.

        Args:
            task_slug: The task slug (workflow-slug/task-name)
            input_data: The input data for the task. Can be either:
                - A list for positional arguments: [arg1, arg2, arg3]
                - A dict for named parameters: {"param1": value1, "param2": value2}
            idempotency_key: Optional client-generated key that makes this call safe
                to retry. Repeating a call with the same key within 24 hours returns
                the task run the first call started instead of starting another one.

        Returns:
            TaskRunDetails: The completed task run details

        Raises:
            ClientError: For 4xx client errors (invalid task, malformed input, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
            TaskRunError: If the task run fails with an error
        """
        task_run = self.start_task(
            task_slug, input_data, idempotency_key=idempotency_key
        )

        # If already in a terminal state, just get the details
        status = task_run.status.value
        if status in (
            TaskRunStatusValues.COMPLETED,
            TaskRunStatusValues.FAILED,
            TaskRunStatusValues.CANCELED,
        ):
            return self.get_task_run(task_run.id)

        return retry_with_backoff(
            lambda: self._task_run_completed_with_sse(task_run.id),
            max_retries=5,
            poll_interval=1.0,
            backoff_factor=2.0,
            exempted_exceptions=(TaskRunError,),
        )

    def _task_run_completed_with_sse(self, task_run_id: str) -> TaskRunDetails:
        for event in self.task_run_events([task_run_id]):
            if event and event.id == task_run_id:
                if event.error:
                    raise TaskRunError(event.error)
                return event

        raise RenderError("Task run completed with no event")

    @handle_http_errors("create task")
    def _create_task_api_call(
        self,
        task_slug: TaskSlug,
        input_data: TaskData,
        *,
        idempotency_key: str | None = None,
    ) -> Response[Error | TaskRun]:
        """Internal method to make the create task API call."""
        run_task = run_task_body(task_slug, input_data, idempotency_key)

        # Make the API call
        return create_task.sync_detailed(
            client=self.client.internal,
            body=run_task,
        )

    def get_task_run(self, task_run_id: str) -> TaskRunDetails:
        """Get details about a specific task run.

        This corresponds to GET /task-runs/{taskRunId} in the API.

        Args:
            task_run_id: The ID of the task run to retrieve

        Returns:
            TaskRunDetails: The task run details

        Raises:
            ClientError: For 4xx client errors (task not found, invalid ID, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._get_task_run_api_call(task_run_id).parsed

    @handle_http_errors("get task run")
    def _get_task_run_api_call(
        self, task_run_id: str
    ) -> Response[Error | TaskRunDetails]:
        """Internal method to make the get task run API call."""
        return get_task_run.sync_detailed(
            client=self.client.internal,
            task_run_id=task_run_id,
        )

    def cancel_task_run(self, task_run_id: str) -> None:
        """Cancel a running task.

        This corresponds to DELETE /task-runs/{taskRunId} in the API.

        Args:
            task_run_id: The ID of the task run to cancel

        Raises:
            ClientError: For 4xx client errors (task not found, already completed, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        self._cancel_task_run_api_call(task_run_id)

        # cancel_task_run returns None on success (204 status)
        # Error objects will be handled by the decorator

    @handle_http_errors("cancel task run")
    def _cancel_task_run_api_call(self, task_run_id: str) -> Response[Any | Error]:
        """Internal method to make the cancel task run API call."""
        return cancel_task_run.sync_detailed(
            client=self.client.internal,
            task_run_id=task_run_id,
        )

    def list_task_runs(
        self,
        params: ListTaskRunsParams | None = None,
    ) -> list[TaskRunWithCursor]:
        """List task runs with optional filtering.

        This corresponds to GET /task-runs in the API.

        Args:
            params: Optional parameters for filtering the results

        Returns:
            list[TaskRunWithCursor]: List of task runs with cursor info

        Raises:
            ClientError: For 4xx client errors (invalid parameters, unauthorized, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._list_task_runs_api_call(params).parsed

    @handle_http_errors("list task runs")
    def _list_task_runs_api_call(
        self, params: ListTaskRunsParams | None = None
    ) -> Response[Error | list[TaskRunWithCursor]]:
        """Internal method to make the list task runs API call."""
        # Convert params to API parameters
        limit = params.limit if params and params.limit is not None else UNSET
        cursor = params.cursor if params and params.cursor is not None else UNSET
        owner_id = params.owner_id if params and params.owner_id is not None else UNSET

        return list_task_runs.sync_detailed(
            client=self.client.internal,
            limit=limit,
            cursor=cursor,
            owner_id=owner_id,
        )

    def start_flow(
        self,
        flow_slug: FlowSlug,
        input_data: FlowData,
        *,
        idempotency_key: str | None = None,
    ) -> FlowRun:
        """Start a flow and return the flow run without waiting for completion.

        The returned FlowRun provides the flow run ID immediately.
        Use get_flow_run() with the returned flow run's ID to check its status.

        This corresponds to POST /flow-runs in the API.

        Args:
            flow_slug: The flow slug (workflow-slug/flow-name). Append :version
                to run a specific version; otherwise the latest version runs.
            input_data: The input data for the flow. Can be either:
                - A list for positional arguments: [arg1, arg2, arg3]
                - A dict for named parameters: {"param1": value1, "param2": value2}
            idempotency_key: Optional client-generated key that makes this call safe
                to retry. Repeating a call with the same key within 24 hours returns
                the flow run the first call started instead of starting another one.

        Returns:
            FlowRun: The created flow run

        Raises:
            ClientError: For 4xx client errors (invalid flow, malformed input, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._start_flow_run_api_call(
            flow_slug, input_data, idempotency_key=idempotency_key
        ).parsed

    @handle_http_errors("start flow run")
    def _start_flow_run_api_call(
        self,
        flow_slug: FlowSlug,
        input_data: FlowData,
        *,
        idempotency_key: str | None = None,
    ) -> Response[Error | FlowRun]:
        """Internal method to make the start flow run API call."""
        return start_flow_run.sync_detailed(
            client=self.client.internal,
            body=start_flow_run_body(flow_slug, input_data, idempotency_key),
        )

    def get_flow_run(self, flow_run_id: str) -> FlowRunDetails:
        """Get details about a specific flow run.

        This corresponds to GET /flow-runs/{flowRunId} in the API.

        Args:
            flow_run_id: The ID of the flow run to retrieve

        Returns:
            FlowRunDetails: The flow run details

        Raises:
            ClientError: For 4xx client errors (flow run not found, invalid ID, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._get_flow_run_api_call(flow_run_id).parsed

    @handle_http_errors("get flow run")
    def _get_flow_run_api_call(
        self, flow_run_id: str
    ) -> Response[Error | FlowRunDetails]:
        """Internal method to make the get flow run API call."""
        return get_flow_run.sync_detailed(
            client=self.client.internal,
            flow_run_id=flow_run_id,
        )

    def cancel_flow_run(self, flow_run_id: str) -> None:
        """Cancel a running flow.

        This corresponds to DELETE /flow-runs/{flowRunId} in the API.

        Args:
            flow_run_id: The ID of the flow run to cancel

        Raises:
            ClientError: For 4xx client errors (flow run not found, already
                completed, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        self._cancel_flow_run_api_call(flow_run_id)

    @handle_http_errors("cancel flow run")
    def _cancel_flow_run_api_call(self, flow_run_id: str) -> Response[Any | Error]:
        """Internal method to make the cancel flow run API call."""
        return cancel_flow_run.sync_detailed(
            client=self.client.internal,
            flow_run_id=flow_run_id,
        )

    def list_flow_runs(
        self,
        params: ListFlowRunsParams | None = None,
    ) -> list[FlowRunWithCursor]:
        """List flow runs with optional filtering.

        This corresponds to GET /flow-runs in the API.

        Args:
            params: Optional parameters for filtering the results

        Returns:
            list[FlowRunWithCursor]: List of flow runs with cursor info

        Raises:
            ClientError: For 4xx client errors (invalid parameters, unauthorized, etc.)
            ServerError: For 5xx server errors and network failures
            TimeoutError: If the request times out
        """
        return self._list_flow_runs_api_call(params).parsed

    @handle_http_errors("list flow runs")
    def _list_flow_runs_api_call(
        self, params: ListFlowRunsParams | None = None
    ) -> Response[Error | list[FlowRunWithCursor]]:
        """Internal method to make the list flow runs API call."""
        return list_flow_runs.sync_detailed(
            client=self.client.internal,
            **list_flow_runs_query(params),
        )
