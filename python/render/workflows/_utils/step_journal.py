"""The step history a flow attempt writes, kept in step with the SDK
server's."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime
from typing import TYPE_CHECKING

from render.client.errors import (
    ClientError,
    ExecutionError,
    FlowBadRequestError,
    FlowCancelledError,
    FlowLimitError,
    FlowUnreachableError,
    RateLimitError,
    ServerError,
    TerminalFlowError,
)
from render.client.errors import TimeoutError as SdkTimeoutError
from render.workflows._models.history import History
from render.workflows._models.step import (
    StepAttemptRecord,
    StepAttemptRequest,
    StepCompleteRequest,
    StepError,
    StepKey,
    StepOutcome,
    StepRecord,
    StepStartRequest,
    StepSuccess,
)
from render.workflows._models.wire import UNSET
from render.workflows._utils import clock, serializers

if TYPE_CHECKING:
    from render.workflows.client import UDSClient
    from render.workflows.durable_context import RunningStep


logger = logging.getLogger(__name__)


class RunFailure:
    """The error that fails the run: a divergence from the history, a step
    that failed for good, or a step write the SDK server didn't take. Its type
    says how the attempt ends. It's kept, not just raised, so it fails the
    run even if the flow catches it: the next step raises it again, and so
    does the context on exit.
    """

    error: ExecutionError | None = None

    def stop(self, error: ExecutionError) -> ExecutionError:
        """Stop the attempt, returning the error to raise. An error replaces
        an earlier one only if it ranks higher in
        _RUN_FAILURE_ERROR_PRIORITY; otherwise the first error wins, e.g. a
        step that failed for good over the failed write that would have
        recorded it."""
        if self.error is None or (
            _run_failure_error_rank(error) < _run_failure_error_rank(self.error)
        ):
            self.error = error
        return self.error

    def raise_if_set(self) -> None:
        if self.error is not None:
            raise self.error


_RUN_FAILURE_ERROR_PRIORITY: tuple[type[ExecutionError], ...] = (
    # The user cancelled the run, and reporting any failure would overwrite
    # that.
    FlowCancelledError,
    # Retrying won't fix the run, so it outranks a lost write the next
    # attempt could redo.
    TerminalFlowError,
)
"""Run failures from highest priority to lowest. Any other error ranks
last."""


def _run_failure_error_rank(error: ExecutionError) -> int:
    for rank, cls in enumerate(_RUN_FAILURE_ERROR_PRIORITY):
        if isinstance(error, cls):
            return rank
    return len(_RUN_FAILURE_ERROR_PRIORITY)


class StepJournal:
    """A flow attempt's step history, and the step writes that keep the
    SDK server's history in step with it.

    Each write is recorded before it's sent, as the SDK server records it. A
    write the SDK server doesn't take leaves its history behind what ran, so
    it fails the run, even if the flow catches the error.
    """

    _client: UDSClient
    _history: History
    """The validated history this attempt replays, empty on a first attempt,
    plus the step writes this attempt makes.
    """
    _session_id: str
    """The run's own task run id, which renderd keys step writes by."""
    _failure: RunFailure

    def __init__(
        self,
        client: UDSClient,
        history: History,
        *,
        session_id: str,
        failure: RunFailure,
    ) -> None:
        self._client = client
        self._history = history
        self._session_id = session_id
        self._failure = failure

    def step_state(self, step_key: StepKey) -> tuple[StepRecord | None, int]:
        """The step's record, if any, and the attempt a replay of it is on."""
        return self._history.get_step_state(step_key)

    def attempts(self, step_key: StepKey) -> list[StepAttemptRecord]:
        """The step's recorded failed attempts, in attempt order."""
        return self._history.attempts(step_key)

    def unconsumed_step(self, next_seq: int) -> StepRecord | None:
        """The first recorded step the attempt hasn't reached, or None."""
        return next(
            (s for s in self._history.steps if s.step_key.seq >= next_seq), None
        )

    def start(
        self, step_ctx: RunningStep, encoded_input: str | None = None
    ) -> datetime:
        """Record that the step started, returning when it did."""
        started_at = clock.now()
        self._history.record_start(
            step_ctx.step_key,
            task_name=step_ctx.name,
            started_at=started_at,
            encoded_input=encoded_input,
        )
        self._send(
            lambda: self._client.step_start(
                StepStartRequest(
                    step_key=step_ctx.step_key,
                    task_name=step_ctx.name,
                    input_=(
                        serializers.to_wire(encoded_input)
                        if encoded_input is not None
                        else UNSET
                    ),
                    started_at=started_at.isoformat(),
                )
            )
        )
        return started_at

    def attempt_failed(
        self, step_ctx: RunningStep, error: StepError, *, started_at: datetime
    ) -> None:
        """Record a failed attempt that the step will retry locally."""
        self._history.record_attempt(
            StepAttemptRecord(
                step_key=step_ctx.step_key,
                attempt=step_ctx.attempt,
                # renderd records the flow attempt. The SDK doesn't read it
                # back from its own writes.
                workflow_attempt=0,
                error=error,
                ended_at=clock.now(),
            )
        )
        self._send(
            lambda: self._client.step_attempt(
                StepAttemptRequest(
                    step_key=step_ctx.step_key,
                    attempt=step_ctx.attempt,
                    error=error,
                    started_at=started_at.isoformat(),
                )
            )
        )

    def complete(self, step_ctx: RunningStep, output: str) -> None:
        """Complete the step with its encoded output."""
        completed_at = self._completed_at(step_ctx)
        self._history.record_complete(
            step_ctx.step_key,
            completed_at=completed_at,
            output=output,
        )
        self._send(
            lambda: self._client.step_complete(
                StepCompleteRequest(
                    session_id=self._session_id,
                    key=step_ctx.step_key,
                    outcome=StepOutcome(
                        completed_at=completed_at.isoformat(),
                        result=StepSuccess(output=serializers.payload(output)),
                    ),
                )
            )
        )

    def fail(
        self,
        step_ctx: RunningStep,
        error: StepError,
        *,
        started_at: datetime,
        log_errors: bool = False,
    ) -> None:
        """Complete the step with the error from its final attempt.

        Args:
            log_errors: Log a failed write instead of failing the run. For a
                step closed out after the run already failed, whose error
                stands unless the write's error is terminal and outranks it.
        """
        ended_at = self._completed_at(step_ctx)

        outcome = StepOutcome(
            completed_at=ended_at.isoformat(),
            result=serializers.final_attempt(
                error,
                session_id=self._session_id,
                step_key=step_ctx.step_key,
                attempt=step_ctx.attempt,
                started_at=started_at,
                ended_at=ended_at,
            ),
        )
        self._history.record_complete(
            step_ctx.step_key,
            completed_at=ended_at,
            error=error,
        )
        request = StepCompleteRequest(
            session_id=self._session_id, key=step_ctx.step_key, outcome=outcome
        )

        self._send(lambda: self._client.step_complete(request), log_errors=log_errors)

    def _send(self, write: Callable[[], object], *, log_errors: bool = False) -> None:
        """Send a step write, failing the run if the SDK server doesn't take
        it."""
        try:
            write()
        except Exception as e:
            match e:
                case ServerError() | SdkTimeoutError() | RateLimitError():
                    # Still failing after the client's own retries.
                    error: ExecutionError = FlowUnreachableError(str(e))
                case ClientError(code="run_cancelled"):
                    error = FlowCancelledError(str(e))
                case ClientError(status_code=422):
                    # The API's LimitError: a flow limit the write
                    # exceeded.
                    body = e.json_body or {}
                    error = FlowLimitError(
                        str(e),
                        code=e.code,
                        limit=body.get("limit"),
                        value=body.get("value"),
                    )
                case ClientError():
                    error = FlowBadRequestError(str(e), code=e.code)
                case _:
                    # E.g. a response the client can't parse.
                    error = ExecutionError(str(e), type="flow")
            # A terminal error always stops the attempt: the run's failure
            # may rank below it, e.g. a cancel its failure callback would
            # overwrite.
            if log_errors and not isinstance(error, TerminalFlowError):
                # The next attempt's replay sends the write again.
                logger.warning(
                    "step write failed after the attempt stopped: %r",
                    error,
                    exc_info=e,
                )
                return
            raise self._failure.stop(error) from e

    def _completed_at(self, step_ctx: RunningStep) -> datetime:
        """When the step completes: now, but never before it started."""
        now = clock.now()
        # A resumed step's start came from an earlier worker's clock, which can
        # be ahead of this one. The SDK server rejects a completion before the
        # start, so it completes at the start instead.
        step = self._history.step(step_ctx.step_key)
        if step is not None and now < step.started_at:
            return step.started_at
        return now
