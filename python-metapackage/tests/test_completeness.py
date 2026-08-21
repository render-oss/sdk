"""Exhaustive anti-regression sweep over the entire `render_sdk` mirror.

This is the test that guarantees NO module and NO public symbol of the real
`render` package is unreachable — or reachable but non-identical — through
the generated `render_sdk` compatibility mirror. Everything else in this
suite spot-checks a handful of representative modules; this test walks the
whole tree:

* every ``render.x.y`` module must also import as ``render_sdk.x.y``;
* every leaf module must be the *same object* under both names (the shim
  replaces itself in ``sys.modules`` with the real module);
* every package mirror (``__init__.py``), which keeps its own module
  identity, must delegate every public attribute to the identical object on
  the real package, and its ``__all__`` must match the real one exactly;
* inversely, the mirror must contain no orphan modules (a ``.py`` with no
  real counterpart — e.g. a module deleted from `render` after the mirror
  was last generated) and every mirror module must ship a sibling ``.pyi``
  stub so type checkers resolve the old names.

If this test fails after changing the real package, regenerate the mirror
with ``scripts/generate_mirror.py``.

The whole sweep runs in ONE fresh interpreter (importing ~791 modules takes
a few seconds); the subprocess collects failures instead of raising and
reports them as a single JSON document.
"""

from __future__ import annotations

from typing import Any

import pytest
from conftest import run_py_json

_SWEEP_CODE = """
import importlib
import importlib.util
import json
import sys
import types
from pathlib import Path

# Resolve the mirror's on-disk location up front, straight from the import
# system, before anything has been imported (once render_sdk is imported,
# sys.modules entries for leaves point at the *real* package's files).
mirror_root = Path(
    importlib.util.find_spec("render_sdk").submodule_search_locations[0]
)

import render

real_root = Path(render.__file__).resolve().parent


def walk_modules(root, top):
    "Yield (dotted_name, is_package) for every *.py under root."
    out = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        parts = list(path.relative_to(root).with_suffix("").parts)
        is_package = parts[-1] == "__init__"
        if is_package:
            parts = parts[:-1]
        out.append((".".join([top, *parts]), is_package))
    return out


import_failures = []    # [real_name, repr(exc)]
identity_failures = []  # [real_name, detail]
attr_failures = []      # [real_name, attr, detail]
all_mismatches = []     # [real_name, real __all__, shim __all__]
orphan_shims = []       # mirror files with no real counterpart
missing_stubs = []      # mirror files with no sibling .pyi

# --- Pass 1: import every module under BOTH names; leaves must be one object.
real_modules = walk_modules(real_root, "render")
loaded = []
for real_name, is_package in real_modules:
    shim_name = "render_sdk" + real_name[len("render"):]
    try:
        real_mod = importlib.import_module(real_name)
        shim_mod = importlib.import_module(shim_name)
    except Exception as exc:
        import_failures.append([real_name, repr(exc)])
        continue
    loaded.append((real_name, shim_name, is_package, real_mod, shim_mod))
    if not is_package and shim_mod is not real_mod:
        identity_failures.append(
            [real_name, "shim leaf module is not the real module object"]
        )

# --- Pass 2: with the full tree imported, every public attribute of every
# package must resolve through the shim to the *identical* object.
for real_name, shim_name, is_package, real_mod, shim_mod in loaded:
    if not is_package:
        continue
    real_all = getattr(real_mod, "__all__", None)
    if real_all is not None:
        shim_all = getattr(shim_mod, "__all__", None)
        if shim_all is None or list(shim_all) != list(real_all):
            all_mismatches.append(
                [
                    real_name,
                    list(real_all),
                    None if shim_all is None else list(shim_all),
                ]
            )
        names = list(real_all)
    else:
        names = [n for n in dir(real_mod) if not n.startswith("_")]
    for attr in names:
        try:
            real_val = getattr(real_mod, attr)
        except Exception as exc:
            attr_failures.append(
                [real_name, attr, "getattr on REAL package failed: " + repr(exc)]
            )
            continue
        try:
            shim_val = getattr(shim_mod, attr)
        except Exception as exc:
            attr_failures.append(
                [real_name, attr, "getattr on shim failed: " + repr(exc)]
            )
            continue
        if shim_val is real_val:
            continue
        # This sweep itself imported every submodule under both names, and
        # the import machinery binds each imported submodule as an attribute
        # on its parent package — on shim packages that binding shadows the
        # generated __getattr__ delegation. Such a binding is legitimate:
        # the bound object is the mirror counterpart of the real submodule
        # (the identical module for leaves — pass 1 — and the mirror
        # subpackage for packages, whose own attributes this loop checks
        # separately). Still require that the generated delegation resolves
        # the name to the identical real object: that is what a user who has
        # not imported the submodule observes.
        shadowing_submodule = isinstance(shim_val, types.ModuleType) and (
            sys.modules.get(shim_name + "." + attr) is shim_val
        )
        delegate = vars(shim_mod).get("__getattr__")
        try:
            delegated_ok = delegate is not None and delegate(attr) is real_val
        except Exception:
            delegated_ok = False
        if shadowing_submodule and delegated_ok:
            continue
        attr_failures.append(
            [real_name, attr, "shim attribute is a different object"]
        )

# --- Pass 3 (inverse): no orphan mirror modules, and a .pyi stub for each.
for path in sorted(mirror_root.rglob("*.py")):
    if "__pycache__" in path.parts:
        continue
    rel = path.relative_to(mirror_root)
    if not (real_root / rel).exists():
        orphan_shims.append(str(rel))
    if not path.with_suffix(".pyi").exists():
        missing_stubs.append(str(rel))

print(
    json.dumps(
        {
            "modules_checked": len(real_modules),
            "import_failures": import_failures,
            "identity_failures": identity_failures,
            "attr_failures": attr_failures,
            "all_mismatches": all_mismatches,
            "orphan_shims": orphan_shims,
            "missing_stubs": missing_stubs,
        }
    )
)
"""


@pytest.fixture(scope="module")
def sweep() -> dict[str, Any]:
    """Run the full sweep once (one subprocess) and share it across tests."""
    return run_py_json(_SWEEP_CODE)


def _explain(label: str, failures: list[Any], hint: str) -> str:
    lines = "\n".join(f"  - {failure!r}" for failure in failures)
    return f"{label} ({len(failures)} failures):\n{lines}\n\n{hint}"


_REGEN_HINT = (
    "The render_sdk mirror is out of sync with the real render package. "
    "Regenerate it: uv run python scripts/generate_mirror.py"
)


def test_sweep_covered_the_full_module_tree(sweep: dict[str, Any]) -> None:
    """Sanity: the walk actually found the whole render tree (~791 modules).

    If this ever drops below the threshold, the sweep is walking the wrong
    directory (or the package layout changed radically) and every green
    result below is meaningless.
    """
    assert sweep["modules_checked"] > 700, (
        f"Sweep only found {sweep['modules_checked']} modules under the real "
        "render package; expected > 700. The walk is probably rooted at the "
        "wrong directory."
    )


def test_every_render_module_imports_under_both_names(
    sweep: dict[str, Any],
) -> None:
    """Every render.x.y must import cleanly as BOTH render.x.y and
    render_sdk.x.y — a module missing from the mirror makes old imports
    raise ModuleNotFoundError for downstream users."""
    assert not sweep["import_failures"], _explain(
        "Modules that failed to import under one of their two names",
        sweep["import_failures"],
        _REGEN_HINT,
    )


def test_every_leaf_module_is_the_same_object_under_both_names(
    sweep: dict[str, Any],
) -> None:
    """Leaf shims replace themselves in sys.modules with the real module, so
    `render_sdk.x.y is render.x.y`. Anything less breaks isinstance checks,
    module-level singletons, and monkeypatching across the two names."""
    assert not sweep["identity_failures"], _explain(
        "Leaf modules that are NOT the identical object under both names",
        sweep["identity_failures"],
        _REGEN_HINT,
    )


def test_every_public_package_attribute_is_the_identical_object(
    sweep: dict[str, Any],
) -> None:
    """Package mirrors keep their own module identity but must delegate every
    public attribute (per __all__ when present, else every non-underscore
    name) to the *identical* object on the real package."""
    assert not sweep["attr_failures"], _explain(
        "Package attributes that differ (or failed) between shim and real",
        sweep["attr_failures"],
        _REGEN_HINT,
    )


def test_every_package_all_matches_the_real_package(
    sweep: dict[str, Any],
) -> None:
    """Where the real package defines __all__, the mirror's literal __all__
    must match it exactly — `from render_sdk.pkg import *` must export
    precisely what `from render.pkg import *` does."""
    assert not sweep["all_mismatches"], _explain(
        "Packages whose shim __all__ differs from the real __all__",
        sweep["all_mismatches"],
        _REGEN_HINT,
    )


def test_mirror_contains_no_orphan_modules(sweep: dict[str, Any]) -> None:
    """Inverse sweep: every mirror .py must have a real counterpart. An
    orphan means a module was removed from render but its shim still imports
    a module that no longer exists (or shadows a deletion)."""
    assert not sweep["orphan_shims"], _explain(
        "Mirror modules with no corresponding module in the real package",
        sweep["orphan_shims"],
        _REGEN_HINT,
    )


def test_every_mirror_module_has_a_type_stub(sweep: dict[str, Any]) -> None:
    """Every mirror .py must ship a sibling .pyi so type checkers resolve
    render_sdk imports to the real types (the runtime alias is invisible to
    static analysis)."""
    assert not sweep["missing_stubs"], _explain(
        "Mirror modules missing a sibling .pyi stub",
        sweep["missing_stubs"],
        _REGEN_HINT,
    )
