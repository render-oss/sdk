"""How a replayed flow step diverges from the step recorded in history."""

from __future__ import annotations

import json

from render.workflows._models.step import StepRecord, StepType
from render.workflows._models.task import DeterminismDetails, DeterminismKind

_DESCRIPTION_LIMIT = 500


def args_divergence(
    recorded: StepRecord, name: str, encoded_args: str
) -> DeterminismDetails | None:
    """How this call diverges from its recorded step, if it does."""
    actual_args = _canonical(encoded_args)
    recorded_name = recorded.task_name or ""
    recorded_input = recorded.input_
    recorded_args = (
        _canonical(recorded_input) if recorded_input else "[<missing recorded input>]"
    )

    kind = _type_divergence(recorded.type_)
    # Both sides are canonical JSON, so equal args compare equal as strings.
    if kind is None and (
        not recorded_input or (name, actual_args) != (recorded_name, recorded_args)
    ):
        kind = DeterminismKind.INPUT_HASH
    if kind is None:
        return None
    return DeterminismDetails(
        step_key=recorded.step_key,
        kind=kind,
        workflow_attempt=recorded.workflow_attempt,
        expected=_describe(recorded.type_, recorded_name, recorded_args),
        actual=_describe(StepType.INLINE, name, actual_args),
    )


def encoding_failure_divergence(
    recorded: StepRecord, name: str
) -> DeterminismDetails | None:
    """How this call, whose args failed to encode, diverges from its recorded
    step, if it does."""
    recorded_name = recorded.task_name or ""
    recorded_input = recorded.input_
    # A step without input can have a recorded encoding failure, or have
    # been cut off before recording it. Match the same call in either case.
    if (
        recorded.type_ is StepType.INLINE
        and recorded_name == name
        and not recorded_input
        and (recorded.completed_at is None or recorded.error is not None)
    ):
        return None

    recorded_args = (
        _canonical(recorded_input) if recorded_input else "[<missing recorded input>]"
    )
    return DeterminismDetails(
        step_key=recorded.step_key,
        kind=_type_divergence(recorded.type_) or DeterminismKind.INPUT_HASH,
        workflow_attempt=recorded.workflow_attempt,
        expected=_describe(recorded.type_, recorded_name, recorded_args),
        actual=f"inline {name}(<input could not be encoded>)",
    )


def _type_divergence(recorded_type: StepType) -> DeterminismKind | None:
    """How an inline step diverges from a recorded step of this type, if it does."""
    match recorded_type:
        case StepType.INLINE:
            return None
        case StepType.UNKNOWN:
            return DeterminismKind.UNKNOWN_TYPE
        case _:
            return DeterminismKind.TYPE


def _canonical(encoded: str) -> str:
    """The encoded JSON with object keys sorted at every level."""
    return json.dumps(json.loads(encoded), sort_keys=True, separators=(",", ":"))


def _describe(step_type: StepType, name: str, canonical_args: str) -> str:
    # str-mixin enums format as "StepType.INLINE" on 3.11+, so use the value.
    call = f"{step_type.value} {name}({canonical_args[1:-1]})"
    if len(call) > _DESCRIPTION_LIMIT:
        return call[:_DESCRIPTION_LIMIT] + "…"
    return call
