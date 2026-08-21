"""``python -m`` parity between the render_sdk mirror and the real package.

Every leaf module in the mirror carries a ``__main__`` branch that re-runs the
real module via ``runpy.run_module(..., run_name="__main__", alter_sys=True)``,
so ``python -m render_sdk.x.y`` must behave exactly like
``python -m render.x.y``: same exit code, same stdout, and the same stderr
apart from the mirror's one-time DeprecationWarning.

Packages have no ``__main__`` branch on either side, so both spellings must
fail the same way when run with ``-m``.
"""

from __future__ import annotations

import subprocess

from conftest import run_module


def _scrub_warnings(stderr: str) -> str:
    """Drop the mirror's DeprecationWarning noise from stderr.

    Depending on the active warning filters the warning surfaces as a
    ``...: DeprecationWarning: ...`` line, optionally followed by a
    ``warnings.warn(...)`` source-context echo. Everything else — including
    any RuntimeWarning runpy emits identically on both sides — is kept
    verbatim so real divergences still fail the comparison.
    """
    kept = [
        line
        for line in stderr.splitlines()
        if "DeprecationWarning" not in line and "warnings.warn" not in line
    ]
    return "\n".join(kept)


def _assert_parity(
    shim: subprocess.CompletedProcess[str],
    real: subprocess.CompletedProcess[str],
) -> None:
    assert shim.returncode == real.returncode, (
        f"returncode diverged: shim={shim.returncode} real={real.returncode}\n"
        f"shim stderr:\n{shim.stderr}\nreal stderr:\n{real.stderr}"
    )
    assert shim.stdout == real.stdout
    assert _scrub_warnings(shim.stderr) == _scrub_warnings(real.stderr)


def test_cli_no_args_matches_real_cli() -> None:
    shim = run_module("render_sdk.workflows.cli")
    real = run_module("render.workflows.cli")
    _assert_parity(shim, real)
    assert real.returncode == 1
    assert "Usage: render-workflows <module:app>" in real.stderr
    assert "Example: render-workflows myapp:app" in real.stderr


def test_cli_unimportable_app_target_matches_real_cli() -> None:
    shim = run_module("render_sdk.workflows.cli", "bogus_module_xyz:app")
    real = run_module("render.workflows.cli", "bogus_module_xyz:app")
    _assert_parity(shim, real)
    assert real.returncode == 1
    assert "Could not import module 'bogus_module_xyz'" in real.stderr


def test_cli_malformed_app_path_matches_real_cli() -> None:
    shim = run_module("render_sdk.workflows.cli", "no_colon_here")
    real = run_module("render.workflows.cli", "no_colon_here")
    _assert_parity(shim, real)
    assert real.returncode == 1
    assert "Error: Invalid app path 'no_colon_here'" in real.stderr


def test_top_level_packages_are_equally_not_runnable() -> None:
    shim = run_module("render_sdk")
    real = run_module("render")
    assert shim.returncode != 0
    assert shim.returncode == real.returncode
    assert "No module named render_sdk.__main__" in shim.stderr
    assert "No module named render.__main__" in real.stderr


def test_subpackages_are_equally_not_runnable() -> None:
    shim = run_module("render_sdk.workflows")
    real = run_module("render.workflows")
    assert shim.returncode != 0
    assert shim.returncode == real.returncode
    assert "No module named render_sdk.workflows.__main__" in shim.stderr
    assert "No module named render.workflows.__main__" in real.stderr


def test_leaf_module_without_main_guard_runs_cleanly() -> None:
    """Arbitrary leaves are ``-m`` runnable, not just the CLI.

    ``render.workflows.task`` has no ``if __name__ == "__main__"`` block, so
    both spellings must import-and-exit 0 with no stdout.
    """
    shim = run_module("render_sdk.workflows.task")
    real = run_module("render.workflows.task")
    _assert_parity(shim, real)
    assert real.returncode == 0
    assert real.stdout == ""
