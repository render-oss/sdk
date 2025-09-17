"""Task executor for running tasks."""

import logging
from typing import Any

from .client import UDSClient
from .models import CallbackData, CallbackType
from .task import TaskRegistry, TaskResult

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Executes tasks received from the SDK server."""

    def __init__(self, task_registry: TaskRegistry, client: UDSClient):
        self.task_registry = task_registry
        self.client = client

    def _execute_task(self, task_name: str, input_args: list[Any]) -> Any:
        """Execute a task by name with the given input."""
        func = self.task_registry.get_function(task_name)
        if not func:
            return TaskResult(error=ValueError(f"Task '{task_name}' not found"))
        try:
            result = func(*input_args)
            return TaskResult(result=result)
        except Exception as e:
            return TaskResult(error=e)

    async def execute(self, task_name: str, input_args: list[Any]) -> Any:
        """Execute a task by name with the given input."""
        logger.info(f"Starting execution of task: {task_name}")

        sent_error = False

        try:
            # Execute the task
            result = self._execute_task(task_name, input_args)
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
        error_callback = CallbackData(type=CallbackType.ERROR, error=str(error))
        await self.client.post_callback(error_callback)

    async def _send_success_callback(self, task_name: str, result: Any):
        """Send a success callback to the server."""
        success_callback = CallbackData(type=CallbackType.COMPLETE, result=result)
        await self.client.post_callback(success_callback)
