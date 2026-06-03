"""Render Python SDK

Task definition (for workers):

    from render_sdk import Workflows, Retry

    app = Workflows()

    @app.task
    def my_task(x: int) -> int:
        return x * 2

Synchronous REST API access (default):

    from render_sdk import Render

    render = Render()

    result = render.workflows.run_task("my-workflow/my_task", [5])

    task_run = render.workflows.start_task("my-workflow/my_task", [5])
    # Later: result = render.workflows.get_task_run(task_run.id)

Async REST API access:

    from render_sdk import RenderAsync

    render = RenderAsync()

    result = await render.workflows.run_task("my-workflow/my_task", [5])

    task_run = await render.workflows.start_task("my-workflow/my_task", [5])
    result = await task_run
"""

__version__ = "0.7.0"

# Render/RenderAsync are lazy-loaded so the workflow worker path stays fast.
from typing import TYPE_CHECKING

from render_sdk.workflows import Options, Retry, Workflows, start, task

if TYPE_CHECKING:
    from render_sdk.render import Render
    from render_sdk.render_async import RenderAsync

__all__ = [
    "__version__",
    # Primary APIs
    "Render",  # Sync REST API client (default)
    "RenderAsync",  # Async REST API client
    "Workflows",  # Task definition
    # Configuration
    "Options",
    "Retry",
    # Deprecated: use Workflows.task and Workflows.start() instead
    "start",
    "task",
]


_LAZY_ATTRS = {
    "Render": ("render_sdk.render", "Render"),
    "RenderAsync": ("render_sdk.render_async", "RenderAsync"),
}


def __getattr__(name: str):
    target = _LAZY_ATTRS.get(name)
    if target is None:
        raise AttributeError(f"module 'render_sdk' has no attribute {name!r}")

    import importlib

    module_name, attr_name = target
    value = getattr(importlib.import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_ATTRS) | set(__all__))


# Direct client access available via:
#   render.client  # Access from existing Render instance
#   from render_sdk.client import Client  # Or import directly
#
# Raw API access available via:
#   from render_sdk.public_api import AuthenticatedClient
