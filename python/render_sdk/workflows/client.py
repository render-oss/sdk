"""Unix domain socket client for communicating with the SDK server.

Uses a hand-rolled HTTP/UDS transport (``_uds_http``) and hand-rolled
data models (``_callback_models``) so this module — which is on the
worker hot path — does not pull in ``httpx`` or ``attrs`` at import
time.

Error translation from raw transport exceptions to
``render_sdk.client.errors`` types lives in the :func:`_translate_errors`
decorator, applied per public method together with
:func:`_retry_transient_errors`. That keeps ``_uds_http.py`` unaware of
domain error vocabulary and operation labels.
"""

import asyncio
import base64
import functools
import http.client
import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from render_sdk.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
    TaskRunError,
)
from render_sdk.client.errors import TimeoutError as SdkTimeoutError
from render_sdk.version import get_user_agent
from render_sdk.workflows._callback_models import CallbackRequest as ApiCallbackRequest
from render_sdk.workflows._callback_models import (
    InputResponse,
    RunSubtaskRequest,
    RunSubtaskResponse,
    SubtaskResultRequest,
    SubtaskResultResponse,
    TaskComplete,
    TaskError,
    Tasks,
    Unset,
)
from render_sdk.workflows._uds_http import HttpStatusError, request_json

logger = logging.getLogger(__name__)


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
POLLING_TIMEOUT = 24 * 60 * 60  # 24 hours
QUERY_TIMEOUT = 15  # 15 seconds

# Total retry window is ~5 minutes (303.75 seconds)
_UDS_MAX_RETRIES = 25
_UDS_INITIAL_DELAY_S = 0.25
_UDS_BACKOFF_FACTOR = 2.0
_UDS_MAX_DELAY_S = 16.0


def _retry_transient_errors(func: Callable[..., Awaitable[Any]]):
    """Retry async functions on transient UDS errors.

    Retries on ``ServerError`` (5xx, connection errors), our
    ``TimeoutError``, and ``RateLimitError`` (429). Does not retry on
    ``ClientError`` (4xx) or other exceptions. Stacked OUTSIDE
    :func:`_translate_errors` so it sees translated typed errors, not raw
    transport exceptions.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        last_error: Exception | None = None
        for attempt in range(_UDS_MAX_RETRIES):
            try:
                return await func(*args, **kwargs)
            except (ServerError, SdkTimeoutError, RateLimitError) as e:
                last_error = e
                if attempt < _UDS_MAX_RETRIES - 1:
                    delay = min(
                        _UDS_INITIAL_DELAY_S * (_UDS_BACKOFF_FACTOR**attempt),
                        _UDS_MAX_DELAY_S,
                    )
                    logger.warning(
                        "Request to Render failed (%d/%d), retry in %.1fs: %s",
                        attempt + 1,
                        _UDS_MAX_RETRIES,
                        delay,
                        e,
                    )
                    await asyncio.sleep(delay)
        if last_error is not None:
            raise last_error

    return wrapper


def _extract_status_message(body: bytes) -> str | None:
    """Best-effort extraction of an error message from an HTTP error body.

    Tries JSON ``{"message": ...}`` / ``{"error": ...}`` first, then falls
    back to the raw body as UTF-8. Returns ``None`` if nothing usable is
    found.
    """
    if not body:
        return None
    try:
        payload = json.loads(body)
        if isinstance(payload, dict):
            raw = payload.get("message") or payload.get("error")
            if isinstance(raw, str):
                return raw
    except (ValueError, UnicodeDecodeError):
        pass
    try:
        return body.decode("utf-8", errors="replace").strip() or None
    except Exception:  # pragma: no cover - defensive
        return None


def _translate_errors(operation: str) -> Callable[[Callable], Callable]:
    """Translate raw transport exceptions into render_sdk.client.errors types.

    The transport in ``_uds_http`` raises stdlib exceptions plus
    :class:`HttpStatusError`. This decorator turns those into the
    appropriate typed error with the operation label baked into the
    message, so callers see a consistent error vocabulary regardless of
    which transport-level failure occurred.
    """

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            # `socket.timeout` is an alias for the built-in ``TimeoutError``;
            # our domain timeout is imported as ``SdkTimeoutError`` so the
            # built-in name stays free for catching.
            except TimeoutError as e:
                raise SdkTimeoutError(f"{operation} timed out: {e}") from e
            except (ConnectionError, FileNotFoundError) as e:
                raise ServerError(f"{operation} failed to connect: {e}") from e
            except http.client.HTTPException as e:
                raise ServerError(f"{operation} got invalid HTTP response: {e}") from e
            except HttpStatusError as e:
                message = _extract_status_message(e.body)
                full = f"{operation} failed with status {e.status}"
                if message:
                    full = f"{full}: {message}"
                if e.status == 429:
                    raise RateLimitError(full) from e
                if e.status < 500:
                    raise ClientError(full) from e
                raise ServerError(full) from e
            except json.JSONDecodeError as e:
                raise RenderError(f"{operation} failed: non-JSON response: {e}") from e
            except OSError as e:
                raise ServerError(f"{operation} network error: {e}") from e

        return wrapper

    return decorator


class UDSClient:
    """Client for communicating with the SDK server over Unix Domain Socket."""

    def __init__(self, socket_path: str):
        self.socket_path = socket_path

    async def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
    ) -> Any:
        """Bundle the per-call constants (user agent, timeout, socket path).

        This carries no error translation — that lives on the public
        methods via :func:`_translate_errors`. Each public method is
        responsible for asserting the response shape it expects.
        """
        return await request_json(
            socket_path=self.socket_path,
            method=method,
            path=path,
            body=body,
            user_agent=get_user_agent(),
            timeout=QUERY_TIMEOUT,
        )

    @_retry_transient_errors
    @_translate_errors("get input")
    async def get_input(self) -> InputResponse:
        """Get the task name and input for a task run."""
        payload = await self._request("GET", "/input", None)
        if not isinstance(payload, dict):
            raise RenderError(f"get input failed: unexpected response: {payload!r}")
        return InputResponse.from_dict(payload)

    @_retry_transient_errors
    @_translate_errors("post callback")
    async def post_callback(self, callback_request: CallbackRequest) -> None:
        """Send a callback to the server."""
        if callback_request.status == Status.SUCCESS:
            # Wire format expects results to be wrapped in an array.
            result_array = (
                [callback_request.result]
                if not isinstance(callback_request.result, list)
                else callback_request.result
            )
            result_json = json.dumps(result_array).encode()
            data = ApiCallbackRequest(
                complete=TaskComplete(output=base64.b64encode(result_json).decode())
            )
        elif (
            callback_request.status == Status.ERROR
            and callback_request.error is not None
        ):
            data = ApiCallbackRequest(error=TaskError(details=callback_request.error))
        else:
            data = ApiCallbackRequest()

        await self._request("POST", "/callback", data.to_dict())

    async def run_subtask(
        self, task_name: str, input_data: list[Any] | dict[str, Any] | None = None
    ) -> Any:
        """
        Run a subtask and wait for its completion.

        Args:
            task_name: Name of the task to run
            input_data: Input data to pass to the task. Can be either:
                - A list for positional arguments: [arg1, arg2, arg3]
                - A dict for named parameters: {"param1": value1, "param2": value2}

        Returns:
            The result of the subtask execution
        """
        # Encode input data as base64 JSON
        input_json = json.dumps(input_data if input_data is not None else []).encode()
        subtask_request = RunSubtaskRequest(
            task_name=task_name,
            input_=base64.b64encode(input_json).decode(),
        )

        response = await self._start_subtask(subtask_request)
        task_run_id = response.task_run_id

        start_time = time.time()
        while time.time() - start_time < POLLING_TIMEOUT:
            result = await self.get_task_result(task_run_id)

            if result.status == Status.SUCCESS:
                actual_result = result.result
                if isinstance(actual_result, list) and len(actual_result) == 1:
                    return actual_result[0]
                return actual_result
            elif result.status == Status.ERROR:
                raise TaskRunError(f"Subtask failed: {result.error}")
            elif result.status == Status.RUNNING:
                await asyncio.sleep(POLLING_INTERVAL)
            else:
                raise RenderError(f"Unknown subtask status: {result.status}")

    @_retry_transient_errors
    @_translate_errors("run subtask")
    async def _start_subtask(
        self, subtask_request: RunSubtaskRequest
    ) -> RunSubtaskResponse:
        payload = await self._request("POST", "/run-subtask", subtask_request.to_dict())
        if not isinstance(payload, dict):
            raise RenderError(f"run subtask failed: unexpected response: {payload!r}")
        return RunSubtaskResponse.from_dict(payload)

    @_retry_transient_errors
    @_translate_errors("register tasks")
    async def register_tasks(self, tasks: Tasks) -> None:
        """Register tasks with the server."""
        await self._request("POST", "/register-tasks", tasks.to_dict())

    @_retry_transient_errors
    @_translate_errors("get task result")
    async def get_task_result(self, task_run_id: str) -> TaskResultResponse:
        """Get the result of a task run."""
        subtask_result_request = SubtaskResultRequest(task_run_id=task_run_id)

        payload = await self._request(
            "POST", "/get-subtask-result", subtask_result_request.to_dict()
        )
        if not isinstance(payload, dict):
            raise RenderError(
                f"get task result failed: unexpected response: {payload!r}"
            )
        response = SubtaskResultResponse.from_dict(payload)

        if response.still_running:
            return TaskResultResponse(status=Status.RUNNING)

        if not isinstance(response.error, Unset) and response.error is not None:
            return TaskResultResponse(
                status=Status.ERROR,
                error=response.error.details,
            )

        if not isinstance(response.complete, Unset) and response.complete is not None:
            result: Any | None = None
            if response.complete.output:
                try:
                    result = json.loads(
                        base64.b64decode(response.complete.output).decode()
                    )
                except (json.JSONDecodeError, ValueError) as e:
                    raise RenderError(f"Failed to decode task result: {e}") from e
            return TaskResultResponse(status=Status.SUCCESS, result=result)

        raise RenderError("Unknown task status")
