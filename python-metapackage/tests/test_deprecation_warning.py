"""The render_sdk shim warns on import — exactly once, and only the shim.

Contract: importing ``render_sdk`` (any entry point into the mirror) emits
one DeprecationWarning telling users to migrate to ``render``; importing
``render`` itself must never warn. Warning emission is a property of a cold
interpreter, so every test here runs its import in a fresh subprocess with
explicit ``-W`` flags — pytest's own filters and long-imported modules would
otherwise mask both false positives and false negatives.
"""

from __future__ import annotations

from conftest import run_py

# Stable prefix of the warning message; the full text also names the package.
_RENAME_MESSAGE = "has been renamed to 'render'"


def test_import_render_sdk_raises_under_error_filter() -> None:
    """`-W error::DeprecationWarning` turns the shim's warning into a crash.

    This proves the warning is a real DeprecationWarning raised at import
    time, not text printed to stderr by other means.
    """
    result = run_py("import render_sdk", "-W", "error::DeprecationWarning")
    assert result.returncode != 0
    assert _RENAME_MESSAGE in result.stderr, result.stderr


def test_warning_emitted_exactly_once_across_submodule_imports() -> None:
    """Multiple render_sdk imports in one process warn exactly once.

    ``-W always`` disables deduplication by the warnings registry, so a
    second emission anywhere in the mirror (a submodule warning on import,
    say) would show up as a second occurrence here.
    """
    result = run_py(
        "import render_sdk, render_sdk.workflows, "
        "render_sdk.client.errors, render_sdk.workflows.task",
        "-W",
        "always",
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr.count(_RENAME_MESSAGE) == 1, result.stderr


def test_import_render_never_warns() -> None:
    """The real package must import cleanly even under the error filter."""
    result = run_py("import render", "-W", "error::DeprecationWarning")
    assert result.returncode == 0, result.stderr
    assert _RENAME_MESSAGE not in result.stderr, result.stderr


def test_warning_visible_under_default_filters_in_main() -> None:
    """`python -c "import render_sdk"` shows the warning out of the box.

    Python's default filters show DeprecationWarning only when it is
    triggered from ``__main__`` — which a direct import like this one is.
    Accepted limitation: when render_sdk is imported by library code (any
    module other than ``__main__``), the default filters suppress the
    message; users of such libraries only see it under ``-W always``/
    ``-W error`` or in test runners that enable DeprecationWarning.
    """
    result = run_py("import render_sdk")
    assert result.returncode == 0, result.stderr
    assert _RENAME_MESSAGE in result.stderr, result.stderr
