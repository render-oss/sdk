"""Regression guards for real-module ``__spec__`` integrity.

The previous dynamic shim implemented ``render_sdk`` as a ``sys.meta_path``
finder whose ``create_module`` returned the already-imported real module.
importlib then "initialized" that module object a second time, clobbering the
real module's ``__spec__`` — which silently broke ``importlib.reload``,
``importlib.resources``, and anything else that trusts a module's spec.

The static mirror must never touch the real modules' import-system metadata:
after importing any mix of ``render_sdk`` modules, every ``render.*`` module's
spec must look exactly as the normal import system created it, and the mirror
packages must keep their own specs.

Every test runs in a fresh interpreter (see conftest) and imports the mirror
first — the top-level package, a subpackage, a leaf module, and a nested leaf —
before inspecting the real package.
"""

from __future__ import annotations

from conftest import run_py_json

# Imported at the top of every subprocess: exercising the top-level package,
# a subpackage, a leaf under it, and a leaf in a *different* subpackage is
# what tripped the old finder-based shim.
_IMPORT_MIRROR_FIRST = (
    "import render_sdk\n"
    "import render_sdk.workflows\n"
    "import render_sdk.workflows.task\n"
    "import render_sdk.client.errors\n"
)


def test_real_package_spec_is_intact_after_mirror_imports() -> None:
    info = run_py_json(
        _IMPORT_MIRROR_FIRST
        + "import json\n"
        + "import render.workflows\n"
        + "spec = render.workflows.__spec__\n"
        + "print(json.dumps({\n"
        + "    'name': spec.name,\n"
        + "    'origin': spec.origin,\n"
        + "    'search': list(spec.submodule_search_locations or []),\n"
        + "}))\n"
    )
    assert info["name"] == "render.workflows"
    assert info["origin"].endswith("render/workflows/__init__.py")
    assert info["search"], "package spec lost its submodule_search_locations"
    assert info["search"][0].endswith("render/workflows")


def test_real_leaf_spec_is_intact_after_mirror_imports() -> None:
    # ``render.workflows.task`` the *attribute* is the ``task`` decorator
    # (it shadows the submodule), so the module is fetched via sys.modules.
    info = run_py_json(
        _IMPORT_MIRROR_FIRST
        + "import json\n"
        + "import sys\n"
        + "spec = sys.modules['render.workflows.task'].__spec__\n"
        + "print(json.dumps({\n"
        + "    'name': spec.name,\n"
        + "    'origin': spec.origin,\n"
        + "    'search': spec.submodule_search_locations,\n"
        + "}))\n"
    )
    assert info["name"] == "render.workflows.task"
    assert info["origin"].endswith("render/workflows/task.py")
    assert info["search"] is None, "a leaf module must not carry search locations"


def test_real_package_survives_importlib_reload() -> None:
    """``importlib.reload`` needs an intact spec; the old shim broke it."""
    info = run_py_json(
        _IMPORT_MIRROR_FIRST
        + "import importlib\n"
        + "import json\n"
        + "import sys\n"
        + "import render.workflows\n"
        + "reloaded = importlib.reload(render.workflows)\n"
        + "print(json.dumps({\n"
        + "    'name': render.workflows.__name__,\n"
        + "    'same_object': reloaded is sys.modules['render.workflows'],\n"
        + "    'workflows_module': render.workflows.Workflows.__module__,\n"
        + "}))\n"
    )
    assert info["name"] == "render.workflows"
    assert info["same_object"] is True
    assert info["workflows_module"] == "render.workflows.app"


def test_importlib_resources_resolves_real_package() -> None:
    """``importlib.resources`` walks the spec to find package data."""
    info = run_py_json(
        _IMPORT_MIRROR_FIRST
        + "import importlib.resources\n"
        + "import json\n"
        + "path = importlib.resources.files('render.workflows')\n"
        + "print(json.dumps({'path': str(path)}))\n"
    )
    assert info["path"].endswith("render/workflows")


def test_mirror_package_keeps_its_own_spec() -> None:
    """Mirror *packages* have their own identity (unlike leaf modules, which
    alias themselves to the real module), so their specs must stay theirs."""
    info = run_py_json(
        _IMPORT_MIRROR_FIRST
        + "import json\n"
        + "import sys\n"
        + "spec = sys.modules['render_sdk.workflows'].__spec__\n"
        + "print(json.dumps({'name': spec.name}))\n"
    )
    assert info["name"] == "render_sdk.workflows"
