"""The step history a flow attempt replays against."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any

from render.client.errors import FlowHistoryError, FlowHistoryErrorCode
from render.workflows._models.step import (
    StepAttemptRecord,
    StepError,
    StepKey,
    StepRecord,
    StepType,
)


@dataclass
class History:
    steps: list[StepRecord] = field(default_factory=list)
    """The recorded steps, in step key order."""
    step_attempts: dict[StepKey, list[StepAttemptRecord]] = field(default_factory=dict)
    """Failed inline attempts of open steps, by step, in attempt order."""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> History:
        steps = sorted(
            (StepRecord.from_dict(s) for s in d.get("steps") or []),
            key=lambda step: (step.step_key.seq, step.step_key.sub_key),
        )
        attempts: dict[StepKey, list[StepAttemptRecord]] = {}
        for a in d.get("step_attempts", []):
            record = StepAttemptRecord.from_dict(a)
            attempts.setdefault(record.step_key, []).append(record)
        return cls(
            steps=steps,
            step_attempts={
                step_key: sorted(records, key=lambda record: record.attempt)
                for step_key, records in attempts.items()
            },
        )

    def validate(self) -> None:
        """Check the invariants replay relies on, raising FlowHistoryError."""
        validate_steps(self.steps, self.step_attempts)

    def step(self, step_key: StepKey) -> StepRecord | None:
        """The step recorded under step_key, or None if there isn't one."""
        # The index lookup relies on v1's assumption that each seq has one
        # sub_key, so a step sits at the index of its seq. Validation still
        # allows several sub_keys per seq, since that could change. Such a
        # history shifts steps off their index, so fail rather than return
        # the wrong step. Seqs can't skip one, so the last step's seq shows
        # whether any seq holds more than one step.
        if self.steps and self.steps[-1].step_key.seq != len(self.steps) - 1:
            raise _several_steps_per_seq(step_key)
        if step_key.seq >= len(self.steps):
            return None
        step = self.steps[step_key.seq]
        if step.step_key.seq != step_key.seq:
            raise _several_steps_per_seq(step_key)
        return step if step.step_key.sub_key == step_key.sub_key else None

    def attempts(self, step_key: StepKey) -> list[StepAttemptRecord]:
        """The step's recorded failed attempts, in attempt order."""
        return self.step_attempts.get(step_key, [])

    def get_step_state(self, step_key: StepKey) -> tuple[StepRecord | None, int]:
        """The step's record, if any, and the attempt a replay of it is on,
        counting from 0."""
        recorded_step = self.step(step_key)
        if recorded_step is None:
            return None, 0
        if recorded_step.completed_at is not None:
            # A finished step records the flow attempt that completed it,
            # so this picks up after that one.
            return recorded_step, recorded_step.workflow_attempt + 1
        # An open step was cut off. It picks up after its last recorded
        # failure, or after the first attempt if it recorded none.
        attempts = self.attempts(step_key)
        return recorded_step, attempts[-1].attempt + 1 if attempts else 1

    def record_start(
        self,
        step_key: StepKey,
        *,
        task_name: str,
        started_at: datetime,
        encoded_input: str | None = None,
    ) -> None:
        """Start an inline step, as the SDK server records it."""
        # The first start of a step wins.
        if self.step(step_key) is not None:
            return

        # A step starts open, in flow attempt 0. renderd sets the flow
        # attempt that finished it; this copy keeps 0.
        self.steps.append(
            StepRecord(
                step_key=step_key,
                type_=StepType.INLINE,
                workflow_attempt=0,
                started_at=started_at,
                task_name=task_name,
                input_=encoded_input,
            )
        )

    def record_attempt(self, attempt: StepAttemptRecord) -> None:
        """Add a failed attempt the step will retry, as the SDK server records it."""
        if self.step(attempt.step_key) is None:
            raise ValueError(f"step {attempt.step_key} has no recorded start")

        attempts = self.step_attempts.setdefault(attempt.step_key, [])
        # The first record of an attempt wins.
        if any(a.attempt == attempt.attempt for a in attempts):
            return

        attempts.append(attempt)

    def record_complete(
        self,
        step_key: StepKey,
        *,
        completed_at: datetime,
        output: str | None = None,
        error: StepError | None = None,
    ) -> None:
        """Finish a step, as the SDK server records it."""
        step = self.step(step_key)
        if step is None:
            raise ValueError(f"step {step_key} has no recorded start")

        # The first completion of a step wins.
        if step.completed_at is not None:
            return

        if completed_at < step.started_at:
            raise ValueError(
                f"step {step_key} completed at {completed_at}, before it started "
                f"at {step.started_at}"
            )

        # A step sits at the index of its seq, as step() checks.
        self.steps[step_key.seq] = replace(
            step,
            completed_at=completed_at,
            output=output,
            error=error,
        )

        # The SDK server only sends the attempts of open steps.
        self.step_attempts.pop(step_key, None)


def _several_steps_per_seq(step_key: StepKey) -> FlowHistoryError:
    return FlowHistoryError(
        FlowHistoryErrorCode.SEQ_SUB_KEYS,
        "a seq has several steps, but this SDK looks steps up assuming each "
        "seq has one",
        step_key,
    )


def validate_steps(
    steps: list[StepRecord], attempts: dict[StepKey, list[StepAttemptRecord]]
) -> None:
    """Check
    - the steps' seqs count up from zero
    - only the last step is open
    - no step comes after a terminal one
    - the last step isn't terminal, since the run already ended there
    - the last step's failed attempts fit it.
    """
    if not steps:
        return
    if steps[0].step_key.seq != 0:
        raise FlowHistoryError(
            FlowHistoryErrorCode.STEP_SEQ, "expected seq 0", steps[0].step_key
        )

    for prev, step in zip(steps, steps[1:], strict=False):
        # Steps can share a seq, told apart by their sub-keys, but seqs can't
        # skip one.
        if step.step_key.seq not in (prev.step_key.seq, prev.step_key.seq + 1):
            raise FlowHistoryError(
                FlowHistoryErrorCode.STEP_SEQ,
                f"expected seq {prev.step_key.seq + 1}",
                step.step_key,
            )
        if prev.completed_at is None:
            raise FlowHistoryError(
                FlowHistoryErrorCode.AFTER_OPEN,
                "steps come after this unfinished step",
                prev.step_key,
            )
        reason = _terminal_reason(prev)
        if reason is not None:
            raise FlowHistoryError(
                FlowHistoryErrorCode.AFTER_TERMINAL,
                f"steps come after this step, which ended the run because {reason}",
                prev.step_key,
            )

    last = steps[-1]
    reason = _terminal_reason(last)
    if reason is not None:
        raise FlowHistoryError(
            FlowHistoryErrorCode.TERMINAL,
            f"the run ended at this step because {reason}",
            last.step_key,
        )
    # Only the last step can be resumed, so other steps' attempts don't matter.
    validate_attempts(last, attempts.get(last.step_key, []))


def _terminal_reason(step: StepRecord) -> str | None:
    """Why the step ended the run, or None if it didn't."""
    # A step only finishes with an error that's terminal: it ran out of
    # retries, its args couldn't be encoded, or a replay diverged from it.
    if step.completed_at is None or step.error is None:
        return None
    return f"it failed with {step.error.name}"


def validate_attempts(step: StepRecord, attempts: list[StepAttemptRecord]) -> None:
    """Check that the step's failed attempts fit it: numbered in order, and
    made while it was running."""
    # The SDK server only sends an open step's attempts, so a finished step
    # has none to check. Replay returns its recorded outcome instead.
    if step.completed_at is not None:
        return

    prev = -1
    for attempt in attempts:
        # An attempt cut off by a crash records no failure, so numbers can
        # skip one, but never repeat or go back.
        if attempt.attempt <= prev:
            raise FlowHistoryError(
                FlowHistoryErrorCode.ATTEMPT_SEQ,
                f"expected an attempt after {prev}, got attempt {attempt.attempt}",
                step.step_key,
            )
        prev = attempt.attempt
        if attempt.workflow_attempt < step.workflow_attempt:
            raise FlowHistoryError(
                FlowHistoryErrorCode.ATTEMPT_STEP,
                f"attempt {attempt.attempt} is from flow attempt "
                f"{attempt.workflow_attempt}, before the step started in "
                f"{step.workflow_attempt}",
                step.step_key,
            )
        if attempt.ended_at < step.started_at:
            raise FlowHistoryError(
                FlowHistoryErrorCode.ATTEMPT_STEP,
                f"attempt {attempt.attempt} ended before the step started",
                step.step_key,
            )
