"""Render API Client

This module provides the main Client class for interacting with Render's REST API.
"""

import os

from render_sdk.client.sse import SSEClient
from render_sdk.client.workflows import WorkflowsService
from render_sdk.experimental.experimental import ExperimentalService
from render_sdk.public_api.client import AuthenticatedClient
from render_sdk.version import get_user_agent


class Client:
    """Render API client

    This class provides access to Render's REST API with automatic authentication
    and service-specific clients.

    Attributes:
        internal: The internal generated API client
        token: The authentication token
        base_url: The API base URL
        workflows: Service client for workflow operations
        experimental: Service client for experimental features
    """

    token: str

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.render.com",
        owner_id: str | None = None,
        region: str | None = None,
    ):
        """Initialize a new Render API client.

        Args:
            token: API authentication token. If not provided, will look for
                  RENDER_API_KEY environment variable.
            owner_id: Default owner ID for object storage. If not provided,
                     will look for RENDER_WORKSPACE_ID environment variable.
            region: Default region for object storage. If not provided,
                   will look for RENDER_REGION environment variable.
            *options: Client configuration options
        """
        # Set default values
        if token is None:
            self.token = os.getenv("RENDER_API_KEY", "")
            if self.token == "":
                raise ValueError(
                    "Either provide a token or set the RENDER_API_KEY "
                    + "environment variable"
                )
        else:
            self.token = token

        workspace_id = os.getenv("RENDER_WORKSPACE_ID", "") or None
        self.owner_id: str | None = owner_id or workspace_id
        self.region: str | None = region or os.getenv("RENDER_REGION", "") or None

        # Use the local dev URL when provided,
        # Otherwise if local dev is enabled, use the default local dev URL
        # Otherwise, use the base URL
        use_local_dev = os.getenv("RENDER_USE_LOCAL_DEV", "")
        local_dev_url = os.getenv("RENDER_LOCAL_DEV_URL", "")
        if local_dev_url:
            self.base_url = local_dev_url
        elif use_local_dev in ["1", "t", "T", "true", "TRUE", "True"]:
            self.base_url = "http://localhost:8120"
        else:
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
            headers={"User-Agent": get_user_agent()},
        )

        # Initialize service clients
        self.workflows = WorkflowsService(self)
        self.sse = SSEClient(self)
        self.experimental = ExperimentalService(self)
