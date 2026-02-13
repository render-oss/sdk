"""Render Python SDK

Task definition (for workers):

    from render_sdk import Workflows, Retry

    app = Workflows()

    @app.task
    def my_task(x: int) -> int:
        return x * 2

REST API access (for clients):

    from render_sdk import Render

    render = Render()
    result = await render.workflows.run_task("my-workflow/my_task", [5])
"""

__version__ = "0.3.0"

# Primary user-facing APIs
from render_sdk.render import Render
from render_sdk.workflows import Options, Retry, Workflows, start, task

__all__ = [
    "__version__",
    # Primary APIs
    "Render",  # REST API client
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
