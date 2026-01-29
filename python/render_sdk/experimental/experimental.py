"""Experimental Service

This module provides the ExperimentalService class that exposes experimental features
from the Render SDK.
"""

from typing import TYPE_CHECKING

from render_sdk.experimental.object.client import ObjectClient

if TYPE_CHECKING:
    from render_sdk.client.client import Client


class StorageService:
    """Storage Service

    Provides access to experimental storage features.

    Example:
        ```python
        # Access object storage
        await client.experimental.storage.objects.put(
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
        self.objects = ObjectClient(client.internal)


class ExperimentalService:
    """Experimental Service

    Provides access to experimental Render SDK features.

    Features in this namespace may change or be removed without a migration plan.
    When a feature stabilizes, it will be promoted to the main SDK namespace.

    Example:
        ```python
        from render_sdk.client import Client

        client = Client()

        # Access experimental object storage
        await client.experimental.storage.objects.put(
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
        self.storage = StorageService(client)
