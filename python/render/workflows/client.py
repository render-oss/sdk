"""Unix domain socket client for communicating with the SDK server."""

import asyncio
import base64
import importlib.metadata
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any

import httpx

from render.client.errors import RenderError, TaskRunError
from render.client.util import handle_http_errors
from render.workflows.callback_api.api.default import (
    get_input,
    post_callback,
    post_get_subtask_result,
    post_register_tasks,
    post_run_subtask,
)
from render.workflows.callback_api.client import Client
from render.workflows.callback_api.models import (
    CallbackRequest as GeneratedCallbackRequest,
)
from render.workflows.callback_api.models import (
    InputResponse,
    RunSubtaskRequest,
    RunSubtaskResponse,
    SubtaskResultRequest,
    TaskComplete,
    TaskError,
    Tasks,
)
from render.workflows.callback_api.models.subtask_result_response import (
    SubtaskResultResponse,
)
from render.workflows.callback_api.types import Response, Unset


class Status(Enum):
    RUNNING = "running"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class TaskResultResponse:
    """Response when requesting task results."""

    status: Status
    result: Any | None = None
    error: str | None = None


@dataclass
class CallbackRequest:
    status: Status
    result: Any | None = None
    error: str | None = None


POLLING_INTERVAL = 1.0

try:
    version = importlib.metadata.version("render")
except importlib.metadata.PackageNotFoundError:
    version = "unknown"  # fallback version


class UDSClient:
    """Client for communicating with the SDK server over Unix Domain Socket."""

    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.client = Client(base_url="http://localhost")

        # Set up transport for Unix Domain Socket
        transport = httpx.HTTPTransport(uds=socket_path)
        async_transport = httpx.AsyncHTTPTransport(uds=socket_path)

        # Create httpx clients with UDS transport and User-Agent header
        headers = {"User-Agent": f"render-workflows-python-sdk/{version}"}
        sync_client = httpx.Client(
            transport=transport, headers=headers, base_url="http://localhost"
        )
        async_client = httpx.AsyncClient(
            transport=async_transport, headers=headers, base_url="http://localhost"
        )

        # Set the clients on the generated client
        self.client.set_httpx_client(sync_client)
        self.client.set_async_httpx_client(async_client)

    async def disconnect(self):
        """Close the async httpx client."""
        if (
            hasattr(self.client, "_async_client")
            and self.client._async_client is not None
        ):
            await self.client._async_client.aclose()
        if hasattr(self.client, "_client") and self.client._client is not None:
            self.client._client.close()

    async def get_input(self) -> InputResponse:
        """Get the task name and input for a task run."""
        response = await get_input.asyncio(client=self.client)

        return response

    async def post_callback(self, callback_request: CallbackRequest) -> None:
        """Send a callback to the server."""
        data: GeneratedCallbackRequest

        if callback_request.status == Status.SUCCESS:
            # Ensure result is wrapped in an array as expected by the API
            result_array = (
                [callback_request.result]
                if not isinstance(callback_request.result, list)
                else callback_request.result
            )
            result_json = json.dumps(result_array).encode("utf-8")

            data = GeneratedCallbackRequest(
                complete=TaskComplete(
                    output=base64.b64encode(result_json).decode("utf-8")
                )
            )
        elif callback_request.status == Status.ERROR:
            data = GeneratedCallbackRequest(
                error=TaskError(details=callback_request.error)
            )

        # Send using the generated API
        await self._post_callback_api_call(data)

    @handle_http_errors("post callback")
    async def _post_callback_api_call(
        self, data: GeneratedCallbackRequest
    ) -> Response[Any]:
        """Internal method to make the post callback API call."""
        return await post_callback.asyncio_detailed(client=self.client, body=data)

    async def run_subtask(self, task_name: str, input_data: any = None) -> any:
        """
        Run a subtask and wait for its completion.

        Args:
            task_name: Name of the task to run
            input_data: Input data to pass to the task

        Returns:
            The result of the subtask execution
        """
        # Encode input data as base64 JSON
        input_json = json.dumps(input_data if input_data is not None else []).encode(
            "utf-8"
        )
        subtask_request = RunSubtaskRequest(
            task_name=task_name,
            input_=base64.b64encode(input_json).decode("utf-8"),
        )

        # Start the subtask
        response = (await self._run_subtask_api_call(subtask_request)).parsed

        task_run_id = response.task_run_id

        # Poll for completion
        while True:
            result = await self.get_task_result(task_run_id)

            if result.status == Status.SUCCESS:
                # Extract the actual value from the array
                actual_result = result.result
                if isinstance(actual_result, list) and len(actual_result) == 1:
                    return actual_result[0]
                return actual_result
            elif result.status == Status.ERROR:
                raise TaskRunError(f"Subtask failed: {result.error}")
            elif result.status == Status.RUNNING:
                # Wait a bit before polling again
                await asyncio.sleep(POLLING_INTERVAL)
            else:
                raise RenderError(f"Unknown subtask status: {result.status}")

    @handle_http_errors("run subtask")
    async def _run_subtask_api_call(
        self, body: RunSubtaskRequest
    ) -> Response[Any | RunSubtaskResponse]:
        return await post_run_subtask.asyncio_detailed(client=self.client, body=body)

    async def register_tasks(
        self,
        tasks: Tasks,
    ) -> None:
        """Register tasks with the server."""
        await self._register_tasks_api_call(tasks)

    @handle_http_errors("register tasks")
    async def _register_tasks_api_call(self, tasks: Tasks) -> Response[Any]:
        """Internal method to make the register tasks API call."""
        return await post_register_tasks.asyncio_detailed(
            client=self.client, body=tasks
        )

    async def get_task_result(self, task_run_id: str) -> TaskResultResponse:
        """Get the result of a task run."""
        subtask_result_request = SubtaskResultRequest(task_run_id=task_run_id)

        response = (await self._get_task_result_api_call(subtask_result_request)).parsed

        # Check if task is still running
        if response.still_running:
            return TaskResultResponse(
                status=Status.RUNNING,
                result=None,
                error=None,
            )

        # Check if there was an error
        if not isinstance(response.error, Unset) and response.error is not None:
            return TaskResultResponse(
                status=Status.ERROR,
                result=None,
                error=response.error.details,
            )

        # Check if task completed successfully
        if not isinstance(response.complete, Unset) and response.complete is not None:
            result = None
            if response.complete.output:
                try:
                    result = json.loads(
                        base64.b64decode(response.complete.output).decode("utf-8")
                    )
                except (json.JSONDecodeError, ValueError) as e:
                    raise RenderError(f"Failed to decode task result: {e}") from e

            return TaskResultResponse(
                status=Status.SUCCESS,
                result=result,
                error=None,
            )

        raise RenderError("Unknown task status")

    @handle_http_errors("get task result")
    async def _get_task_result_api_call(
        self, body: SubtaskResultRequest
    ) -> Response[Any | SubtaskResultResponse]:
        """Internal method to make the get task result API call."""
        return await post_get_subtask_result.asyncio_detailed(
            client=self.client, body=body
        )
