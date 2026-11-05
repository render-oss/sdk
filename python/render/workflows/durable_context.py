"""The FlowContext the workflow runtime hands to flows."""

from __future__ import annotations

import inspect
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, replace
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from render.client.errors import (
    DeterminismError,
    ExecutionError,
    FlowNestedStepError,
    FlowUnreachableError,
    RenderError,
    StepError,
    TerminalFlowError,
)
from render.workflows import _determinism
from render.workflows._models.history import History
from render.workflows._models.step import StepKey, StepRecord
from render.workflows._models.task import DeterminismDetails, DeterminismKind
from render.workflows._models.wire import UNSET, Unset
from render.workflows._utils import clock, serializers
from render.workflows._utils.step_errors import (
    raised_error,
    recorded_error,
)
from render.workflows._utils.step_journal import RunFailure, StepJournal
from render.workflows.context import FlowContext, FlowRunMetadata
from render.workflows.flow import FlowDefinition
from render.workflows.task import Retry, TaskDefinition

if TYPE_CHECKING:
    from types import TracebackType

    from render.workflows._models.task import InputResponse
    from render.workflows.client import UDSClient


_ONE_STEP_AT_A_TIME = (
    "A flow runs one step at a time, so a step's function can't make ctx calls."
)


class _ConcurrentStepError(TerminalFlowError):
    """A ctx call made while another step is in flight."""


@dataclass(frozen=True)
class RunningStep:
    """One step of a flow attempt, keyed by the order it started."""

    step_key: StepKey
    name: str
    retry: Retry | None
    attempt: int = 0
    """The attempt the step is on, counting from 0."""


_running_step: ContextVar[RunningStep | None] = ContextVar("running_step", default=None)


class DurableFlowContext(FlowContext):
    """The FlowContext handed to flows by the workflow runtime."""

    _metadata: FlowRunMetadata
    _failure: RunFailure
    _journal: StepJournal
    _next_seq: int = 0
    """The seq the next step will take."""
    _in_flight: bool = False
    """Whether a ctx call owns the one-step-at-a-time slot, from
    sequence allocation until the step returns or raises.
    """
    _entered: bool = False
    """Whether the context has run its attempt. A context runs one attempt."""

    def __init__(self, client: UDSClient, input_response: InputResponse) -> None:
        task_run_id = input_response.task_run_id
        if isinstance(task_run_id, Unset) or not task_run_id:
            raise RenderError("flow input is missing its task_run_id")
        if input_response.inline_retry_mode not in (UNSET, "local"):
            raise RenderError(
                f"inline retry mode {input_response.inline_retry_mode!r} "
                f"isn't supported. Steps retry locally"
            )
        self._metadata = FlowRunMetadata(flow_run_id=task_run_id)
        self._workflow_attempt = (
            0 if isinstance(input_response.attempt, Unset) else input_response.attempt
        )
        self._failure = RunFailure()
        self._journal = StepJournal(
            client,
            _replay_history(input_response),
            session_id=task_run_id,
            failure=self._failure,
        )

    def __enter__(self) -> DurableFlowContext:
        # A reused context would replay from its last seq, and could carry a
        # stale run failure into the next attempt.
        if self._entered:
            raise RuntimeError("a DurableFlowContext runs one flow attempt")
        self._entered = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._in_flight = False
        # A run failure fails the run even if the flow caught it, returned
        # normally, or raised a different error in its place.
        self._failure.raise_if_set()
        # A failed flow can stop short of its history; a successful one
        # can't. E.g. a replay that returns before a recorded refund step.
        if exc_type is None:
            self._validate_completion()

    @property
    def metadata(self) -> FlowRunMetadata:
        return self._metadata

    @property
    def run_failure(self) -> ExecutionError | None:
        """The error that stopped the attempt, or None if nothing did."""
        return self._failure.error

    def _validate_completion(self) -> None:
        """A successful flow must have consumed every recorded step."""
        recorded = self._journal.unconsumed_step(self._next_seq)
        if recorded is None:
            return
        raise self._failure.stop(
            DeterminismError(
                DeterminismDetails(
                    step_key=recorded.step_key,
                    kind=DeterminismKind.TYPE,
                    workflow_attempt=recorded.workflow_attempt,
                    expected=f"{recorded.type_.value} step {recorded.task_name or ''}",
                    actual="flow completion before the recorded step",
                )
            )
        )

    def invoke(self, task: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(task, FlowDefinition):
            raise TypeError(
                f"ctx.invoke({task.name}): a flow can't invoke another flow"
            )
        if not isinstance(task, TaskDefinition):
            raise TypeError(
                "ctx.invoke takes a registered task. Use ctx.step to run a function"
            )
        raise NotImplementedError(
            f"ctx.invoke({task.name}): invoking a registered task from a flow "
            f"isn't supported yet"
        )

    # Not on FlowContext yet, so a call fails with this error, not an
    # AttributeError.
    def sleep(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("ctx.sleep: sleeping in a flow isn't supported yet")

    def step(self, name: Any, fn: Any, /, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(name, str):
            raise TypeError(
                "ctx.step takes the step's name first, such as "
                'ctx.step("charge", charge, order_id)'
            )
        if not name:
            raise ValueError("ctx.step needs a non-empty step name")
        if isinstance(fn, FlowDefinition):
            raise TypeError(f"ctx.step({fn.name}): a flow can't run another flow")
        if isinstance(fn, TaskDefinition):
            raise TypeError(
                f"ctx.step({fn.name}): {fn.name} is a registered task. "
                f"Use ctx.invoke to run it"
            )
        if not callable(fn):
            raise TypeError("ctx.step takes a function to run as a step")
        if inspect.iscoroutinefunction(fn):
            raise TypeError(
                "ctx.step takes a sync function. Async steps aren't supported yet"
            )

        retry = _step_retry(kwargs)
        with self.start_step(name, retry) as (step_ctx, recorded_step):
            try:
                return self._run_step(step_ctx, recorded_step, fn, args)
            except ExecutionError as error:
                if not isinstance(error, StepError):
                    # Runtime failures stop this attempt and go to the executor.
                    # Recovery may supersede it before its callback is accepted;
                    # they are not persisted as application step outcomes.
                    self._failure.stop(error)
                self._failure.raise_if_set()

                completion = error.to_step_completion()
                if completion is not None:
                    self._journal.finish_attempt(completion)

                # A recoverable failure reaches flow code only after its write.
                self._failure.raise_if_set()
                raise

    @contextmanager
    def start_step(
        self, name: str, retry: Retry | None
    ) -> Generator[tuple[RunningStep, StepRecord | None], None, None]:
        """
        Number a step as it starts and hold the one-step-at-a-time slot until
        it finishes. Steps run one at a time, so the numbering follows the
        order the flow calls them. Yields the step, at the attempt a
        replay picks up from, with its record if it has one.
        """
        self._failure.raise_if_set()
        # Either fails the run, even if the flow or an enclosing step
        # catches it.
        outer_step = _running_step.get()
        if outer_step is not None:
            raise self._failure.stop(
                FlowNestedStepError(
                    f"ctx.step can't be called within a step: step "
                    f"{outer_step.name!r} made a ctx call from its function. "
                    f"Make ctx calls from the flow function instead."
                )
            )
        if self._in_flight:
            raise self._failure.stop(_ConcurrentStepError(_ONE_STEP_AT_A_TIME))
        self._in_flight = True

        # A negative policy retries nothing, the same as 0.
        if retry is not None and retry.max_retries < 0:
            retry = replace(retry, max_retries=0)
        step_key = StepKey(seq=self._next_seq)
        recorded_step, attempt = self._journal.step_state(step_key)
        step_ctx = RunningStep(
            step_key=step_key, name=name, retry=retry, attempt=attempt
        )

        self._next_seq += 1
        token = _running_step.set(step_ctx)
        try:
            yield step_ctx, recorded_step
        finally:
            _running_step.reset(token)
            self._in_flight = False

    def _run_step(
        self,
        step_ctx: RunningStep,
        recorded_step: StepRecord | None,
        fn: Callable[..., Any],
        args: tuple[Any, ...],
    ) -> Any:
        encoded_args = self._checked_args(step_ctx, recorded_step, args)

        # A finished step returns its recorded outcome instead of running again.
        if recorded_step is not None and recorded_step.completed_at is not None:
            if recorded_step.error is not None:
                raise raised_error(
                    step_ctx.name,
                    recorded_step.error,
                    session_id=self._metadata.flow_run_id,
                    step_key=step_ctx.step_key,
                )
            return _decoded_output(recorded_step)

        if recorded_step is None:
            self._journal.start(step_ctx, encoded_args)

        # Failed argument encoding raised above unless this was a replay.
        if encoded_args is None:
            raise TerminalFlowError("step input is missing after argument validation")
        output, step_ctx = self._run_attempts(step_ctx, fn, encoded_args)
        self._journal.complete(step_ctx, output)
        # Return the decoded output, so a first run sees what a replay would.
        return serializers.decode(output)

    def _checked_args(
        self,
        step_ctx: RunningStep,
        recorded_step: StepRecord | None,
        args: tuple[Any, ...],
    ) -> str | None:
        """Encode and check args; a replayed encoding failure has no input."""
        try:
            return _encode_and_check_args(step_ctx, recorded_step, args)
        except (TypeError, ValueError) as e:
            # A completed encoding failure is raised from its recorded outcome.
            if recorded_step is not None and recorded_step.completed_at is not None:
                return None
            # A new step records its failed input encoding without an input.
            # An open one was cut off before recording that failure.
            started_at = (
                self._journal.start(step_ctx) if recorded_step is None else clock.now()
            )
            raise self._step_failure(
                step_ctx,
                e,
                started_at=started_at,
            ) from None

    def _run_attempts(
        self,
        step_ctx: RunningStep,
        fn: Callable[..., Any],
        encoded_args: str,
    ) -> tuple[str, RunningStep]:
        """Run the step until it succeeds or runs out of retries.

        Returns the encoded result and the step at the attempt that succeeded.
        Local inline retries move the step to a new attempt, so the caller
        must use the returned step, not the one it passed in.
        """
        retry = step_ctx.retry
        max_retries = retry.max_retries if retry else 0

        if step_ctx.attempt > max_retries:
            raise self._fail_resume_past_retries(step_ctx, max_retries)

        while True:
            started_at = clock.now()
            try:
                # Each attempt decodes fresh arguments, so mutations from a
                # failed call cannot affect the next attempt or a replay.
                # Decoding is the copy, and is cheaper than copy.deepcopy.
                result = fn(*_decoded_args(encoded_args))
            except (TerminalFlowError, FlowUnreachableError):
                raise
            except Exception as e:
                # A runtime guard may have been caught and wrapped by user code.
                self._failure.raise_if_set()
                if not retry or step_ctx.attempt >= max_retries:
                    raise self._step_failure(
                        step_ctx, e, started_at=started_at
                    ) from None

                self._journal.attempt_failed(
                    step_ctx, recorded_error(e), started_at=started_at
                )
                # Back off here, at the failure, so a resumed attempt never waits.
                time.sleep(_retry_delay_ms(retry, step_ctx.attempt) / 1000)
                step_ctx = replace(step_ctx, attempt=step_ctx.attempt + 1)
                continue

            # A swallowed runtime violation still stops this attempt.
            self._failure.raise_if_set()

            try:
                return serializers.encode(result), step_ctx
            except (TypeError, ValueError) as e:
                # Not retried: another attempt would repeat the function's
                # side effects and return a result that still can't be encoded.
                raise self._step_failure(
                    step_ctx,
                    e,
                    started_at=started_at,
                ) from None

    def _fail_resume_past_retries(
        self, step_ctx: RunningStep, max_retries: int
    ) -> ExecutionError:
        """Reuse the last recorded failure without executing another attempt."""
        prev_attempts = self._journal.attempts(step_ctx.step_key)
        if prev_attempts:
            final = prev_attempts[-1]
            return raised_error(
                step_ctx.name,
                final.error,
                session_id=self._metadata.flow_run_id,
                step_key=step_ctx.step_key,
                completion=final,
            )

        return TerminalFlowError(
            f"ctx.step({step_ctx.name}) resumed at attempt {step_ctx.attempt}, "
            f"past its {max_retries} retries"
        )

    def _step_failure(
        self,
        step_ctx: RunningStep,
        error: Exception,
        *,
        started_at: datetime,
    ) -> StepError:
        recorded = recorded_error(error)
        return raised_error(
            step_ctx.name,
            recorded,
            session_id=self._metadata.flow_run_id,
            step_key=step_ctx.step_key,
            completion=self._journal.create_failed_attempt(
                step_ctx,
                recorded,
                started_at=started_at,
                workflow_attempt=self._workflow_attempt,
            ),
        )


def _replay_history(input_response: InputResponse) -> History:
    """Validate history before replaying each outcome at its original ctx call."""
    input_response.history.validate()
    return input_response.history


def _step_retry(kwargs: dict[str, Any]) -> Retry | None:
    """The step's retry policy, from ctx.step's keyword arguments."""
    retry = kwargs.pop("retry", None)
    if kwargs:
        raise TypeError(
            f"ctx.step got unexpected keyword arguments {sorted(kwargs)}. "
            f"Pass the function's arguments positionally, or bind them "
            f"with functools.partial"
        )
    return retry


def _encode_and_check_args(
    step_ctx: RunningStep,
    recorded_step: StepRecord | None,
    args: tuple[Any, ...],
) -> str:
    """
    The step's args, encoded and, on a replay, checked against its record.

    Raises DeterminismError if a replay diverges from its record, or the
    encoding error if the args can't be encoded.
    """
    # A replay is checked before the step can run or record anything.
    try:
        encoded_args = serializers.encode(list(args))
    except (TypeError, ValueError):
        if recorded_step is not None:
            divergence = _determinism.encoding_failure_divergence(
                recorded_step, step_ctx.name
            )
            if divergence is not None:
                raise DeterminismError(divergence) from None
        raise

    if recorded_step is not None:
        # Confirm it matches what we previously saw
        divergence = _determinism.args_divergence(
            recorded_step, step_ctx.name, encoded_args
        )
        if divergence is not None:
            raise DeterminismError(divergence)
    return encoded_args


def _decoded_output(recorded_step: StepRecord) -> Any:
    """A finished step's recorded output."""
    output = recorded_step.output
    return serializers.decode(output) if output else None


def _decoded_args(encoded: str) -> list[Any]:
    return cast("list[Any]", serializers.decode(encoded))


def _retry_delay_ms(retry: Retry, failed_attempt: int) -> int:
    """The scheduler delay after this failed attempt."""
    return max(
        0,
        int(retry.wait_duration_ms * retry.backoff_scaling**failed_attempt),
    )
