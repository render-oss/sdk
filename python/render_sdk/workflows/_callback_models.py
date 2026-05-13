"""Data models for the workflow callback API.

Only the fields the runner actually exchanges with the SDK server are
modelled here. Serialization is handled by the generic :func:`_wire`
helper and the :class:`_Wire` mixin, so each model is just a dataclass
declaration with no per-class ``to_dict`` body. ``from_dict`` is
explicit on the three classes the runner parses off the wire.

The module depends only on the standard library so it can sit on the
worker hot path — defining or running a task does not pull in
``httpx`` or ``attrs``.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, cast


class _Unset:
    """Sentinel for fields that were not provided on the wire.

    Mirrors the auto-generated ``Unset`` so callers can keep doing
    ``isinstance(value, Unset)`` checks. A single shared instance is used
    so identity comparisons (``is UNSET``) also work.
    """

    _instance: _Unset | None = None

    def __new__(cls) -> _Unset:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "UNSET"


Unset = _Unset
UNSET: _Unset = _Unset()


def _wire(obj: Any) -> Any:
    """Recursively convert a dataclass tree to wire-format dicts.

    Fields whose value is ``UNSET`` are dropped, matching the
    auto-generated ``to_dict`` behavior. Field names can be remapped for
    the wire via ``field(metadata={"wire_name": "..."})`` — used so the
    Python-keyword renames (``input_`` → ``input``, ``type_`` → ``type``)
    stay correct in JSON output.
    """
    if is_dataclass(obj):
        d: dict[str, Any] = {}
        for f in fields(obj):
            value = getattr(obj, f.name)
            if isinstance(value, _Unset):
                continue
            d[f.metadata.get("wire_name", f.name)] = _wire(value)
        return d
    if isinstance(obj, list):
        return [_wire(v) for v in obj]
    return obj


class _Wire:
    """Mixin providing the generic ``to_dict`` for every wire model below."""

    def to_dict(self) -> dict[str, Any]:
        # `_wire` on a dataclass instance always returns a dict — the cast
        # documents that invariant for the type checker without a runtime hit.
        return cast("dict[str, Any]", _wire(self))


@dataclass
class InputResponse(_Wire):
    task_name: str
    input_: str = field(metadata={"wire_name": "input"})

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InputResponse:
        return cls(task_name=d["task_name"], input_=d.get("input", ""))


@dataclass
class TaskComplete(_Wire):
    output: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskComplete:
        return cls(output=d["output"])


@dataclass
class TaskError(_Wire):
    details: str
    stack_trace: str | _Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskError:
        return cls(details=d["details"], stack_trace=d.get("stack_trace", UNSET))


@dataclass
class CallbackRequest(_Wire):
    error: TaskError | _Unset = UNSET
    complete: TaskComplete | _Unset = UNSET


@dataclass
class RunSubtaskRequest(_Wire):
    task_name: str
    input_: str | _Unset = field(default=UNSET, metadata={"wire_name": "input"})


@dataclass
class RunSubtaskResponse(_Wire):
    task_run_id: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RunSubtaskResponse:
        return cls(task_run_id=d["task_run_id"])


@dataclass
class SubtaskResultRequest(_Wire):
    task_run_id: str


@dataclass
class SubtaskResultResponse(_Wire):
    still_running: bool
    error: TaskError | _Unset = UNSET
    complete: TaskComplete | _Unset = UNSET

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SubtaskResultResponse:
        error: TaskError | _Unset = UNSET
        if d.get("error") is not None:
            error = TaskError.from_dict(d["error"])
        complete: TaskComplete | _Unset = UNSET
        if d.get("complete") is not None:
            complete = TaskComplete.from_dict(d["complete"])
        return cls(
            still_running=bool(d["still_running"]),
            error=error,
            complete=complete,
        )


@dataclass
class RetryConfig(_Wire):
    max_retries: int | _Unset = UNSET
    wait_duration_ms: int | _Unset = UNSET
    factor: float | _Unset = UNSET


@dataclass
class TaskOptions(_Wire):
    retry: RetryConfig | _Unset = UNSET
    timeout_seconds: int | _Unset = UNSET
    plan: str | _Unset = UNSET


@dataclass
class TaskParameter(_Wire):
    name: str
    has_default: bool
    type_: str | _Unset = field(default=UNSET, metadata={"wire_name": "type"})
    default_value: str | _Unset = UNSET


@dataclass
class Task(_Wire):
    name: str
    options: TaskOptions | _Unset = UNSET
    parameters: list[TaskParameter] | _Unset = UNSET


@dataclass
class Tasks(_Wire):
    tasks: list[Task]
