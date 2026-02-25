"""Synchronous Experimental Service.

This module provides the sync versions of ExperimentalService and StorageService.
"""

from typing import TYPE_CHECKING

from render_sdk.experimental.object.client_sync import SyncObjectClient

if TYPE_CHECKING:
    from render_sdk.client.client import Client


class SyncStorageService:
    """Synchronous Storage Service.

    Provides access to experimental storage features using synchronous HTTP calls.

    Example:
        ```python
        client.experimental.storage.objects.put(
            owner_id="tea-xxxxx",
            region="oregon",
            key="file.png",
            data=b"content"
        )
        ```
    """

    def __init__(self, client: "Client"):
        """Initialize the storage service.

        Args:
            client: The Render client instance
        """
        self.objects = SyncObjectClient(
            client.internal,
            default_owner_id=client.owner_id,
            default_region=client.region,
        )


class SyncExperimentalService:
    """Synchronous Experimental Service.

    Provides access to experimental Render SDK features using synchronous HTTP calls.

    Features in this namespace may change or be removed without a migration plan.
    When a feature stabilizes, it will be promoted to the main SDK namespace.

    Example:
        ```python
        from render_sdk import RenderSync

        render = RenderSync()

        render.experimental.storage.objects.put(
            owner_id="tea-xxxxx",
            region="oregon",
            key="file.png",
            data=b"content"
        )
        ```
    """

    def __init__(self, client: "Client"):
        """Initialize the experimental service.

        Args:
            client: The Render client instance
        """
        self.storage = SyncStorageService(client)
