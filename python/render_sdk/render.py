"""Unified REST API client for Render services."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render_sdk.client import Client
    from render_sdk.client.workflows import WorkflowsService
    from render_sdk.experimental import ExperimentalService


class Render:
    """
    Unified REST API client for all Render services.

    This is the primary entry point for interacting with Render's APIs.

    Example:
        render = Render()  # Uses RENDER_API_KEY from environment

        # Run a task
        result = await render.workflows.run_task("my-workflow/my-task", [42])

        # Direct client access for advanced use cases
        render.client.workflows.run_task(...)
    """

    _client: Client

    def __init__(
        self,
        *,
        token: str | None = None,
        base_url: str = "https://api.render.com",
        owner_id: str | None = None,
        region: str | None = None,
    ) -> None:
        """
        Initialize the Render SDK.

        Args:
            token: API token. If not provided, uses RENDER_API_KEY env var.
            base_url: API base URL (rarely needed).
            owner_id: Default owner ID for object storage. If not provided,
                     uses RENDER_WORKSPACE_ID env var.
            region: Default region for object storage. If not provided,
                   uses RENDER_REGION env var.
        """
        from render_sdk.client import Client

        self._client = Client(
            token=token, base_url=base_url, owner_id=owner_id, region=region
        )

    @property
    def client(self) -> Client:
        """
        Access to the underlying API client.

        Use this for fine-grained control or advanced use cases.

        Example:
            render = Render()

            # Access client directly
            render.client.workflows.run_task(...)
        """
        return self._client

    @property
    def workflows(self) -> WorkflowsService:
        """REST API for workflow operations (run tasks, get status)."""
        return self._client.workflows

    @property
    def experimental(self) -> ExperimentalService:
        """Experimental APIs including object storage."""
        return self._client.experimental
