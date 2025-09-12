"""Task executor for running tasks."""

import logging
from typing import Any, List
from .task import TaskRegistry
from .client import UDSClient
from .models import CallbackData, CallbackType

logger = logging.getLogger(__name__)

class TaskExecutor:
    """Executes tasks received from the SDK server."""

    def __init__(self, task_registry: TaskRegistry, client: UDSClient):
        self.task_registry = task_registry
        self.client = client

    async def execute(self, task_name: str, input_args: List[Any]) -> Any:
        """Execute a task by name with the given input."""
        logger.info(f"Starting execution of task: {task_name}")

        try:
            # Execute the task
            result = self.task_registry.execute_task(task_name, *input_args)
            if result.error:
                # Send error callback and raise the error
                await self._send_error_callback(task_name, result.error)
                raise result.error
            else:
                # Send success callback
                await self._send_success_callback(task_name, result.result)
                return result.result

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            # Only send error callback if we haven't already sent one
            # Check if this is a re-raised error from result.error above
            if not hasattr(e, '_callback_sent'):
                await self._send_error_callback(task_name, e)
            raise

    async def _send_error_callback(self, task_name: str, error: Exception):
        """Send an error callback to the server."""
        error_callback = CallbackData(
            type=CallbackType.ERROR,
            error=str(error)
        )
        await self.client.post_callback(error_callback)
        # Mark the error as having had a callback sent
        error._callback_sent = True

    async def _send_success_callback(self, task_name: str, result: Any):
        """Send a success callback to the server."""
        success_callback = CallbackData(
            type=CallbackType.COMPLETE,
            result=result
        )
        await self.client.post_callback(success_callback)
