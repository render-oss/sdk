"""Encoding helpers for inline flow steps."""

from __future__ import annotations

import base64
import json
from datetime import datetime

from render.workflows._models.step import (
    Payload,
    StepAttempt,
    StepError,
    StepKey,
)


def encode(value: object) -> str:
    return json.dumps(value, allow_nan=False)


def decode(value: str) -> object:
    return json.loads(value)


def to_wire(value: str) -> str:
    """The base64 the socket API carries for encoded JSON."""
    return base64.b64encode(value.encode()).decode()


def payload(value: str) -> Payload:
    return Payload(data=to_wire(value))


def final_attempt(
    error: StepError,
    *,
    session_id: str,
    step_key: StepKey,
    attempt: int,
    started_at: datetime,
    ended_at: datetime,
) -> StepAttempt:
    """The failed attempt that ends a step, with its error as a JSON payload."""
    return StepAttempt(
        session_id=session_id,
        key=step_key,
        attempt=attempt,
        started_at=started_at.isoformat(),
        ended_at=ended_at.isoformat(),
        error=payload(json.dumps(error.to_dict())),
    )
