"""Workflows service

This module provides the WorkflowsService class for workflow-related API operations.
It mirrors the functionality of the Go WorkflowsService.
"""

from typing import TYPE_CHECKING, Any

from render.client.types import (
    ListTaskRunsParams,
    TaskData,
    TaskIdentifier,
    TaskRun,
    TaskRunDetails,
    TaskRunStatusValues,
)
from render.client.util import retry_with_backoff
from render.public_api.api.workflows import (
    create_task,
    cancel_task_run,
    get_task_run,
    list_task_runs,
)
from render.public_api.models.error import Error
from render.public_api.models.run_task import RunTask
from render.client.util import handle_http_errors
from render.public_api.types import Response
from render.client.errors import TaskRunError

if TYPE_CHECKING:
    from render.client.client import Client


class AwaitableTaskRun:
    """TaskRun with awaitable functionality for waiting on completion.

    This class wraps a TaskRun and makes it awaitable, so you can use:
    `result = await task_run`
    """

    def __init__(self, task_run: TaskRun, workflows_service: "WorkflowsService"):
        self.task_run = task_run
        self.workflows_service = workflows_service
        self._details: TaskRunDetails | None = None

    @property
    def id(self) -> str:
        """Get the task run ID."""
        return self.task_run.id

    @property
    def status(self) -> str:
        """Get the current task run status."""
        return self.task_run.status.value

    def is_terminal_status(self) -> bool:
        """Check if the task run is in a terminal state."""
        return self.status in (
            TaskRunStatusValues.COMPLETED,
            TaskRunStatusValues.FAILED,
        )

    def __await__(self):
        """Make AwaitableTaskRun awaitable directly."""
        return self._wait_for_completion().__await__()

    async def _wait_for_completion(self) -> TaskRunDetails:
        """Internal method to wait for task completion.

        Returns:
            TaskRunDetails: The final task run details

        Raises:
            Exception: If the task run fails or API calls fail
        """
        # If already completed, get current details and return
        if self.is_terminal_status():
            return await self.workflows_service.get_task_run(self.id)

        return await retry_with_backoff(
            self._task_run_completed_with_sse,
            max_retries=5,
            poll_interval=1.0,
            backoff_factor=2.0,
            exempted_exceptions=(TaskRunError,),
        )

    async def _task_run_completed_with_sse(self) -> tuple[TaskRunDetails, bool]:
        async for event in self.workflows_service.client.sse.stream_task_run_events([self.id]):
            if event and event.id == self.id:
                # Update our internal state
                self.task_run = event

                if event.error:
                    raise TaskRunError(event.error)

                return event


class WorkflowsService:
    """Service for workflow-related API operations.

    This class provides methods for running tasks, getting task run details,
    canceling tasks, and listing task runs.
    """

    def __init__(self, client: "Client"):
        self.client = client

    async def run_task(
        self,
        task_identifier: TaskIdentifier,
        input_data: TaskData,
    ) -> AwaitableTaskRun:
        """Execute a task using the workflows API.

        This corresponds to POST /task-runs in the API.

        Args:
            task_identifier: The identifier of the task to run
            input_data: The input data for the task

        Returns:
            AwaitableTaskRun: An awaitable task run object

        Raises:
            Exception: If the API request fails
        """
        response = (await self._create_task_api_call(task_identifier, input_data)).parsed

        # Return wrapped task run with awaitable functionality
        return AwaitableTaskRun(response, self)

    @handle_http_errors("create task")
    async def _create_task_api_call(self, task_identifier: TaskIdentifier, input_data: TaskData) -> Response[Error | TaskRun]:
        """Internal method to make the create task API call."""
        # Create the request body
        run_task = RunTask(
            task=task_identifier,
            input_=input_data,
        )

        # Make the API call
        return await create_task.asyncio_detailed(
            client=self.client.internal,
            body=run_task,
        )

    async def get_task_run(self, task_run_id: str) -> TaskRunDetails:
        """Get details about a specific task run.

        This corresponds to GET /task-runs/{taskRunId} in the API.

        Args:
            task_run_id: The ID of the task run to retrieve

        Returns:
            TaskRunDetails: The task run details

        Raises:
            Exception: If the API request fails
        """
        return (await self._get_task_run_api_call(task_run_id)).parsed

    @handle_http_errors("get task run")
    async def _get_task_run_api_call(self, task_run_id: str) -> Response[Error | TaskRunDetails]:
        """Internal method to make the get task run API call."""
        return await get_task_run.asyncio_detailed(
            client=self.client.internal,
            task_run_id=task_run_id,
        )

    async def cancel_task_run(self, task_run_id: str) -> None:
        """Cancel a running task.

        This corresponds to DELETE /task-runs/{taskRunId} in the API.

        Args:
            task_run_id: The ID of the task run to cancel

        Raises:
            Exception: If the API request fails
        """
        await self._cancel_task_run_api_call(task_run_id)

        # cancel_task_run returns None on success (204 status)
        # Error objects will be handled by the decorator

    @handle_http_errors("cancel task run")
    async def _cancel_task_run_api_call(self, task_run_id: str) -> Response[Any | Error]:
        """Internal method to make the cancel task run API call."""
        return await cancel_task_run.asyncio_detailed(
            client=self.client.internal,
            task_run_id=task_run_id,
        )

    async def list_task_runs(
        self,
        params: ListTaskRunsParams | None = None,
    ) -> list[TaskRun]:
        """List task runs with optional filtering.

        This corresponds to GET /task-runs in the API.

        Args:
            params: Optional parameters for filtering the results

        Returns:
            list[TaskRun]: List of task runs

        Raises:
            Exception: If the API request fails
        """
        return (await self._list_task_runs_api_call(params)).parsed

    @handle_http_errors("list task runs")
    async def _list_task_runs_api_call(self, params: ListTaskRunsParams | None = None) -> Response[Error | list[TaskRun]]:
        """Internal method to make the list task runs API call."""
        # Convert params to API parameters
        limit = params.limit if params else None
        cursor = params.cursor if params else None
        owner_id = params.owner_id if params else None

        return await list_task_runs.asyncio_detailed(
            client=self.client.internal,
            limit=limit,
            cursor=cursor,
            owner_id=owner_id,
        )
