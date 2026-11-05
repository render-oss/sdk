"""Convert application failures between exceptions and step history."""

from __future__ import annotations

import traceback
from typing import Any

from render.client.errors import StepError
from render.workflows._models.step import StepAttemptRecord, StepKey
from render.workflows._models.step import StepError as WireStepError
from render.workflows._models.wire import UNSET, Unset
from render.workflows._utils import serializers

# Leave room for the message and data under the SDK server's error-size limit.
_STACK_BYTE_LIMIT = 16_000
_DATA_BYTE_LIMIT = 16_000


def recorded_error(error: Exception) -> WireStepError:
    data = _encoded_fields(error)
    stack = "".join(traceback.format_exception(error))
    encoded_stack = stack.encode("utf-8")
    if len(encoded_stack) > _STACK_BYTE_LIMIT:
        # Keep the innermost frames without splitting a UTF-8 character.
        suffix = encoded_stack[-(_STACK_BYTE_LIMIT - len("…".encode())) :]
        stack = "…" + suffix.decode("utf-8", errors="ignore")

    return WireStepError(
        name=type(error).__name__,
        message=str(error),
        stack=stack,
        data=data,
    )


def _encoded_fields(error: Exception) -> str | Unset:
    """Keep whole encodable fields that fit within the data budget."""
    fields: dict[str, Any] = {}
    data: str | Unset = UNSET
    for key, value in vars(error).items():
        if key.startswith("__"):
            continue
        try:
            candidate = serializers.encode({**fields, key: value})
        except (TypeError, ValueError):
            continue
        if len(candidate.encode("utf-8")) <= _DATA_BYTE_LIMIT:
            fields[key] = value
            data = candidate
    return data


def raised_error(
    name: str,
    error: WireStepError,
    *,
    session_id: str | None,
    step_key: StepKey,
    completion: StepAttemptRecord | None = None,
) -> StepError:
    """Recorded failures are application outcomes, regardless of their names."""
    return StepError(
        f"Step {name!r} failed with {error.name}: {error.message}",
        type="flow",
        err_type="runtime",
        step_name=name,
        error_name=error.name,
        error_data=_decoded_data(error),
        session_id=session_id,
        step_key=step_key,
        completion=completion,
    )


def _decoded_data(error: WireStepError) -> Any:
    if isinstance(error.data, Unset):
        return None
    try:
        return serializers.decode(error.data)
    except ValueError:
        return error.data
