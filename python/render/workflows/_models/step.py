"""A flow step's writes, and the records of them that history replays."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from render.workflows._models.wire import UNSET, Unset, Wire, parse_base64, parse_time


@dataclass
class StepError(Wire):
    name: str
    message: str
    stack: str | Unset = UNSET
    # JSON of the extra fields the raised error carried, if any.
    data: str | Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepError:
        return cls(
            name=d["name"],
            message=d["message"],
            stack=d.get("stack", UNSET),
            data=d.get("data", UNSET),
        )


@dataclass(frozen=True)
class StepKey(Wire):
    seq: int
    # The SDK's name for the step within its seq.
    sub_key: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepKey:
        return cls(seq=d["seq"], sub_key=d.get("sub_key", ""))


@dataclass
class StepStartRequest(Wire):
    step_key: StepKey
    task_name: str
    # The base64 of the step's arguments, as a JSON array.
    input_: str | Unset = field(default=UNSET, metadata={"wire_name": "input"})
    started_at: str | Unset = UNSET


@dataclass
class StepStartResponse(Wire):
    applied: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepStartResponse:
        return cls(applied=bool(d["applied"]))


@dataclass
class StepAttemptRequest(Wire):
    # A failed attempt that will be retried.
    step_key: StepKey
    attempt: int
    error: StepError
    started_at: str | Unset = UNSET


@dataclass
class StepAttemptResponse(Wire):
    applied: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepAttemptResponse:
        applied = d["applied"]
        if type(applied) is not bool:
            raise TypeError(f"step attempt applied must be a boolean, got {applied!r}")
        return cls(applied=applied)


@dataclass
class Payload(Wire):
    # The base64 of the encoded value.
    data: str
    # 1 is JSON, the only serializer.
    serializer: int = 1


@dataclass
class StepAttemptData(Wire):
    workflow_attempt: int


@dataclass
class StepAttempt(Wire):
    # The failed attempt that ends a step.
    session_id: str
    key: StepKey
    attempt: int
    started_at: str
    ended_at: str
    # A JSON StepError.
    error: Payload
    data: StepAttemptData | Unset = UNSET


@dataclass
class StepSuccess(Wire):
    """A step that completed without an error."""

    # Unset for a step without an output.
    output: Payload | Unset = UNSET


@dataclass
class StepOutcome(Wire):
    """A step's result: a success, or the failed attempt that ends it."""

    completed_at: str
    # The step-history proto's oneof: a success, or the final attempt.
    result: StepSuccess | StepAttempt

    def to_dict(self) -> dict[str, Any]:
        # The SDK server takes the oneof flattened: a success's output sits
        # beside completed_at, and the SDK server fills in its flow attempt.
        d: dict[str, Any] = {"completed_at": self.completed_at}
        if isinstance(self.result, StepSuccess):
            d.update(self.result.to_dict())
        else:
            d["final_attempt"] = self.result.to_dict()
        return d


@dataclass
class StepCompleteRequest(Wire):
    session_id: str
    key: StepKey
    outcome: StepOutcome

    def to_dict(self) -> dict[str, Any]:
        # The generic serialization would nest the oneof, so use the outcome's.
        return {**super().to_dict(), "outcome": self.outcome.to_dict()}


@dataclass
class StepCompleteResponse(Wire):
    applied: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepCompleteResponse:
        return cls(applied=bool(d["applied"]))


class StepType(str, Enum):
    """The kind of ctx call that recorded a step."""

    INLINE = "inline"
    DETACHED = "detached"
    SLEEP = "sleep"
    UNKNOWN = "unknown"
    """A type this SDK doesn't know, which replay reports rather than failing
    to parse."""

    @classmethod
    def _missing_(cls, value: object) -> StepType:
        return cls.UNKNOWN


# History records are only parsed off the wire, never sent, so absent
# fields are None rather than UNSET.
@dataclass
class StepRecord(Wire):
    step_key: StepKey
    type_: StepType = field(metadata={"wire_name": "type"})
    # The flow attempt that completed the step, 0 until then. A hint to how
    # many flow attempts the step took.
    workflow_attempt: int
    started_at: datetime
    task_name: str | None = None
    # The step's JSON arguments and output, decoded from the wire's base64.
    input_: str | None = field(default=None, metadata={"wire_name": "input"})
    output: str | None = None
    error: StepError | None = None
    # Set exactly when the step is finished.
    completed_at: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepRecord:
        return cls(
            step_key=StepKey.from_dict(d["step_key"]),
            type_=StepType(d["type"]),
            workflow_attempt=d["workflow_attempt"],
            started_at=parse_time(d["started_at"]),
            task_name=d.get("task_name"),
            input_=parse_base64(d["input"]) if d.get("input") else None,
            output=parse_base64(d["output"]) if d.get("output") else None,
            error=StepError.from_dict(d["error"]) if d.get("error") else None,
            completed_at=(
                parse_time(d["completed_at"]) if d.get("completed_at") else None
            ),
        )


@dataclass
class StepAttemptRecord(Wire):
    """A failed inline attempt of a step that hasn't finished.

    The SDK server only sends the attempts of open steps. Once a step
    finishes, its attempts no longer appear in the history."""

    step_key: StepKey
    attempt: int
    workflow_attempt: int
    error: StepError
    ended_at: datetime
    started_at: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StepAttemptRecord:
        return cls(
            step_key=StepKey.from_dict(d["step_key"]),
            attempt=d["attempt"],
            workflow_attempt=d["workflow_attempt"],
            error=StepError.from_dict(d["error"]),
            ended_at=parse_time(d["ended_at"]),
            started_at=parse_time(d["started_at"]) if d.get("started_at") else None,
        )
