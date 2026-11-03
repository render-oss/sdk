from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from render.client.types import FlowRunDetails

    # Type-only: the step models raise these errors, so a runtime import
    # would be circular.
    from render.workflows._models.step import StepKey
    from render.workflows._models.task import DeterminismDetails
    from render.workflows.client import CallbackRequest


class RenderError(Exception):
    """Base exception for all Render errors."""

    pass


class ClientError(RenderError):
    """Exception for client errors. This is returned when
    the client makes a request to the API and the API returns a 4xx error.

    status_code is the HTTP status, or None when the error did not come from
    an HTTP response. json_body is the decoded JSON error body, or None when
    the API didn't send a JSON object. Callers read the fields their API
    defines from it."""

    def __init__(
        self,
        *args: object,
        code: str | None = None,
        status_code: int | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(*args)
        # Set by callers that parse the error themselves, e.g. the public API
        # client and the sandbox errors.
        self._code = code
        self.status_code = status_code
        self.json_body = json_body

    @property
    def code(self) -> str | None:
        """The machine-readable code from the error body, or None when the API
        did not send one."""
        if self._code is not None:
            return self._code
        code = self.json_body.get("code") if self.json_body else None
        return code if isinstance(code, str) else None


class RateLimitError(ClientError):
    """Exception for rate limit errors. This is returned when
    the client makes a request to the API and the API returns a 429 error."""

    pass


class TimeoutError(RenderError):
    """Exception for timeout errors. This is returned when the
    client makes a request to the API and the request times out."""

    pass


class ServerError(RenderError):
    """Exception for server errors. This is returned when the
    client makes a request to the API and the API returns a 5xx error."""

    pass


class ExecutionError(RenderError):
    """Exception for a task run or a flow step that failed.

    type is "task" for a task run and "flow" for a step in a flow.
    err_type says why it failed when that's known, such as "runtime" for an
    error the code raised. For a flow step, step_name is the step's name
    and error_name is the type name of the error it raised, such as
    "ValueError". error_data holds the attributes that error set on itself,
    such as a `code`, when they encode as JSON. session_id and step_key
    identify the step within its flow run."""

    def __init__(
        self,
        *args: object,
        type: Literal["task", "flow"],
        err_type: str | None = None,
        step_name: str | None = None,
        error_name: str | None = None,
        error_data: Any = None,
        session_id: str | None = None,
        step_key: "StepKey | None" = None,
    ) -> None:
        super().__init__(*args)
        self.type = type
        self.err_type = err_type
        self.step_name = step_name
        self.error_name = error_name
        self.error_data = error_data
        self.session_id = session_id
        self.step_key = step_key

    def to_callback_request(self) -> "CallbackRequest":
        """The error callback that reports this error as the task's failure."""
        # Imported here: the workflow client imports these errors.
        from render.workflows.client import CallbackRequest, Status

        return CallbackRequest(status=Status.ERROR, error=str(self))


class TaskRunError(ExecutionError):
    """Exception for task run errors. This is returned when a running
    task fails."""

    def __init__(self, *args: object, err_type: str | None = None) -> None:
        super().__init__(*args, type="task", err_type=err_type)


class FlowRunError(RenderError):
    """Exception for flow run errors. This is raised when a flow run
    being waited on fails or is canceled.

    flow_run_id is the ID of the flow run, and details are its final details,
    whose status says whether it failed or was canceled."""

    def __init__(
        self,
        *args: object,
        flow_run_id: str | None = None,
        details: "FlowRunDetails | None" = None,
    ) -> None:
        super().__init__(*args)
        self.flow_run_id = flow_run_id
        self.details = details


class TerminalFlowError(ExecutionError):
    """Exception for a flow step error that retrying won't fix. A step
    that raises it fails without using its remaining retries."""

    def __init__(
        self,
        *args: object,
        type: Literal["task", "flow"] = "flow",
        err_type: str | None = None,
        step_name: str | None = None,
        error_name: str | None = None,
        error_data: Any = None,
        session_id: str | None = None,
        step_key: "StepKey | None" = None,
    ) -> None:
        super().__init__(
            *args,
            type=type,
            err_type=err_type,
            step_name=step_name,
            error_name=error_name,
            error_data=error_data,
            session_id=session_id,
            step_key=step_key,
        )


class FlowCancelledError(TerminalFlowError):
    """Exception for a flow run that was cancelled while an attempt ran.
    The attempt stops without reporting a failure, and the cancel overrides
    any error that already failed the run."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args, type="flow")


class FlowBadRequestError(TerminalFlowError):
    """Exception for a step write the workflow system rejected, such as a
    400, a 422 or a 409 other than a cancel. Retrying won't fix it, so it
    fails the run.

    code is the workflow system's code for the rejection, if it sent one."""

    def __init__(self, *args: object, code: str | None = None) -> None:
        super().__init__(*args, type="flow")
        self.code = code


def _public_limit_code(code: str | None) -> str | None:
    """The limit code as customers see it: the workflow system sends
    ``workflow_*``, and REST and GraphQL report the same limits as ``flow_*``."""
    if code is not None and code.startswith("workflow_"):
        return "flow_" + code.removeprefix("workflow_")
    return code


class FlowLimitError(FlowBadRequestError):
    """Exception for a step write over a flow limit: the workflow
    system's LimitError.

    code names the limit, such as "flow_payload_too_large". limit is the
    limit and value is what exceeded it, when the workflow system sent them."""

    def __init__(
        self,
        *args: object,
        code: str | None = None,
        limit: int | None = None,
        value: int | None = None,
    ) -> None:
        super().__init__(*args, code=_public_limit_code(code))
        # The workflow system's own code, which the error callback reports.
        self._wire_code = code
        self.limit = limit
        self.value = value

    def to_callback_request(self) -> "CallbackRequest":
        from render.workflows._models.task import TaskErrorReason

        request = super().to_callback_request()
        # The LimitError's code names the limit, which is also the reason.
        if self._wire_code is not None:
            request.reason = TaskErrorReason(self._wire_code)
        request.limit = self.limit
        request.value = self.value
        return request


class FlowNestedStepError(TerminalFlowError):
    """Exception for a ctx call made from inside a step's function. It fails
    the run even if the flow or the enclosing step catches it."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args, type="flow")


class FlowUnreachableError(ExecutionError):
    """Exception for a flow attempt that lost contact with the workflow
    system. The attempt reports it as a system error and exits, so the run
    recovers."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args, type="flow")

    def to_callback_request(self) -> "CallbackRequest":
        from render.workflows._models.task import TaskErrorReason

        request = super().to_callback_request()
        # Render caused the failure, so the run is retried as a system failure.
        request.reason = TaskErrorReason.SYSTEM
        return request


class DeterminismError(TerminalFlowError):
    """
    A replay made a different ``ctx`` call than the one recorded in history.

    It fails the run even if flow code catches it, and every later
    ``ctx`` call raises it again.
    """

    def __init__(self, details: "DeterminismDetails") -> None:
        super().__init__(
            f"Flow replay diverged from its history at step {details.step_key.seq}: "
            f"{details.kind.description}. History recorded {details.expected}; this attempt called "
            f"{details.actual}. A flow must make the same ctx calls in the same "
            f"order with the same inputs on every replay. Move non-deterministic "
            f"work into a step.",
            step_key=details.step_key,
        )
        self.details = details

    def to_callback_request(self) -> "CallbackRequest":
        request = super().to_callback_request()
        request.determinism = self.details
        return request


class FlowHistoryErrorCode(str, Enum):
    """Why a flow's recorded history can't be replayed."""

    STEP_SEQ = "WFL-HIST-STEP-SEQ"
    """The steps' seqs don't count up from zero without skipping one."""
    AFTER_OPEN = "WFL-HIST-AFTER-OPEN"
    """A step comes after one that never finished."""
    AFTER_TERMINAL = "WFL-HIST-AFTER-TERMINAL"
    """A step comes after one that ended the run."""
    TERMINAL = "WFL-HIST-TERMINAL"
    """The last step ended the run, so there's nothing left to replay."""
    ATTEMPT_STEP = "WFL-HIST-ATTEMPT-STEP"
    """A failed attempt was made before its step started."""
    ATTEMPT_SEQ = "WFL-HIST-ATTEMPT-SEQ"
    """A step's failed attempts aren't numbered in increasing order."""
    SEQ_SUB_KEYS = "WFL-HIST-SEQ-SUB-KEYS"
    """A seq has several steps, which this SDK can't look up yet."""


class FlowHistoryError(RenderError):
    """Exception for a flow's recorded history that can't be replayed safely.

    code says what's wrong and step_key identifies the step it concerns, when
    there is one. Both lead the message, so a message can be looked up by its
    prefix."""

    def __init__(
        self,
        code: FlowHistoryErrorCode,
        message: str,
        step_key: "StepKey | None" = None,
    ) -> None:
        # Logs and the error callback only see str(error), so the step goes
        # in the message as well as on the error.
        where = ""
        if step_key is not None:
            where = f" [seq={step_key.seq}"
            if step_key.sub_key:
                where += f" sub_key={step_key.sub_key!r}"
            where += "]"
        super().__init__(f"{code.value}{where}: {message}")
        self.code = code
        self.step_key = step_key
