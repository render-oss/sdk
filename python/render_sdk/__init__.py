"""Render Python SDK

Task definition (for workers):

    from render_sdk import Workflows, Retry

    app = Workflows()

    @app.task
    def my_task(x: int) -> int:
        return x * 2

Async REST API access:

    from render_sdk import Render

    render = Render()

    result = await render.workflows.run_task("my-workflow/my_task", [5])

    task_run = await render.workflows.start_task("my-workflow/my_task", [5])
    result = await task_run

Synchronous REST API access (Flask, Django, scripts):

    from render_sdk import RenderSync

    render = RenderSync()

    result = render.workflows.run_task("my-workflow/my_task", [5])

    task_run = render.workflows.start_task("my-workflow/my_task", [5])
    # Later: result = render.workflows.get_task_run(task_run.id)
"""

__version__ = "0.4.0"

# Primary user-facing APIs
from render_sdk.render import Render
from render_sdk.render_sync import RenderSync
from render_sdk.workflows import Options, Retry, Workflows, start, task

__all__ = [
    "__version__",
    # Primary APIs
    "Render",  # Async REST API client
    "RenderSync",  # Sync REST API client
    "Workflows",  # Task definition
    # Configuration
    "Options",
    "Retry",
    # Deprecated: use Workflows.task and Workflows.start() instead
    "start",
    "task",
]

# Direct client access available via:
#   render.client  # Access from existing Render instance
#   from render_sdk.client import Client  # Or import directly
#
# Raw API access available via:
#   from render_sdk.public_api import AuthenticatedClient
