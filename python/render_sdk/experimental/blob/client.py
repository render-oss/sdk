"""High-level blob storage client.

Provides simple put/get/delete operations for blob storage.
"""

from typing import TYPE_CHECKING, BinaryIO

import httpx

from render_sdk.client.errors import RenderError
from render_sdk.client.util import handle_http_error
from render_sdk.experimental.blob.api import BlobApi
from render_sdk.experimental.blob.types import BlobData, OwnerID, PutBlobResult
from render_sdk.public_api.models.region import Region

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient


class BlobClient:
    """BlobClient is a high level client for interacting with blob storage.

    It exposes methods to put/get/delete blobs.
    """

    def __init__(self, client: "AuthenticatedClient"):
        self.client = client
        self.api = BlobApi(client)

    async def put(
        self,
        *,
        owner_id: OwnerID,
        region: Region | str,
        key: str,
        data: bytes | BinaryIO,
        size: int | None = None,
        content_type: str | None = None,
    ) -> PutBlobResult:
        """Upload a blob to storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the blob
            data: Binary data as bytes or a file-like stream
            size: Size in bytes (optional for bytes, required for streams)
            content_type: MIME type of the content (optional)

        Returns:
            PutBlobResult: Result with optional ETag

        Raises:
            RenderError: If size validation fails or upload fails
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            # Upload bytes
            await blob_client.put(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png",
                data=b"binary content",
                content_type="image/png"
            )

            # Upload from file stream
            with open("/path/to/file.zip", "rb") as f:
                import os
                size = os.path.getsize("/path/to/file.zip")
                await blob_client.put(
                    owner_id="tea-xxxxx",
                    region="oregon",
                    key="file.zip",
                    data=f,
                    size=size
                )
            ```
        """
        # Resolve and validate size
        resolved_size = self._resolve_size(data, size)

        # Convert region to Region enum if it's a string
        region_enum = Region(region) if isinstance(region, str) else region

        # Step 1: Get presigned upload URL from Render API
        presigned = await self.api.get_upload_url(
            owner_id=owner_id,
            region=region_enum,
            key=key,
            size_bytes=resolved_size,
        )

        # Step 2: Upload to storage via presigned URL
        headers = {
            "Content-Length": str(resolved_size),
        }

        if content_type:
            headers["Content-Type"] = content_type

        async with httpx.AsyncClient() as http_client:
            response = await http_client.put(
                presigned.url,
                headers=headers,
                content=data,
            )

            handle_http_error(response, "upload blob")

            return PutBlobResult(
                etag=response.headers.get("ETag"),
            )

    async def get(
        self, *, owner_id: OwnerID, region: Region | str, key: str
    ) -> BlobData:
        """Download a blob from storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the blob

        Returns:
            BlobData: Blob data with content

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            blob = await blob_client.get(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png"
            )

            print(blob.size)           # Size in bytes
            print(blob.content_type)   # MIME type if available
            # blob.data is bytes
            ```
        """
        # Convert region to Region enum if it's a string
        region_enum = Region(region) if isinstance(region, str) else region

        # Step 1: Get presigned download URL from Render API
        presigned = await self.api.get_download_url(
            owner_id=owner_id,
            region=region_enum,
            key=key,
        )

        # Step 2: Download from storage via presigned URL
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(presigned.url)

            handle_http_error(response, "download blob")

            data = response.content

            return BlobData(
                data=data,
                size=len(data),
                content_type=response.headers.get("Content-Type"),
            )

    async def delete(
        self, *, owner_id: OwnerID, region: Region | str, key: str
    ) -> None:
        """Delete a blob from storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the blob

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            await blob_client.delete(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png"
            )
            ```
        """
        # Convert region to Region enum if it's a string
        region_enum = Region(region) if isinstance(region, str) else region

        # DELETE goes directly to Render API (no presigned URL)
        await self.api.delete(
            owner_id=owner_id,
            region=region_enum,
            key=key,
        )

    def scoped(self, *, owner_id: OwnerID, region: Region | str) -> "ScopedBlobClient":
        """Create a scoped blob client for a specific owner and region.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region

        Returns:
            ScopedBlobClient: Scoped blob client that doesn't require
                owner_id/region on each call

        Example:
            ```python
            scoped = blob_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )

            # Subsequent calls only need the key
            await scoped.put(key="file.png", data=buffer)
            await scoped.get(key="file.png")
            await scoped.delete(key="file.png")
            ```
        """
        return ScopedBlobClient(self, owner_id, region)

    def _resolve_size(self, data: bytes | BinaryIO, size: int | None) -> int:
        """Resolve and validate the size for a put operation.

        - For bytes: auto-calculate size, validate if provided
        - For streams: require explicit size

        Args:
            data: Binary data (bytes or stream)
            size: Optional size in bytes

        Returns:
            int: The size in bytes

        Raises:
            RenderError: If size validation fails
        """
        if isinstance(data, bytes):
            # Auto-calculate for bytes
            actual_size = len(data)

            if size is not None and size != actual_size:
                raise RenderError(
                    f"Size mismatch: provided size {size} does not match "
                    f"actual size {actual_size}"
                )

            return actual_size
        else:
            # Require explicit size for streams
            if size is None:
                raise RenderError("size is required for stream uploads")
            if size <= 0:
                raise RenderError("size must be a positive integer")

            return size


class ScopedBlobClient:
    """Scoped Blob Client

    Pre-configured client for a specific owner and region.
    Eliminates the need to specify owner_id and region on every operation.

    Example:
        ```python
        scoped = blob_client.scoped(
            owner_id="tea-xxxxx",
            region="oregon"
        )

        # Methods have the same signature as BlobClient but without owner_id/region
        await scoped.put(key="file.png", data=b"content")
        blob = await scoped.get(key="file.png")
        await scoped.delete(key="file.png")
        ```
    """

    def __init__(
        self, blob_client: BlobClient, owner_id: OwnerID, region: Region | str
    ):
        self._blob_client = blob_client
        self._owner_id = owner_id
        self._region = region

    async def put(
        self,
        *,
        key: str,
        data: bytes | BinaryIO,
        size: int | None = None,
        content_type: str | None = None,
    ) -> PutBlobResult:
        """Upload a blob to storage using scoped owner and region.

        Args:
            key: Object key (path) for the blob
            data: Binary data as bytes or a file-like stream
            size: Size in bytes (optional for bytes, required for streams)
            content_type: MIME type of the content (optional)

        Returns:
            PutBlobResult: Result with optional ETag

        Example:
            ```python
            scoped = blob_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            await scoped.put(
                key="file.png",
                data=b"content",
                content_type="image/png"
            )
            ```
        """
        return await self._blob_client.put(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
            data=data,
            size=size,
            content_type=content_type,
        )

    async def get(self, *, key: str) -> BlobData:
        """Download a blob from storage using scoped owner and region.

        Args:
            key: Object key (path) for the blob

        Returns:
            BlobData: Blob data with content

        Example:
            ```python
            scoped = blob_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            blob = await scoped.get(key="file.png")
            ```
        """
        return await self._blob_client.get(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )

    async def delete(self, *, key: str) -> None:
        """Delete a blob from storage using scoped owner and region.

        Args:
            key: Object key (path) for the blob

        Example:
            ```python
            scoped = blob_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            await scoped.delete(key="file.png")
            ```
        """
        await self._blob_client.delete(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )
