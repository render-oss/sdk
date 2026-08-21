"""Cold-import compatibility matrix for the ``render_sdk`` mirror package.

Every scenario runs in a fresh interpreter (via the conftest helpers): the
properties under test — cold-start importability, lazy-load side effects,
star-import surface, and worker-path import-graph slimness — belong to a
process that has not imported anything yet. pytest's own process has long
since imported both packages, so in-process assertions would prove nothing.

The laziness guard at the bottom mirrors the worker-path contract in
``python/render/workflows/tests/test_lazy_imports.py``: importing through
the compatibility name must not widen the import graph.
"""

from __future__ import annotations

import pytest
from conftest import run_py, run_py_json

# Keep in sync with render_sdk.__all__ (itself a mirror of render.__all__).
TOP_LEVEL_ALL: tuple[str, ...] = (
    "__version__",
    "Render",
    "RenderAsync",
    "Workflows",
    "TaskContext",
    "Options",
    "Retry",
    "start",
    "task",
)


def test_top_level_names_import_and_version_matches() -> None:
    """Every name in render_sdk.__all__ is importable; __version__ is 1.0.1."""
    names = ", ".join(TOP_LEVEL_ALL)
    code = (
        f"from render_sdk import {names}\nimport json\nprint(json.dumps(__version__))\n"
    )
    assert run_py_json(code) == "1.0.1"


def test_lazy_render_clients_resolve_and_materialize_real_modules() -> None:
    """Render/RenderAsync are lazy in the real package; importing them through
    render_sdk must still trigger the real lazy loader, materializing
    render.render and render.render_async in sys.modules."""
    code = (
        "from render_sdk import Render, RenderAsync\n"
        "assert Render is not None and RenderAsync is not None\n"
        "import json\n"
        "import sys\n"
        "print(json.dumps({\n"
        "    'render.render': 'render.render' in sys.modules,\n"
        "    'render.render_async': 'render.render_async' in sys.modules,\n"
        "}))\n"
    )
    assert run_py_json(code) == {
        "render.render": True,
        "render.render_async": True,
    }


# Deep imports that must each work as the FIRST statement of a fresh
# process (no prior `import render_sdk` to warm anything up).
DEEP_IMPORT_STATEMENTS: tuple[str, ...] = (
    "import render_sdk.client.errors",
    "from render_sdk.client.errors import TaskRunError",
    "from render_sdk.public_api import AuthenticatedClient",
    "import render_sdk.experimental.key_value",
    "import render_sdk.experimental.sandbox",
    "import render_sdk.workflows._callback_models",
    "import render_sdk.workflows._uds_http",
)


@pytest.mark.parametrize("statement", DEEP_IMPORT_STATEMENTS)
def test_deep_import_cold(statement: str) -> None:
    """A deep render_sdk import succeeds cold, as the first statement run."""
    result = run_py(statement)
    assert result.returncode == 0, f"cold `{statement}` failed:\n{result.stderr}"


def test_deep_import_via_importlib_resolves_to_real_leaf() -> None:
    """importlib.import_module on a generated leaf returns the real module.

    render_sdk/public_api/models/artifact.py exists in the generated mirror
    and aliases itself to render.public_api.models.artifact.
    """
    code = (
        "import importlib\n"
        "m = importlib.import_module('render_sdk.public_api.models.artifact')\n"
        "import json\n"
        "print(json.dumps({\n"
        "    'name': m.__name__,\n"
        "    'has_artifact': m.Artifact is not None,\n"
        "}))\n"
    )
    payload = run_py_json(code)
    assert payload["name"] == "render.public_api.models.artifact"
    assert payload["has_artifact"] is True


def test_client_attribute_access_delegates_to_real_module() -> None:
    """`render_sdk.client` attribute access resolves via __getattr__ delegation
    to the real (already-imported-on-the-worker-path) render.client module and
    is usable — its errors submodule is reachable."""
    code = (
        "import render_sdk\n"
        "c = render_sdk.client\n"
        "import json\n"
        "import types\n"
        "assert isinstance(c, types.ModuleType)\n"
        "assert c.errors.TaskRunError is not None\n"
        "print(json.dumps(c.__name__))\n"
    )
    assert run_py_json(code) == "render.client"


def test_star_import_top_level_binds_exactly_all() -> None:
    """`from render_sdk import *` binds exactly the __all__ names — the eight
    public names plus __version__ (star import honors __all__ even for the
    dunder listed there)."""
    code = (
        "ns = {}\n"
        "exec('from render_sdk import *', ns)\n"
        "import json\n"
        "bound = sorted(k for k in ns if not k.startswith('__'))\n"
        "print(json.dumps({\n"
        "    'bound': bound,\n"
        "    'has_version': '__version__' in ns,\n"
        "    'version': ns.get('__version__'),\n"
        "}))\n"
    )
    payload = run_py_json(code)
    assert payload["bound"] == sorted(n for n in TOP_LEVEL_ALL if n != "__version__")
    assert payload["has_version"] is True
    assert payload["version"] == "1.0.1"


@pytest.mark.parametrize("subpackage", ["workflows", "client"])
def test_star_import_subpackage_matches_real_all(subpackage: str) -> None:
    """Star import from a mirror subpackage binds exactly the real package's
    __all__. For client this exercises the mirror's package __getattr__ on
    top of the real package's lazy attribute loader."""
    code = (
        "ns = {}\n"
        f"exec('from render_sdk.{subpackage} import *', ns)\n"
        "import importlib\n"
        "import json\n"
        f"real = importlib.import_module('render.{subpackage}')\n"
        "bound = sorted(k for k in ns if not k.startswith('__'))\n"
        "print(json.dumps({'bound': bound, 'real_all': sorted(real.__all__)}))\n"
    )
    payload = run_py_json(code)
    assert payload["bound"] == payload["real_all"]


def test_star_import_leaf_module_matches_real_module() -> None:
    """Leaf modules ARE the real modules, so `from render_sdk.workflows.task
    import *` binds exactly what the real module's star import binds."""
    code = (
        "mirror_ns = {}\n"
        "exec('from render_sdk.workflows.task import *', mirror_ns)\n"
        "real_ns = {}\n"
        "exec('from render.workflows.task import *', real_ns)\n"
        "import json\n"
        "mirror = sorted(k for k in mirror_ns if not k.startswith('__'))\n"
        "real = sorted(k for k in real_ns if not k.startswith('__'))\n"
        "print(json.dumps({'mirror': mirror, 'real': real}))\n"
    )
    payload = run_py_json(code)
    assert payload["mirror"] == payload["real"]
    assert {"Options", "Retry", "task"} <= set(payload["mirror"])


# ---------------------------------------------------------------------------
# Worker-path laziness parity guard.
#
# Mirror of _FORBIDDEN_ON_WORKER_PATH / _ALLOWED_ON_WORKER_PATH in
# python/render/workflows/tests/test_lazy_imports.py, with each render.*
# entry checked under BOTH spellings: the mirror must not load anything the
# real worker path does not.
# ---------------------------------------------------------------------------

_FORBIDDEN_ON_WORKER_PATH: tuple[str, ...] = (
    # The REST API surface (Render / RenderAsync).
    "render.render",
    "render_sdk.render",
    "render.render_async",
    "render_sdk.render_async",
    # The auto-generated REST client + every model in it.
    "render.public_api",
    "render_sdk.public_api",
    # The hand-written REST client wrappers (allowed leaves listed below).
    "render.client",
    "render_sdk.client",
    # Object storage / experimental APIs.
    "render.experimental",
    "render_sdk.experimental",
    # Third-party HTTP/attribute libraries.
    "httpx",
    "httpcore",
    "attr",
    "attrs",
)

# Submodules of forbidden packages that ARE allowed on the worker path:
# client/__init__ is lazy and client.errors is shared with the UDS HTTP
# transport, so both may load (under either spelling).
_ALLOWED_ON_WORKER_PATH: frozenset[str] = frozenset(
    {
        "render.client",
        "render.client.errors",
        "render_sdk.client",
        "render_sdk.client.errors",
    }
)


def test_worker_path_stays_slim_through_the_mirror() -> None:
    """`from render_sdk import Workflows` must load no more than the real
    worker path does — no REST client, no models, no experimental code, no
    httpx/attrs — under either package spelling."""
    code = (
        "import sys\n"
        "from render_sdk import Workflows\n"
        "assert Workflows is not None\n"
        "import json\n"
        "print(json.dumps(sorted(sys.modules.keys())))\n"
    )
    loaded = set(run_py_json(code))

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
        + "\n\nSee python/render/workflows/tests/test_lazy_imports.py for "
        "the worker-path contract this mirrors."
    )
