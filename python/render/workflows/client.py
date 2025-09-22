"""Unix domain socket client for communicating with the SDK server."""

import base64
import importlib.metadata
import json
from dataclasses import asdict

import aiohttp
from aiohttp import UnixConnector

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
    """Client for communicating with the SDK server over Unix Domain Socket."""

    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session with Unix socket connector."""
        if self.session is None or self.session.closed:
            connector = UnixConnector(path=self.socket_path)
            self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def disconnect(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def _send_http_request(
        self,
        method: str,
        path: str,
        data: dict | None = None,
    ) -> dict:
        """Send an HTTP request over the Unix domain socket using aiohttp."""
        session = await self._get_session()

        # Prepare headers
        headers = {
            "User-Agent": f"render-workflows-python-sdk/{version}",
            "Accept": "application/json",
        }

        # Prepare request data
        json_data = None
        if data:
            json_data = data
            headers["Content-Type"] = "application/json"

        # The URL is just the path since UnixConnector handles the socket connection
        url = f"http://localhost{path}"

        try:
            async with session.request(
                method=method,
                url=url,
                json=json_data,
                headers=headers,
            ) as response:
                # Check for HTTP errors
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")

                try:
                    return await response.json()
                except json.JSONDecodeError as e:
                    raise Exception(f"Internal error parsing JSON response: {e}") from e

        except aiohttp.ClientError as e:
            raise Exception(f"HTTP request failed: {e}") from e
        except Exception as e:
            raise Exception(f"Request error: {e}") from e

    async def get_input(self) -> TaskInput:
        """Get the task name and input for a task run."""
        response_data = await self._send_http_request("GET", "/input")
        return TaskInput(
            task_name=response_data.get("task_name", ""),
            input=response_data.get("input"),
        )

    async def post_callback(self, callback_data: CallbackData) -> CallbackResponse:
        """Send a callback to the server."""
        # Format the callback data according to the API
        if callback_data.type == CallbackType.COMPLETE:
            # Ensure result is wrapped in an array as expected by the API
            result_array = (
                [callback_data.result]
                if not isinstance(callback_data.result, list)
                else callback_data.result
            )
            result_json = json.dumps(result_array).encode("utf-8")

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
            input_json = json.dumps(callback_data.input).encode("utf-8")
            request = CallbackRequest(
                status=CallbackStatus.SUBTASK,
                subtask=SubtaskData(
                    name=callback_data.name or "",
                    input=base64.b64encode(input_json).decode("utf-8"),
                ),
            )
        else:
            raise ValueError(f"Unknown callback type: {callback_data.type}")

        # Convert to dict for HTTP request
        payload = asdict(request)
        response_data = await self._send_http_request("POST", "/callback", payload)

        return CallbackResponse(
            status=response_data.get("status", ""),
            task_run_id=response_data.get("task_run_id"),
        )

    async def register_tasks(
        self,
        tasks: list[TaskDefinition],
    ) -> TaskRegistrationResponse:
        """Register tasks with the server."""
        request = TaskRegistrationRequest(tasks=tasks)
        payload = asdict(request)
        response_data = await self._send_http_request(
            "POST",
            "/register-tasks",
            payload,
        )
        return TaskRegistrationResponse(status=response_data.get("status", ""))

    async def get_task_result(self, task_run_id: str) -> TaskResultResponse:
        """Get the result of a task run."""
        response_data = await self._send_http_request(
            "GET",
            f"/task-result?taskRunID={task_run_id}",
        )
        return TaskResultResponse(
            status=response_data.get("status", ""),
            result=response_data.get("result"),
            error=response_data.get("error"),
        )
