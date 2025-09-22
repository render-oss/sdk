"""Render API Client

This module provides the main Client class for interacting with Render's REST API.
It mirrors the functionality of the Go client.
"""

import os

from render.public_api.client import AuthenticatedClient
from render.client.sse import SSEClient
from render.client.workflows import WorkflowsService


class Client:
    """Render API client

    This class provides access to Render's REST API with automatic authentication
    and service-specific clients.

    Attributes:
        internal: The internal generated API client
        token: The authentication token
        base_url: The API base URL
        workflows: Service client for workflow operations
    """

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.render.com",
    ):
        """Initialize a new Render API client.

        Args:
            token: API authentication token. If not provided, will look for
                  RENDER_API_KEY environment variable.
            *options: Client configuration options
        """
        # Set default values
        self.token = token or os.getenv("RENDER_API_KEY", "")
        self.base_url = base_url

        # Ensure base URL has proper format
        if not self.base_url.startswith(("http://", "https://")):
            self.base_url = f"https://{self.base_url}"

        # Remove trailing slash and add /v1
        api_base = f"{self.base_url.rstrip('/')}/v1"

        # Create the internal authenticated client
        self.internal = AuthenticatedClient(
            base_url=api_base,
            token=self.token,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        # Initialize service clients
        self.workflows = WorkflowsService(self)
        self.sse = SSEClient(self)
