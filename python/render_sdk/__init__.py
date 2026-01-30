"""Render Python SDK

This package provides:
1. REST API Client (render_sdk.Render) for interacting with Render's API
2. Workflow SDK (render_sdk.workflows) for defining and running tasks
"""

__version__ = "0.1.3"

# Primary user-facing APIs
from render_sdk.render import Render
from render_sdk.workflows import Retry, start, task

__all__ = [
    "__version__",
    # REST API client
    "Render",
    # Task definition (existing API)
    "Retry",
    "start",
    "task",
]

# Direct client access available via:
#   render.client  # Access from existing Render instance
#   from render_sdk.client import Client  # Or import directly
#
# Raw API access available via:
#   from render_sdk.public_api import AuthenticatedClient
