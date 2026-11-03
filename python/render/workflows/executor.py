"""Task executor for running tasks."""

import inspect
import logging
from collections.abc import Callable
from contextlib import nullcontext
from typing import Any

from render.client.errors import (
    ExecutionError,
    FlowCancelledError,
    FlowUnreachableError,
)
from render.workflows._models.task import InputResponse
from render.workflows.client import CallbackRequest, Status, UDSClient
from render.workflows.context import (
    FlowContext,
    TaskContext,
    WorkflowTaskContext,
)
from render.workflows.durable_context import DurableFlowContext
from render.workflows.task import TaskRegistry, TaskResult

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Executes tasks received from the SDK server."""

    def __init__(self, task_registry: TaskRegistry, client: UDSClient):
        self.task_registry = task_registry
        self.client = client

    async def _execute_task(
        self,
        task_name: str,
        input_data: list[Any] | dict[str, Any],
        input_response: InputResponse | None = None,
    ) -> Any:
        """Execute a task by name with the given input."""
        task_info = self.task_registry.get_task(task_name)
        if not task_info:
            return TaskResult(error=ValueError(f"Task '{task_name}' not found"))
        func = task_info.func

        is_workflow = bool(input_response and input_response.is_workflow)
        if is_workflow != task_info.workflow:
            registered_as = "a flow" if task_info.workflow else "a plain task"
            started_as = "a flow" if is_workflow else "a plain task"
            return TaskResult(
                error=ValueError(
                    f"'{task_name}' is registered as {registered_as}, but this "
                    f"run was started as {started_as}"
                )
            )
        if input_response and is_workflow:
            ctx = DurableFlowContext(self.client, input_response)
            return await self._call(func, ctx, input_data)
        task_ctx = WorkflowTaskContext(self.client, input_response)
        return await self._call(func, task_ctx, input_data)

    async def _call(
        self,
        func: Callable[..., Any],
        ctx: TaskContext | FlowContext,
        input_data: list[Any] | dict[str, Any],
    ) -> TaskResult:
        # The context is always the first argument; the wire input holds the rest.
        try:
            # A flow's error passes through its context, which checks the
            # run against its history on the way out.
            with ctx if isinstance(ctx, DurableFlowContext) else nullcontext():
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

        except ExecutionError as e:
            # Only the run failure the context recorded is one of ours.
            if isinstance(ctx, DurableFlowContext) and e is ctx.run_failure:
                return TaskResult(error=e)
            # Any other came from user code, so it's reported as a plain error
            # and can't pose as one of ours.
            error = RuntimeError(str(e))
            error.__cause__ = e
            return TaskResult(error=error)
        except Exception as e:
            return TaskResult(error=e)

    async def execute(
        self,
        task_name: str,
        input_data: list[Any] | dict[str, Any],
        *,
        input_response: InputResponse | None = None,
    ) -> Any:
        """Execute a task by name with the given input."""
        logger.debug(f"Starting execution of task: {task_name}")

        try:
            result = await self._execute_task(task_name, input_data, input_response)
            if result.error is not None:
                raise result.error
            await self._send_success_callback(task_name, result.result)
            return result.result
        except FlowCancelledError:
            # The run's outcome isn't this attempt's to report.
            raise
        except FlowUnreachableError as e:
            # Render caused this failure, so the callback says so and the run
            # recovers. If the callback can't get through either, the attempt
            # exits without one.
            logger.error(f"Lost contact with the workflow system: {e}")
            try:
                await self.client.post_callback(e.to_callback_request())
            except Exception:
                logger.warning("Could not report the lost contact", exc_info=True)
            raise
        except Exception as e:
            # Any other failure fails the run.
            logger.error(f"Task execution failed: {e}")
            # Our own errors say how renderd should read them; any other is an
            # ordinary task error.
            await self.client.post_callback(
                e.to_callback_request()
                if isinstance(e, ExecutionError)
                else CallbackRequest(status=Status.ERROR, error=str(e))
            )
            raise

    async def _send_success_callback(self, task_name: str, result: Any):
        """Send a success callback to the server."""
        success_callback = CallbackRequest(status=Status.SUCCESS, result=result)
        await self.client.post_callback(success_callback)
