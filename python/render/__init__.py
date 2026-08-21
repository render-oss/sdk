"""Render Python SDK

Task definition (for workers):

    from render import TaskContext, Workflows

    app = Workflows()

    @app.task
    def my_task(ctx: TaskContext, x: int) -> int:
        return x * 2

Synchronous REST API access (default):

    from render import Render

    render = Render()

    result = render.workflows.run_task("my-workflow/my_task", [5])

    task_run = render.workflows.start_task("my-workflow/my_task", [5])
    # Later: result = render.workflows.get_task_run(task_run.id)

Async REST API access:

    from render import RenderAsync

    render = RenderAsync()

    result = await render.workflows.run_task("my-workflow/my_task", [5])

    task_run = await render.workflows.start_task("my-workflow/my_task", [5])
    result = await task_run
"""

__version__ = "1.0.1"

# Render/RenderAsync are lazy-loaded so the workflow worker path stays fast.
from typing import TYPE_CHECKING

from render.workflows import (
    Options,
    Retry,
    TaskContext,
    Workflows,
    start,
    task,
)

if TYPE_CHECKING:
    from render.render import Render
    from render.render_async import RenderAsync

__all__ = [
    "__version__",
    # Primary APIs
    "Render",  # Sync REST API client (default)
    "RenderAsync",  # Async REST API client
    "Workflows",  # Task definition
    "TaskContext",  # First parameter of every task
    # Configuration
    "Options",
    "Retry",
    # Deprecated: use Workflows.task and Workflows.start() instead
    "start",
    "task",
]


_LAZY_ATTRS = {
    "Render": ("render.render", "Render"),
    "RenderAsync": ("render.render_async", "RenderAsync"),
}


def __getattr__(name: str):
    target = _LAZY_ATTRS.get(name)
    if target is None:
        raise AttributeError(f"module 'render' has no attribute {name!r}")

    import importlib

    module_name, attr_name = target
    value = getattr(importlib.import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_ATTRS) | set(__all__))


# Direct client access available via:
#   render.client  # Access from existing Render instance
#   from render.client import Client  # Or import directly
#
# Raw API access available via:
#   from render.public_api import AuthenticatedClient
