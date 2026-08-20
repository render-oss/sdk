"""Task executor for running tasks."""

import inspect
import logging
from typing import Any

from render_sdk.workflows.client import CallbackRequest, Status, UDSClient
from render_sdk.workflows.context import WorkflowTaskContext
from render_sdk.workflows.task import TaskRegistry, TaskResult

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Executes tasks received from the SDK server."""

    def __init__(self, task_registry: TaskRegistry, client: UDSClient):
        self.task_registry = task_registry
        self.client = client

    async def _execute_task(
        self, task_name: str, input_data: list[Any] | dict[str, Any]
    ) -> Any:
        """Execute a task by name with the given input."""
        func = self.task_registry.get_function(task_name)
        if not func:
            return TaskResult(error=ValueError(f"Task '{task_name}' not found"))

        # The context is always the first argument; the wire input holds the rest.
        ctx = WorkflowTaskContext(self.client)

        try:
            # Determine how to call the function based on input type
            if isinstance(input_data, dict):
                # Named parameters: pass as keyword arguments
                result = func(ctx, **input_data)
            else:
                # Positional parameters: unpack list
                result = func(ctx, *input_data)

            if inspect.isawaitable(result):
                result = await result

            return TaskResult(result=result)

        except Exception as e:
            return TaskResult(error=e)

    async def execute(
        self, task_name: str, input_data: list[Any] | dict[str, Any]
    ) -> Any:
        """Execute a task by name with the given input."""
        logger.debug(f"Starting execution of task: {task_name}")

        sent_error = False

        try:
            # Execute the task
            result = await self._execute_task(task_name, input_data)
            if result.error:
                # Send error callback and raise the error
                await self._send_error_callback(task_name, result.error)
                sent_error = True
                raise result.error
            # Send success callback
            await self._send_success_callback(task_name, result.result)
            return result.result

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            # Only send error callback if we haven't already sent one
            # Check if this is a re-raised error from result.error above
            if not sent_error:
                await self._send_error_callback(task_name, e)
                sent_error = True
            raise

    async def _send_error_callback(self, task_name: str, error: Exception):
        """Send an error callback to the server."""
        error_callback = CallbackRequest(status=Status.ERROR, error=str(error))
        await self.client.post_callback(error_callback)

    async def _send_success_callback(self, task_name: str, result: Any):
        """Send a success callback to the server."""
        success_callback = CallbackRequest(status=Status.SUCCESS, result=result)
        await self.client.post_callback(success_callback)
