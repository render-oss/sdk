"""Unix domain socket client for communicating with the SDK server."""

import base64
import importlib.metadata
import json
from dataclasses import asdict

import httpx

from render.workflows.callback_api.api.default import (
    get_input,
    post_get_subtask_result,
    post_register_tasks,
    post_run_subtask,
)
from render.workflows.callback_api.client import Client
from render.workflows.callback_api.models import (
    RunSubtaskRequest,
    SubtaskResultRequest,
    Tasks,
)
from render.workflows.callback_api.models import (
    Task as GeneratedTask,
)
from render.workflows.callback_api.types import UNSET
from render.workflows.models import (
    CallbackData,
    CallbackRequest,
    CallbackResponse,
    CallbackStatus,
    CallbackType,
    SubtaskData,
    TaskCompleteData,
    TaskDefinition,
    TaskErrorDetails,
    TaskInput,
    TaskRegistrationRequest,
    TaskRegistrationResponse,
    TaskResultResponse,
)

try:
    version = importlib.metadata.version("render")
except importlib.metadata.PackageNotFoundError:
    version = "unknown"  # fallback version


class UDSClient:
    """Client for communicating with the SDK server over Unix Domain Socket using generated API."""

    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.client = Client(base_url="http://localhost")

        # Set up transport for Unix Domain Socket
        transport = httpx.HTTPTransport(uds=socket_path)
        async_transport = httpx.AsyncHTTPTransport(uds=socket_path)

        # Create httpx clients with UDS transport and User-Agent header
        headers = {"User-Agent": f"render-workflows-python-sdk/{version}"}
        sync_client = httpx.Client(
            transport=transport,
            headers=headers,
            base_url="http://localhost"
        )
        async_client = httpx.AsyncClient(
            transport=async_transport,
            headers=headers,
            base_url="http://localhost"
        )

        # Set the clients on the generated client
        self.client.set_httpx_client(sync_client)
        self.client.set_async_httpx_client(async_client)

    async def disconnect(self):
        """Close the async httpx client."""
        if hasattr(self.client, "_async_client") and self.client._async_client is not None:
            await self.client._async_client.aclose()

    async def get_input(self) -> TaskInput:
        """Get the task name and input for a task run."""
        response = await get_input.asyncio(client=self.client)
        if response is None:
            raise Exception("Failed to get input from server")

        return TaskInput(
            task_name=response.task_name,
            input=response.input_,  # Return raw input, let the runner handle parsing
        )

    async def post_callback(self, callback_data: CallbackData) -> CallbackResponse:
        """Send a callback to the server."""
        if callback_data.type == CallbackType.COMPLETE:
            # Ensure result is wrapped in an array as expected by the API
            result_array = (
                [callback_data.result] if not isinstance(callback_data.result, list) else callback_data.result
            )
            result_json = json.dumps(result_array).encode("utf-8")

            # Create the original format request for compatibility
            request = CallbackRequest(
                status=CallbackStatus.COMPLETE,
                complete=TaskCompleteData(
                    output=base64.b64encode(result_json).decode("utf-8"),
                ),
            )
        elif callback_data.type == CallbackType.ERROR:
            request = CallbackRequest(
                status=CallbackStatus.ERROR,
                error=TaskErrorDetails(
                    details=callback_data.error or "",
                    exit_code=1,
                    is_reported_by_sdk=True,
                    is_system_err=False,
                    is_oom=False,
                    is_timeout=False,
                ),
            )
        elif callback_data.type == CallbackType.SUBTASK:
            # For subtasks, use the new run_subtask endpoint
            input_json = json.dumps(callback_data.input).encode("utf-8")
            subtask_request = RunSubtaskRequest(
                task_name=callback_data.name or "",
                input_=base64.b64encode(input_json).decode("utf-8"),
            )

            response = await post_run_subtask.asyncio(client=self.client, body=subtask_request)
            if response is None:
                raise Exception("Failed to run subtask")

            return CallbackResponse(
                status="ok",
                task_run_id=response.task_run_id,
            )
        else:
            raise ValueError(f"Unknown callback type: {callback_data.type}")

        # Send using the original format through httpx directly
        payload = asdict(request)

        # Make the request using the underlying httpx client
        response = await self.client.get_async_httpx_client().post(
            "/callback",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code >= 400:
            error_text = response.text
            raise Exception(f"HTTP {response.status_code}: {error_text}")

        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            # If response is empty or not JSON, that might be OK for callbacks
            response_data = {}

        return CallbackResponse(
            status=response_data.get("status", "ok"),
            task_run_id=response_data.get("task_run_id"),
        )

    async def register_tasks(
        self,
        tasks: list[TaskDefinition],
    ) -> TaskRegistrationResponse:
        """Register tasks with the server."""
        generated_tasks = [GeneratedTask(name=task.name) for task in tasks]

        tasks_request = Tasks(tasks=generated_tasks)
        await post_register_tasks.asyncio_detailed(client=self.client, body=tasks_request)

        return TaskRegistrationResponse(status="ok")

    async def get_task_result(self, task_run_id: str) -> TaskResultResponse:
        """Get the result of a task run."""
        subtask_result_request = SubtaskResultRequest(task_run_id=task_run_id)

        response = await post_get_subtask_result.asyncio(client=self.client, body=subtask_result_request)

        if response is None:
            raise Exception("Failed to get task result")

        # Check if task is still running
        if response.still_running:
            return TaskResultResponse(
                status="running",
                result=None,
                error=None,
            )

        # Check if there was an error
        if not isinstance(response.error, UNSET) and response.error is not None:
            return TaskResultResponse(
                status="error",
                result=None,
                error=response.error.details,
            )

        # Check if task completed successfully
        if not isinstance(response.complete, UNSET) and response.complete is not None:
            result = None
            if response.complete.output:
                try:
                    result = json.loads(base64.b64decode(response.complete.output).decode("utf-8"))
                except (json.JSONDecodeError, ValueError) as e:
                    raise Exception(f"Failed to decode task result: {e}")

            return TaskResultResponse(
                status="complete",
                result=result,
                error=None,
            )

        # Default case
        return TaskResultResponse(
            status="unknown",
            result=None,
            error="Unknown task status",
        )
