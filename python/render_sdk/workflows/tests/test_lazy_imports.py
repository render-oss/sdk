"""Regression guard for the worker import graph.

The worker path (``from render_sdk import Workflows``) deliberately avoids
loading the REST API client, the public_api models, and the experimental
object storage code, since none of them are needed to run a task. Keeping
the import graph slim is what keeps the workflow path fast.

If you find yourself adding an eager top-level ``from render_sdk.<heavy>
import ...`` to a module on the worker path, lazy-load it instead — see
``render_sdk/__init__.py`` and ``render_sdk/client/__init__.py`` for the
pattern. If a fresh module truly belongs on the worker path, add it here
and document why.
"""

from __future__ import annotations

import json
import subprocess
import sys

# Modules that must NOT be loaded by `from render_sdk import Workflows`.
# Each entry matches the module itself and any submodule under it.
_FORBIDDEN_ON_WORKER_PATH: tuple[str, ...] = (
    # The REST API surface (Render / RenderAsync).
    "render_sdk.render",
    "render_sdk.render_async",
    # The auto-generated REST client + every model in it.
    "render_sdk.public_api.models",
    # The hand-written REST client wrappers (Client, WorkflowsService, etc.)
    # plus client.types and client.sse. Worker-path leaf modules are listed
    # in _ALLOWED_ON_WORKER_PATH below.
    "render_sdk.client",
    # Object storage / experimental APIs.
    "render_sdk.experimental",
)

# Submodules of forbidden packages that ARE allowed on the worker path.
_ALLOWED_ON_WORKER_PATH: frozenset[str] = frozenset(
    {
        # Loaded transitively when runner.py imports client.errors / client.util.
        # The package init itself is now lazy, so this is harmless.
        "render_sdk.client",
        "render_sdk.client.errors",
        "render_sdk.client.util",
    }
)


def _modules_loaded_by(import_statement: str) -> set[str]:
    """Run the given import in a fresh interpreter and return sys.modules."""
    code = (
        "import sys\n"
        f"{import_statement}\n"
        "import json\n"
        "print(json.dumps(sorted(sys.modules.keys())))\n"
    )
    result = (
        subprocess.run(  # noqa: S603 — code is a constructed literal, not user input
            [sys.executable, "-c", code],
            check=True,
            capture_output=True,
            text=True,
        )
    )
    return set(json.loads(result.stdout))


def test_worker_path_does_not_load_rest_or_experimental_modules() -> None:
    loaded = _modules_loaded_by("from render_sdk import Workflows")

    leaked: list[str] = []
    for module in sorted(loaded):
        if module in _ALLOWED_ON_WORKER_PATH:
            continue
        for forbidden in _FORBIDDEN_ON_WORKER_PATH:
            if module == forbidden or module.startswith(forbidden + "."):
                leaked.append(module)
                break

    assert not leaked, (
        "Importing `render_sdk.Workflows` eagerly loaded modules that are "
        "off the worker hot path:\n  - "
        + "\n  - ".join(leaked)
        + "\n\nLazy-load the offending imports or move them inside the "
        "function bodies where they're used. See the module docstring of "
        "test_lazy_imports.py for the contract."
    )


def test_lazy_attrs_still_resolve_when_explicitly_accessed() -> None:
    """Smoke check: the lazy machinery must keep `from render_sdk import
    Render` working — otherwise the leak guard above could be satisfied by
    simply breaking the symbol."""
    loaded = _modules_loaded_by(
        "from render_sdk import Render, RenderAsync, Workflows; "
        "assert Render is not None and RenderAsync is not None "
        "and Workflows is not None"
    )
    assert "render_sdk.render" in loaded
    assert "render_sdk.render_async" in loaded
