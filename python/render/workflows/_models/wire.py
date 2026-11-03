"""The UNSET sentinel and the generic serialization shared by every model."""

from __future__ import annotations

import base64
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any, cast

from dateutil.parser import isoparse


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
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class Wire:
    """Mixin providing the generic ``to_dict`` for every wire model."""

    def to_dict(self) -> dict[str, Any]:
        # `_wire` on a dataclass instance always returns a dict — the cast
        # documents that invariant for the type checker without a runtime hit.
        return cast("dict[str, Any]", _wire(self))


def parse_time(value: str) -> datetime:
    """Parse an RFC 3339 time, raising ValueError if it isn't one."""
    parsed = isoparse(value)
    # isoparse also takes ISO 8601 times without an offset, which RFC 3339
    # doesn't allow and which can't be compared with aware times.
    if parsed.utcoffset() is None:
        raise ValueError(f"time without a timezone: {value!r}")
    return parsed


def parse_base64(value: str) -> str:
    """Decode base64 text, raising ValueError if it isn't any."""
    return base64.b64decode(value, validate=True).decode()
