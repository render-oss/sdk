"""Unix domain socket client for communicating with the SDK server.

Uses a hand-rolled HTTP/UDS transport (``_uds_http``) and hand-rolled
data models (``_models``) so this module — which is on the
worker hot path — does not pull in ``httpx`` or ``attrs`` at import
time.

Error translation from raw transport exceptions to
``render.client.errors`` types lives in the :func:`_translate_errors`
decorator, applied per public method together with
:func:`_retry_transient_errors`. That keeps ``_uds_http.py`` unaware of
domain error vocabulary and operation labels.
"""

import asyncio
import base64
import contextlib
import functools
import http.client
import json
import logging
import time
import uuid
from collections.abc import Awaitable, Callable, Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, ParamSpec, TypeVar

from render import _startup
from render.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
    TaskRunError,
)
from render.client.errors import TimeoutError as SdkTimeoutError
from render.version import get_user_agent
from render.workflows._models.registration import Tasks
from render.workflows._models.step import (
    StepAttemptRequest,
    StepAttemptResponse,
    StepCompleteRequest,
    StepCompleteResponse,
    StepStartRequest,
    StepStartResponse,
)
from render.workflows._models.subtask import (
    RunSubtaskRequest,
    RunSubtaskResponse,
    SubtaskResultRequest,
    SubtaskResultResponse,
)
from render.workflows._models.task import CallbackRequest as ApiCallbackRequest
from render.workflows._models.task import (
    DeterminismDetails,
    InputResponse,
    TaskComplete,
    TaskError,
    TaskErrorReason,
)
from render.workflows._models.wire import Unset
from render.workflows._uds_http import (
    HttpStatusError,
    request_json,
    request_json_sync,
)

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


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
    # Why the task failed, when it's more than an ordinary task error.
    reason: TaskErrorReason | None = None
    # Set when a flow replay diverged from its history.
    determinism: DeterminismDetails | None = None
    # For a flow limit: the limit, and the value that exceeded it.
    limit: int | None = None
    value: int | None = None


POLLING_INTERVAL = 1.0
POLLING_TIMEOUT = 24 * 60 * 60  # 24 hours
QUERY_TIMEOUT = 15  # 15 seconds

# Total retry window is ~5 minutes (303.75 seconds)
_UDS_MAX_RETRIES = 25
_UDS_INITIAL_DELAY_S = 0.25
_UDS_BACKOFF_FACTOR = 2.0
_UDS_MAX_DELAY_S = 16.0


def _retry_transient_errors(
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    """Retry async functions on transient UDS errors.

    Retries on ``ServerError`` (5xx, connection errors), our
    ``TimeoutError``, and ``RateLimitError`` (429). Does not retry on
    ``ClientError`` (4xx) or other exceptions. Stacked OUTSIDE
    :func:`_translate_errors` so it sees translated typed errors, not raw
    transport exceptions.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for attempt in range(_UDS_MAX_RETRIES):
            try:
                return await func(*args, **kwargs)
            except (ServerError, SdkTimeoutError, RateLimitError) as e:
                if attempt >= _UDS_MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(_retry_delay(attempt, e))
        raise AssertionError("unreachable")  # pragma: no cover

    return wrapper


def _retry_transient_errors_sync(func: Callable[P, R]) -> Callable[P, R]:
    """Blocking :func:`_retry_transient_errors`, for flow step writes."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for attempt in range(_UDS_MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except (ServerError, SdkTimeoutError, RateLimitError) as e:
                if attempt >= _UDS_MAX_RETRIES - 1:
                    raise
                time.sleep(_retry_delay(attempt, e))
        raise AssertionError("unreachable")  # pragma: no cover

    return wrapper


def _retry_delay(attempt: int, e: Exception) -> float:
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
    return delay


def _decode_body(body: bytes) -> tuple[str | None, dict[str, Any] | None]:
    """An HTTP error body's message and its decoded JSON object.

    The message is best effort: JSON ``{"message": ...}`` /
    ``{"error": ...}`` first, then the raw body as UTF-8. Either is ``None``
    when the body has nothing usable.
    """
    if not body:
        return None, None
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        payload = None
    json_body = payload if isinstance(payload, dict) else None
    if json_body is not None:
        raw = json_body.get("message") or json_body.get("error")
        if isinstance(raw, str):
            return raw, json_body
    try:
        return body.decode("utf-8", errors="replace").strip() or None, json_body
    except Exception:  # pragma: no cover - defensive
        return None, json_body


def _translate_errors(
    operation: str,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Translate raw transport exceptions into render.client.errors types.

    The transport in ``_uds_http`` raises stdlib exceptions plus
    :class:`HttpStatusError`. This decorator turns those into the
    appropriate typed error with the operation label baked into the
    message, so callers see a consistent error vocabulary regardless of
    which transport-level failure occurred.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with _translated(operation):
                return await func(*args, **kwargs)
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper

    return decorator


def _translate_errors_sync(
    operation: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Blocking :func:`_translate_errors`, for flow step writes."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with _translated(operation):
                return func(*args, **kwargs)
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper

    return decorator


@contextlib.contextmanager
def _translated(operation: str) -> Iterator[None]:
    try:
        yield
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
        message, json_body = _decode_body(e.body)
        full = f"{operation} failed with status {e.status}"
        if message:
            full = f"{full}: {message}"
        if e.status == 429:
            raise RateLimitError(full) from e
        if e.status < 500:
            raise ClientError(full, status_code=e.status, json_body=json_body) from e
        raise ServerError(full) from e
    except json.JSONDecodeError as e:
        raise RenderError(f"{operation} failed: non-JSON response: {e}") from e
    except OSError as e:
        raise ServerError(f"{operation} network error: {e}") from e


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

    def _request_sync(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
    ) -> Any:
        """Blocking :meth:`_request`, for flow step writes."""
        return request_json_sync(
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
        payload = await self._request("GET", "/input" + _startup.input_query(), None)
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
            error = TaskError(details=callback_request.error)
            if callback_request.reason is not None:
                error.reason = callback_request.reason
            if callback_request.determinism is not None:
                error.reason = TaskErrorReason.DETERMINISM
                error.determinism = callback_request.determinism
            if callback_request.limit is not None:
                error.limit = callback_request.limit
            if callback_request.value is not None:
                error.value = callback_request.value
            data = ApiCallbackRequest(error=error)
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
        # Build the request outside _start_subtask, which retries internally, so
        # every retry resends the same idempotency_key and created_at.
        subtask_request = RunSubtaskRequest(
            task_name=task_name,
            input_=base64.b64encode(input_json).decode(),
            idempotency_key=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc).isoformat(),
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

    # Step writes block: they're made from the flow's own sync code.

    @_retry_transient_errors_sync
    @_translate_errors_sync("record step")
    def step_start(self, request: StepStartRequest) -> StepStartResponse:
        """Record an inline step's start, before its first attempt runs."""
        return StepStartResponse.from_dict(
            self._step_write("/step-inline/start", request.to_dict())
        )

    @_retry_transient_errors_sync
    @_translate_errors_sync("record step")
    def step_attempt(self, request: StepAttemptRequest) -> StepAttemptResponse:
        """Record a failed attempt of an inline step that will be retried."""
        return StepAttemptResponse.from_dict(
            self._step_write("/step-inline/attempt", request.to_dict())
        )

    @_retry_transient_errors_sync
    @_translate_errors_sync("record step")
    def step_complete(self, request: StepCompleteRequest) -> StepCompleteResponse:
        """Record an inline step's output or final error."""
        return StepCompleteResponse.from_dict(
            self._step_write("/step-inline/complete", request.to_dict())
        )

    def _step_write(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        payload = self._request_sync("POST", path, body)
        if not isinstance(payload, dict):
            raise RenderError(f"record step failed: unexpected response: {payload!r}")
        return payload

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
