"""Render Python SDK

This package provides:
1. Workflow SDK (render_sdk.workflows) for defining and running tasks
2. REST API Client (render_sdk.client) for interacting with Render's API
"""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = "0.1.0"
