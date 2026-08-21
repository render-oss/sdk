"""Distribution metadata contracts for the render_sdk compatibility shim.

Installing ``render_sdk`` must pin the exact same version of ``render``
(including the key_value extra pass-through), and the shipped mirror must be
complete: a ``.pyi`` stub for every ``.py`` module and ``py.typed`` markers so
type checkers treat the shim as typed. These are properties of the installed
distribution, so they run against ``importlib.metadata`` in fresh
subprocesses.
"""

from __future__ import annotations

from conftest import run_py_json


def _normalize(requirement: str) -> str:
    """Normalize a requirement string for comparison.

    Metadata writers normalize extra names per PEP 685 (``key_value`` becomes
    ``key-value``) and differ in marker quoting, so fold both before matching.
    """
    return requirement.replace("_", "-").replace('"', "'")


def test_versions_match() -> None:
    """render_sdk and render are released in lockstep at the same version."""
    versions = run_py_json(
        "import importlib.metadata as im, json\n"
        "print(json.dumps([im.version('render_sdk'), im.version('render')]))\n"
    )
    assert versions == ["1.0.1", "1.0.1"]


def test_requires_pins_render_exactly() -> None:
    """The shim depends on render== (exact pin) and forwards the extra.

    ``render_sdk[key_value]`` must resolve to ``render[key_value]`` at the
    identical version, so users can swap the distribution name in their
    requirements without changing behavior.
    """
    requires = run_py_json(
        "import importlib.metadata as im, json\n"
        "print(json.dumps(im.requires('render_sdk')))\n"
    )
    assert requires, "render_sdk metadata lists no dependencies"
    normalized = [_normalize(req) for req in requires]

    assert any(req.startswith("render==") for req in normalized), normalized
    assert any(
        "render[key-value]==" in req and "extra == 'key-value'" in req
        for req in normalized
    ), normalized


def test_mirror_ships_stubs_and_py_typed_markers() -> None:
    """The installed mirror carries py.typed markers and a stub per module.

    Preferred source of truth is the dist-info RECORD via
    ``importlib.metadata.files()``. Under the default dev sync, however,
    render_sdk is installed EDITABLE and its RECORD lists only the .pth hook
    (no ``render_sdk/`` entries; on some installers ``files()`` is None), so
    we fall back to the source tree at ``Path(render_sdk.__file__).parent``,
    which is exactly what the editable install imports. The tox environments
    install with ``--no-editable`` and exercise the dist-info branch.
    """
    payload = run_py_json(
        "import importlib.metadata as im\n"
        "import json\n"
        "from pathlib import Path\n"
        "dist_files = im.files('render_sdk')\n"
        "entries = None\n"
        "if dist_files is not None:\n"
        "    entries = [\n"
        "        str(f) for f in dist_files if str(f).startswith('render_sdk/')\n"
        "    ]\n"
        "if entries:\n"
        "    mode = 'dist-info'\n"
        "else:\n"
        "    import render_sdk\n"
        "    root = Path(render_sdk.__file__).resolve().parent\n"
        "    entries = [\n"
        "        'render_sdk/' + p.relative_to(root).as_posix()\n"
        "        for p in root.rglob('*')\n"
        "        if p.is_file() and '__pycache__' not in p.relative_to(root).parts\n"
        "    ]\n"
        "    mode = 'source-tree'\n"
        "print(json.dumps({'mode': mode, 'files': entries}))\n"
    )
    files = payload["files"]
    context = f"mode={payload['mode']}, {len(files)} files"

    assert "render_sdk/py.typed" in files, context
    assert "render_sdk/public_api/py.typed" in files, context

    py_modules = [f for f in files if f.endswith(".py")]
    pyi_stubs = [f for f in files if f.endswith(".pyi")]
    assert py_modules, context
    missing_stubs = {f + "i" for f in py_modules} - set(pyi_stubs)
    orphan_stubs = set(pyi_stubs) - {f + "i" for f in py_modules}
    assert len(py_modules) == len(pyi_stubs), (
        f"{context}: {len(py_modules)} .py vs {len(pyi_stubs)} .pyi; "
        f"missing stubs: {sorted(missing_stubs)[:5]}; "
        f"orphan stubs: {sorted(orphan_stubs)[:5]}"
    )
