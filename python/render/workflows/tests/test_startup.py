"""Tests for the startup timestamps reported on GET /input."""

import subprocess
import sys
import time

from render import _startup
from render.workflows import runner


def test_run_records_sdk_started_before_running(monkeypatch):
    monkeypatch.setattr(_startup, "_sdk_started_ns", None)
    seen: list[int | None] = []

    async def fake_run_async(socket_path: str) -> None:
        seen.append(_startup._sdk_started_ns)

    monkeypatch.setattr(runner, "run_async", fake_run_async)

    before = time.time_ns()
    runner.run("/unused.sock")
    after = time.time_ns()

    assert seen[0] is not None
    assert before <= seen[0] <= after


def test_mark_sdk_started_keeps_first_value(monkeypatch):
    monkeypatch.setattr(_startup, "_sdk_started_ns", 5)
    _startup.mark_sdk_started()
    assert _startup._sdk_started_ns == 5


def test_import_timestamps_are_ordered_in_a_fresh_interpreter():
    code = (
        "import time; t0 = time.time_ns()\n"
        "import render\n"
        "t1 = time.time_ns()\n"
        "from render import _startup as s\n"
        "assert t0 <= s._import_started_ns <= s._import_finished_ns <= t1\n"
        "assert s._sdk_started_ns is None\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True)  # noqa: S603
