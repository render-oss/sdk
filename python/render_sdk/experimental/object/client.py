"""High-level object storage client.

Provides simple put/get/delete operations for object storage.
"""

from typing import TYPE_CHECKING, BinaryIO

import httpx

from render_sdk.client.errors import RenderError
from render_sdk.client.util import handle_http_error
from render_sdk.experimental.object.api import ObjectApi
from render_sdk.experimental.object.types import (
    ListObjectsResponse,
    ObjectData,
    OwnerID,
    PutObjectResult,
)
from render_sdk.public_api.models.region import Region

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient


class ObjectClient:
    """ObjectClient is a high level client for interacting with object storage.

    It exposes methods to put/get/delete objects.
    """

    def __init__(self, client: "AuthenticatedClient"):
        self.client = client
        self.api = ObjectApi(client)

    async def put(
        self,
        *,
        owner_id: OwnerID,
        region: Region | str,
        key: str,
        data: bytes | BinaryIO,
        size: int | None = None,
        content_type: str | None = None,
    ) -> PutObjectResult:
        """Upload an object to storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the object
            data: Binary data as bytes or a file-like stream
            size: Size in bytes (optional for bytes, required for streams)
            content_type: MIME type of the content (optional)

        Returns:
            PutObjectResult: Result with optional ETag

        Raises:
            RenderError: If size validation fails or upload fails
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            # Upload bytes
            await object_client.put(
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
                await object_client.put(
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

            handle_http_error(response, "upload object")

            return PutObjectResult(
                etag=response.headers.get("ETag"),
            )

    async def get(
        self, *, owner_id: OwnerID, region: Region | str, key: str
    ) -> ObjectData:
        """Download an object from storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the object

        Returns:
            ObjectData: Object data with content

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            obj = await object_client.get(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png"
            )

            print(obj.size)           # Size in bytes
            print(obj.content_type)   # MIME type if available
            # obj.data is bytes
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

            handle_http_error(response, "download object")

            data = response.content

            return ObjectData(
                data=data,
                size=len(data),
                content_type=response.headers.get("Content-Type"),
            )

    async def delete(
        self, *, owner_id: OwnerID, region: Region | str, key: str
    ) -> None:
        """Delete an object from storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the object

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            await object_client.delete(
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

    async def list(
        self,
        *,
        owner_id: OwnerID,
        region: Region | str,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> ListObjectsResponse:
        """List objects in storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            cursor: Pagination cursor from previous response
            limit: Maximum number of objects to return (default 20)

        Returns:
            ListObjectsResponse: List of object metadata with optional next cursor

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out

        Example:
            ```python
            # List first page
            response = await object_client.list(
                owner_id="tea-xxxxx",
                region="oregon"
            )

            for obj in response.objects:
                print(f"{obj.key}: {obj.size} bytes")

            # Get next page if available
            if response.next_cursor:
                next_page = await object_client.list(
                    owner_id="tea-xxxxx",
                    region="oregon",
                    cursor=response.next_cursor
                )
            ```
        """
        # Convert region to Region enum if it's a string
        region_enum = Region(region) if isinstance(region, str) else region

        return await self.api.list_objects(
            owner_id=owner_id,
            region=region_enum,
            cursor=cursor,
            limit=limit,
        )

    def scoped(
        self, *, owner_id: OwnerID, region: Region | str
    ) -> "ScopedObjectClient":
        """Create a scoped object client for a specific owner and region.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region

        Returns:
            ScopedObjectClient: Scoped object client that doesn't require
                owner_id/region on each call

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )

            # Subsequent calls only need the key
            await scoped.put(key="file.png", data=buffer)
            await scoped.get(key="file.png")
            await scoped.delete(key="file.png")
            ```
        """
        return ScopedObjectClient(self, owner_id, region)

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


class ScopedObjectClient:
    """Scoped Object Client

    Pre-configured client for a specific owner and region.
    Eliminates the need to specify owner_id and region on every operation.

    Example:
        ```python
        scoped = object_client.scoped(
            owner_id="tea-xxxxx",
            region="oregon"
        )

        # Methods have the same signature as ObjectClient but without owner_id/region
        await scoped.put(key="file.png", data=b"content")
        obj = await scoped.get(key="file.png")
        await scoped.delete(key="file.png")
        ```
    """

    def __init__(
        self, object_client: ObjectClient, owner_id: OwnerID, region: Region | str
    ):
        self._object_client = object_client
        self._owner_id = owner_id
        self._region = region

    async def put(
        self,
        *,
        key: str,
        data: bytes | BinaryIO,
        size: int | None = None,
        content_type: str | None = None,
    ) -> PutObjectResult:
        """Upload an object to storage using scoped owner and region.

        Args:
            key: Object key (path) for the object
            data: Binary data as bytes or a file-like stream
            size: Size in bytes (optional for bytes, required for streams)
            content_type: MIME type of the content (optional)

        Returns:
            PutObjectResult: Result with optional ETag

        Example:
            ```python
            scoped = object_client.scoped(
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
        return await self._object_client.put(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
            data=data,
            size=size,
            content_type=content_type,
        )

    async def get(self, *, key: str) -> ObjectData:
        """Download an object from storage using scoped owner and region.

        Args:
            key: Object key (path) for the object

        Returns:
            ObjectData: Object data with content

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            obj = await scoped.get(key="file.png")
            ```
        """
        return await self._object_client.get(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )

    async def delete(self, *, key: str) -> None:
        """Delete an object from storage using scoped owner and region.

        Args:
            key: Object key (path) for the object

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            await scoped.delete(key="file.png")
            ```
        """
        await self._object_client.delete(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> ListObjectsResponse:
        """List objects in storage using scoped owner and region.

        Args:
            cursor: Pagination cursor from previous response
            limit: Maximum number of objects to return (default 20)

        Returns:
            ListObjectsResponse: List of object metadata with optional next cursor

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            response = await scoped.list()
            for obj in response.objects:
                print(f"{obj.key}: {obj.size} bytes")
            ```
        """
        return await self._object_client.list(
            owner_id=self._owner_id,
            region=self._region,
            cursor=cursor,
            limit=limit,
        )
