"""Object-identity guarantees of the ``render_sdk`` mirror.

The generated mirror makes two deliberately different promises:

* **Leaf modules alias.** Every leaf ``render_sdk/x/y.py`` replaces itself in
  ``sys.modules`` with ``render.x.y`` at import time, so the module — and
  every class, function, and exception defined in it — is the SAME object
  under both names. isinstance/except/is checks interoperate for free.

* **Packages delegate, not alias.** Each ``render_sdk`` package ``__init__``
  keeps its OWN identity in ``sys.modules`` (aliasing a package would point
  its ``__path__`` at the real directory and make child imports re-execute
  real sources under ``render_sdk`` names) but forwards ALL attribute access
  to the real package, and drops any child-module binding the import system
  would setattr onto it that diverges from the real package's attribute. Net
  effect: every attribute reachable through a ``render_sdk`` path — including
  package attributes themselves — is the real object; only the ``sys.modules``
  entries for packages differ.

Every test runs in a fresh interpreter: identity is a property of a cold
``sys.modules``, and pytest's process has already imported everything.
"""

from __future__ import annotations

from conftest import run_py_json


def test_leaf_module_is_same_object_under_both_names() -> None:
    """A leaf module aliases itself: both sys.modules entries are one object."""
    code = (
        "import render_sdk.workflows.task\n"
        "import json\n"
        "import sys\n"
        "print(json.dumps(\n"
        "    sys.modules['render_sdk.workflows.task']\n"
        "    is sys.modules['render.workflows.task']\n"
        "))\n"
    )
    assert run_py_json(code) is True


def test_every_public_attribute_is_the_real_object() -> None:
    """getattr through render_sdk returns the identical object as through
    render, for every __all__ name at every package level. The client level
    is lazy in the real package, so this also forces materialization through
    the mirror's __getattr__ chain."""
    code = (
        "import render\n"
        "import render_sdk\n"
        "import render.client\n"
        "import render.experimental\n"
        "import render.workflows\n"
        "import render_sdk.client\n"
        "import render_sdk.experimental\n"
        "import render_sdk.workflows\n"
        "import json\n"
        "pairs = [\n"
        "    (render_sdk, render, render.__all__),\n"
        "    (render_sdk.workflows, render.workflows, render.workflows.__all__),\n"
        "    (render_sdk.client, render.client, render.client.__all__),\n"
        "    (\n"
        "        render_sdk.experimental,\n"
        "        render.experimental,\n"
        "        render.experimental.__all__,\n"
        "    ),\n"
        "]\n"
        "mismatches = [\n"
        "    f'{real.__name__}.{name}'\n"
        "    for mirror, real, names in pairs\n"
        "    for name in names\n"
        "    if getattr(mirror, name) is not getattr(real, name)\n"
        "]\n"
        "print(json.dumps(mismatches))\n"
    )
    assert run_py_json(code) == []


def test_package_sys_modules_identity_differs_but_attribute_access_aliases() -> None:
    """Packages are delegating mirrors: the sys.modules entry keeps its own
    render_sdk.* identity for the import machinery, but ATTRIBUTE access to a
    package through render_sdk yields the real package object (the mirror
    drops the import system's diverging child binding and delegates instead;
    see module docstring)."""
    code = (
        "import render_sdk.workflows\n"
        "import render.workflows\n"
        "import render_sdk\n"
        "import json\n"
        "import sys\n"
        "mirror = sys.modules['render_sdk.workflows']\n"
        "print(json.dumps({\n"
        "    'distinct': mirror is not sys.modules['render.workflows'],\n"
        "    'name': mirror.__name__,\n"
        "    'attr_is_real': render_sdk.workflows is render.workflows,\n"
        "}))\n"
    )
    payload = run_py_json(code)
    assert payload["distinct"] is True
    assert payload["name"] == "render_sdk.workflows"
    assert payload["attr_is_real"] is True


def test_child_import_does_not_shadow_the_task_decorator() -> None:
    """Regression guard for submodule shadowing. On the real package,
    ``render.workflows.task`` the ATTRIBUTE is the task decorator (bound by
    ``render/workflows/__init__.py`` after the submodule import), not the
    ``render.workflows.task`` module. A naive mirror inverts that: once any
    code runs ``import render_sdk.workflows.task``, the import system binds
    the submodule onto the mirror package, shadowing the delegated decorator
    — so ``@render_sdk.workflows.task`` would raise 'module is not callable'
    depending on import order elsewhere in the program. The mirror's
    __setattr__ drops that diverging binding."""
    code = (
        "import render_sdk.workflows.task  # the shadowing trigger\n"
        "import render.workflows\n"
        "import render_sdk\n"
        "import json\n"
        "decorated = render_sdk.workflows.task(lambda ctx, x: x)\n"
        "print(json.dumps({\n"
        "    'is_decorator': render_sdk.workflows.task\n"
        "    is render.workflows.task,\n"
        "    'callable': callable(render_sdk.workflows.task),\n"
        "    'decorated_type': type(decorated).__name__,\n"
        "}))\n"
    )
    payload = run_py_json(code)
    assert payload["is_decorator"] is True
    assert payload["callable"] is True
    assert payload["decorated_type"] == "TaskDefinition"


def test_exception_interop_in_both_directions() -> None:
    """TaskRunError is one class under both names, so an exception raised via
    either spelling is caught by an except clause written in the other."""
    code = (
        "import render.client.errors as real_errors\n"
        "import render_sdk.client.errors as mirror_errors\n"
        "import json\n"
        "results = {}\n"
        "try:\n"
        "    raise real_errors.TaskRunError('task failed')\n"
        "except mirror_errors.TaskRunError as exc:\n"
        "    results['real_caught_as_mirror'] = str(exc)\n"
        "try:\n"
        "    raise mirror_errors.TaskRunError('task failed')\n"
        "except real_errors.TaskRunError as exc:\n"
        "    results['mirror_caught_as_real'] = str(exc)\n"
        "print(json.dumps(results))\n"
    )
    assert run_py_json(code) == {
        "real_caught_as_mirror": "task failed",
        "mirror_caught_as_real": "task failed",
    }


def test_retry_reached_via_mirror_reports_real_module() -> None:
    """Retry obtained through render_sdk IS the real class, so its __module__
    is the real module path — pickling, repr, and doc tooling all see the
    canonical name."""
    code = (
        "from render_sdk import Retry\n"
        "from render_sdk.workflows import Retry as WorkflowsRetry\n"
        "import json\n"
        "print(json.dumps({\n"
        "    'top': Retry.__module__,\n"
        "    'workflows': WorkflowsRetry.__module__,\n"
        "    'same': Retry is WorkflowsRetry,\n"
        "}))\n"
    )
    payload = run_py_json(code)
    assert payload["top"] == "render.workflows.task"
    assert payload["workflows"] == "render.workflows.task"
    assert payload["same"] is True
