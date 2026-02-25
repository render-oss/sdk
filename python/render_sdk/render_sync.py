"""Synchronous unified REST API client for Render services."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render_sdk.client import Client
    from render_sdk.client.workflows_sync import SyncWorkflowsService
    from render_sdk.experimental.experimental_sync import SyncExperimentalService


class RenderSync:
    """
    Synchronous unified REST API client for all Render services.

    This is the primary entry point for interacting with Render's APIs
    from synchronous code (Flask, Django, scripts, etc.).

    Example:
        render = RenderSync()  # Uses RENDER_API_KEY from environment

        # Run a task and wait for the result
        result = render.workflows.run_task("my-workflow/my_task", [42])

        # Or start a task for fire-and-forget / deferred polling
        task_run = render.workflows.start_task("my-workflow/my_task", [5])
        # Later: result = render.workflows.get_task_run(task_run.id)
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
        Initialize the synchronous Render SDK.

        Args:
            token: API token. If not provided, uses RENDER_API_KEY env var.
            base_url: API base URL (rarely needed).
            owner_id: Default owner ID for object storage. If not provided,
                     uses RENDER_WORKSPACE_ID env var.
            region: Default region for object storage. If not provided,
                   uses RENDER_REGION env var.
        """
        from render_sdk.client import Client
        from render_sdk.client.workflows_sync import SyncWorkflowsService
        from render_sdk.experimental.experimental_sync import SyncExperimentalService

        self._client = Client(
            token=token, base_url=base_url, owner_id=owner_id, region=region
        )
        self._workflows = SyncWorkflowsService(self._client)
        self._experimental = SyncExperimentalService(self._client)

    @property
    def client(self) -> Client:
        """
        Access to the underlying API client.

        Use this for fine-grained control or advanced use cases.
        """
        return self._client

    @property
    def workflows(self) -> SyncWorkflowsService:
        """REST API for workflow operations (run tasks, get status)."""
        return self._workflows

    @property
    def experimental(self) -> SyncExperimentalService:
        """Experimental APIs including object storage."""
        return self._experimental
