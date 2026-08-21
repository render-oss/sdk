"""Pickle compatibility across the render_sdk -> render rename.

Pickles embed the defining module path of every class in GLOBAL opcodes
(``crender_sdk.workflows.task\\nRetry\\n`` in protocol 0). Because every leaf
module in the render_sdk mirror registers itself in ``sys.modules`` as the
real ``render.*`` module, unpickling data written by an old render_sdk 0.x
client must resolve those legacy paths to the real ``render`` classes — in a
cold process that has never imported either package.

The reverse is intentionally NOT supported: objects created through the
render_sdk shim ARE the real ``render.*`` classes, so pickles written by 1.x
embed ``render.workflows.task`` paths that a 0.x client cannot import. That
one-way break is accepted; test_forward_pickles_use_render_paths documents it.
"""

from __future__ import annotations

from conftest import run_py, run_py_json

# A protocol-0 pickle consisting of a single GLOBAL opcode under the legacy
# module path, as an old render_sdk 0.x client would have written it.
_LEGACY_CLASS_PICKLE = b"crender_sdk.workflows.task\nRetry\n."


def test_legacy_render_sdk_pickle_loads_cold() -> None:
    """A pickle written by render_sdk 0.x must load in a fresh 1.x process.

    Subprocess A builds the legacy payload: it pickles a real
    ``render.workflows.task.Retry`` at protocol 0, then rewrites the module
    path bytes to the pre-rename ``render_sdk.workflows.task`` (protocol-0
    GLOBAL opcodes are newline-terminated text, so the length change is safe).
    Subprocess B — which imports only ``pickle``/``base64``, never render —
    must unpickle it into the real class purely via pickle's own import of
    the legacy module path.
    """
    legacy_b64 = run_py_json(
        "import base64, json, pickle\n"
        "from render.workflows.task import Retry\n"
        "obj = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=1.5)\n"
        "payload = pickle.dumps(obj, protocol=0)\n"
        'assert payload.count(b"render.workflows.task") == 1\n'
        "legacy = payload.replace(\n"
        '    b"render.workflows.task", b"render_sdk.workflows.task"\n'
        ")\n"
        'print(json.dumps(base64.b64encode(legacy).decode("ascii")))\n'
    )

    loaded = run_py_json(
        "import base64, json, pickle\n"
        f"obj = pickle.loads(base64.b64decode({legacy_b64!r}))\n"
        "print(json.dumps({\n"
        '    "module": type(obj).__module__,\n'
        '    "qualname": type(obj).__qualname__,\n'
        '    "max_retries": obj.max_retries,\n'
        '    "wait_duration_ms": obj.wait_duration_ms,\n'
        '    "backoff_scaling": obj.backoff_scaling,\n'
        "}))\n"
    )
    assert loaded == {
        "module": "render.workflows.task",
        "qualname": "Retry",
        "max_retries": 3,
        "wait_duration_ms": 1000,
        "backoff_scaling": 1.5,
    }


def test_legacy_global_opcode_resolves_to_real_class() -> None:
    """A bare legacy GLOBAL opcode must resolve to the real Retry class.

    This isolates the resolution step from instance state: loading the
    class-only pickle in a cold process must yield the identical object as
    ``render.workflows.task.Retry``.
    """
    result = run_py_json(
        "import json, pickle, sys\n"
        f"cls = pickle.loads({_LEGACY_CLASS_PICKLE!r})\n"
        'real = sys.modules["render.workflows.task"].Retry\n'
        'print(json.dumps({"is_real": cls is real, "module": cls.__module__}))\n'
    )
    assert result == {"is_real": True, "module": "render.workflows.task"}


def test_forward_pickles_use_render_paths() -> None:
    """Pickles written through the shim embed the NEW module path.

    ``render_sdk.Retry`` IS ``render.workflows.task.Retry``, so pickling it
    writes ``render.workflows.task`` — never ``render_sdk`` — into the
    payload. Consequence (accepted, one-way break): pickles produced by 1.x
    clients cannot be read by old render_sdk 0.x clients, which have no
    ``render`` package to import.
    """
    result = run_py_json(
        "import json, pickle\n"
        "from render_sdk import Retry\n"
        "obj = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=1.5)\n"
        "payload = pickle.dumps(obj, protocol=0)\n"
        "print(json.dumps({\n"
        '    "has_render_path": b"render.workflows.task" in payload,\n'
        '    "has_legacy_path": b"render_sdk" in payload,\n'
        "}))\n"
    )
    assert result == {"has_render_path": True, "has_legacy_path": False}


def test_legacy_pickle_loader_never_imports_render_explicitly() -> None:
    """Guard the guard: the cold loader must rely on pickle's import alone.

    If neither render nor render_sdk is importable the legacy payload must
    fail to load — proving test_legacy_global_opcode_resolves_to_real_class
    is exercising pickle's module resolution, not a leaked ambient import.
    """
    result = run_py(
        "import pickle, sys\n"
        "import importlib.abc\n"
        "class _Block(importlib.abc.MetaPathFinder):\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        '        if name.split(".")[0] in ("render", "render_sdk"):\n'
        '            raise ModuleNotFoundError(f"blocked: {name}")\n'
        "        return None\n"
        "sys.meta_path.insert(0, _Block())\n"
        "try:\n"
        f"    pickle.loads({_LEGACY_CLASS_PICKLE!r})\n"
        "except ModuleNotFoundError:\n"
        "    pass\n"
        "else:\n"
        '    raise SystemExit("legacy pickle loaded without importing render")\n'
    )
    assert result.returncode == 0, result.stderr
