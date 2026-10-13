"""Wall-clock startup timestamps reported to the server on ``GET /input``.

Imported first by ``render/__init__.py`` so the import start is the earliest
point SDK code runs. Stdlib only, to stay cheap.
"""

import time

_import_started_ns: int | None = time.time_ns()
_import_finished_ns: int | None = None
_sdk_started_ns: int | None = None


def mark_import_finished() -> None:
    global _import_finished_ns
    if _import_finished_ns is None:
        _import_finished_ns = time.time_ns()


def mark_sdk_started() -> None:
    global _sdk_started_ns
    if _sdk_started_ns is None:
        _sdk_started_ns = time.time_ns()


def input_query() -> str:
    """Return ``?k=v&...`` for the timestamps that were captured, or ``""``."""
    params = (
        ("sdk_import_started_at", _import_started_ns),
        ("sdk_import_finished_at", _import_finished_ns),
        ("sdk_started_at", _sdk_started_ns),
    )
    parts = [f"{name}={value}" for name, value in params if value]
    return "?" + "&".join(parts) if parts else ""
