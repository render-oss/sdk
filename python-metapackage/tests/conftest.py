"""Shared helpers for the render_sdk compatibility test suite.

Every test runs its imports in a fresh interpreter: the compatibility
guarantees under test (cold-start imports, sys.modules identity, warning
emission, `python -m` behavior) are all properties of a process that has not
imported anything yet, and pytest's own process has long since imported both
packages.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from typing import Any

# Subprocesses must import render_sdk from the INSTALLED distribution, never
# from this project's source tree: with an inherited cwd, sys.path[0] would be
# python-metapackage/ and ./render_sdk would shadow site-packages, letting a
# broken wheel (e.g. a subtree dropped by a packaging regression) test green.
# A neutral cwd covers Python 3.10; PYTHONSAFEPATH (3.11+) hardens -c/-m runs.
_NEUTRAL_CWD = tempfile.mkdtemp(prefix="render-sdk-compat-tests-")


def _clean_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONSAFEPATH"] = "1"
    # A caller's warning filters must not leak into the subprocess.
    env.pop("PYTHONWARNINGS", None)
    return env


def run_py(code: str, *flags: str) -> subprocess.CompletedProcess[str]:
    """Run `python [flags] -c code` in a fresh interpreter."""
    return subprocess.run(  # noqa: S603 — code is a test-authored literal
        [sys.executable, *flags, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        cwd=_NEUTRAL_CWD,
    )


def run_py_json(code: str, *flags: str) -> Any:
    """Run code that prints a single JSON document on stdout; parse it.

    Fails loudly (with the subprocess's stderr) if the interpreter exits
    nonzero or prints something that is not JSON.
    """
    result = run_py(code, *flags)
    assert result.returncode == 0, (  # noqa: S101
        f"subprocess failed (rc={result.returncode}):\n"
        f"--- code ---\n{code}\n--- stderr ---\n{result.stderr}"
    )
    return json.loads(result.stdout)


def run_module(
    module: str, *args: str, flags: tuple[str, ...] = ()
) -> subprocess.CompletedProcess[str]:
    """Run `python [flags] -m module [args]` in a fresh interpreter."""
    return subprocess.run(  # noqa: S603 — module/args are test-authored literals
        [sys.executable, *flags, "-m", module, *args],
        capture_output=True,
        text=True,
        env=_clean_env(),
        cwd=_NEUTRAL_CWD,
    )
