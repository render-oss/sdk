# Auto-generated sync version. Do not edit — run scripts/unasync.py instead.

"""High-level object storage client.

Provides simple put/get/delete operations for object storage.
"""

from collections.abc import Iterator
from typing import TYPE_CHECKING, BinaryIO, cast

import httpx

from render_sdk.client.errors import ClientError, RenderError
from render_sdk.client.util_sync import (
    handle_httpx_exception,
    handle_storage_http_error,
)
from render_sdk.experimental.object.api_sync import SyncObjectApi
from render_sdk.experimental.object.types import (
    ListObjectsResponse,
    ObjectData,
    OwnerID,
    PutObjectResult,
)
from render_sdk.public_api.models.region import Region

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient


FILE_UPLOAD_CHUNK_SIZE_BYTES = 64 * 1024  # 64 KiB


def _file_to_iterable(file_obj: BinaryIO) -> Iterator[bytes]:
    """Convert a sync file object to a byte iterator."""
    while True:
        chunk = file_obj.read(FILE_UPLOAD_CHUNK_SIZE_BYTES)
        if not chunk:
            break
        yield chunk


class SyncObjectClient:
    """SyncObjectClient is a high level client for interacting with object storage.

    It exposes methods to put/get/delete objects.
    """

    def __init__(
        self,
        client: "AuthenticatedClient",
        default_owner_id: str | None = None,
        default_region: str | None = None,
    ):
        self.client = client
        self.api = SyncObjectApi(client)
        self._default_owner_id = default_owner_id
        self._default_region = default_region

    def _resolve_owner_id(self, owner_id: "OwnerID | None") -> OwnerID:
        resolved = owner_id or self._default_owner_id
        if not resolved:
            raise RenderError(
                "owner_id is required. Provide it as a parameter"
                " or set the RENDER_WORKSPACE_ID environment variable."
            )
        return resolved

    def _resolve_region(self, region: "Region | str | None") -> "Region | str":
        resolved = region or self._default_region
        if not resolved:
            raise RenderError(
                "region is required. Provide it as a parameter"
                " or set the RENDER_REGION environment variable."
            )
        return resolved

    def put(
        self,
        *,
        owner_id: OwnerID | None = None,
        region: Region | str | None = None,
        key: str,
        data: bytes | BinaryIO | Iterator[bytes],
        size: int | None = None,
        content_type: str | None = None,
    ) -> PutObjectResult:
        """Upload an object to storage.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region
            key: Object key (path) for the object
            data: Binary data as bytes, a file-like stream, or a byte iterator
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
            object_client.put(
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
                object_client.put(
                    owner_id="tea-xxxxx",
                    region="oregon",
                    key="file.zip",
                    data=f,
                    size=size
                )
            ```
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = self._resolve_region(region)

        # Resolve and validate size
        resolved_size = self._resolve_size(data, size)

        # Step 1: Get presigned upload URL from Render API
        presigned = self.api.get_upload_url(
            owner_id=resolved_owner_id,
            region=resolved_region,
            key=key,
            size_bytes=resolved_size,
        )

        # Validate size against server expectation
        if resolved_size != presigned.max_size_bytes:
            raise ClientError(
                f"File size {resolved_size} bytes does not match expected "
                f"size of {presigned.max_size_bytes} bytes"
            )

        # Step 2: Upload to storage via presigned URL
        headers = {
            "Content-Length": str(resolved_size),
        }

        if content_type:
            headers["Content-Type"] = content_type

        if isinstance(data, bytes):
            content: bytes | Iterator[bytes] = data
        elif hasattr(data, "read"):
            content = _file_to_iterable(cast(BinaryIO, data))
        else:
            content = data

        try:
            # Keep default connect/pool timeouts but disable read/write timeouts
            default_timeout_seconds = 5.0
            timeout = httpx.Timeout(default_timeout_seconds, read=None, write=None)
            with httpx.Client(timeout=timeout) as http_client:
                response = http_client.put(
                    presigned.url,
                    headers=headers,
                    content=content,
                )

                handle_storage_http_error(response, "upload object")

                return PutObjectResult(
                    etag=response.headers.get("ETag"),
                )
        except httpx.RequestError as e:
            handle_httpx_exception(e, "upload object")

    def get(
        self,
        *,
        owner_id: OwnerID | None = None,
        region: Region | str | None = None,
        key: str,
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
            obj = object_client.get(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png"
            )

            print(obj.size)           # Size in bytes
            print(obj.content_type)   # MIME type if available
            # obj.data is bytes
            ```
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = self._resolve_region(region)

        # Step 1: Get presigned download URL from Render API
        presigned = self.api.get_download_url(
            owner_id=resolved_owner_id,
            region=resolved_region,
            key=key,
        )

        # Step 2: Download from storage via presigned URL
        try:
            # Keep default connect/pool timeouts but disable read/write timeouts
            default_timeout_seconds = 5.0
            timeout = httpx.Timeout(default_timeout_seconds, read=None, write=None)
            with httpx.Client(timeout=timeout) as http_client:
                response = http_client.get(presigned.url)

                handle_storage_http_error(response, "download object")

                data = response.content

                return ObjectData(
                    data=data,
                    size=len(data),
                    content_type=response.headers.get("Content-Type"),
                )
        except httpx.RequestError as e:
            handle_httpx_exception(e, "download object")

    def delete(
        self,
        *,
        owner_id: OwnerID | None = None,
        region: Region | str | None = None,
        key: str,
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
            object_client.delete(
                owner_id="tea-xxxxx",
                region="oregon",
                key="path/to/file.png"
            )
            ```
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = self._resolve_region(region)

        # DELETE goes directly to Render API (no presigned URL)
        self.api.delete(
            owner_id=resolved_owner_id,
            region=resolved_region,
            key=key,
        )

    def list(
        self,
        *,
        owner_id: OwnerID | None = None,
        region: Region | str | None = None,
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
            response = object_client.list(
                owner_id="tea-xxxxx",
                region="oregon"
            )

            for obj in response.objects:
                print(f"{obj.key}: {obj.size} bytes")

            # Get next page if available
            if response.next_cursor:
                next_page = object_client.list(
                    owner_id="tea-xxxxx",
                    region="oregon",
                    cursor=response.next_cursor
                )
            ```
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = self._resolve_region(region)

        return self.api.list_objects(
            owner_id=resolved_owner_id,
            region=resolved_region,
            cursor=cursor,
            limit=limit,
        )

    def scoped(
        self, *, owner_id: OwnerID, region: Region | str
    ) -> "SyncScopedObjectClient":
        """Create a scoped object client for a specific owner and region.

        Args:
            owner_id: Owner ID (workspace team ID) in format tea-xxxxx
            region: Storage region

        Returns:
            SyncScopedObjectClient: Scoped object client that doesn't require
                owner_id/region on each call

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )

            # Subsequent calls only need the key
            scoped.put(key="file.png", data=buffer)
            scoped.get(key="file.png")
            scoped.delete(key="file.png")
            ```
        """
        return SyncScopedObjectClient(self, owner_id, region)

    def _resolve_size(
        self, data: bytes | BinaryIO | Iterator[bytes], size: int | None
    ) -> int:
        """Resolve and validate the size for a put operation.

        - For bytes: auto-calculate size, validate if provided
        - For streams: require explicit size

        Args:
            data: Binary data (bytes, stream, or byte iterator)
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
            if size < 0:
                raise RenderError("size must be a non-negative integer")

            return size


class SyncScopedObjectClient:
    """Scoped Object Client

    Pre-configured client for a specific owner and region.
    Eliminates the need to specify owner_id and region on every operation.

    Example:
        ```python
        scoped = object_client.scoped(
            owner_id="tea-xxxxx",
            region="oregon"
        )

        # Same methods as SyncObjectClient, but without owner_id/region
        scoped.put(key="file.png", data=b"content")
        obj = scoped.get(key="file.png")
        scoped.delete(key="file.png")
        ```
    """

    def __init__(
        self, object_client: SyncObjectClient, owner_id: OwnerID, region: Region | str
    ):
        self._object_client = object_client
        self._owner_id = owner_id
        self._region = region

    def put(
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
            scoped.put(
                key="file.png",
                data=b"content",
                content_type="image/png"
            )
            ```
        """
        return self._object_client.put(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
            data=data,
            size=size,
            content_type=content_type,
        )

    def get(self, *, key: str) -> ObjectData:
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
            obj = scoped.get(key="file.png")
            ```
        """
        return self._object_client.get(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )

    def delete(self, *, key: str) -> None:
        """Delete an object from storage using scoped owner and region.

        Args:
            key: Object key (path) for the object

        Example:
            ```python
            scoped = object_client.scoped(
                owner_id="tea-xxxxx",
                region="oregon"
            )
            scoped.delete(key="file.png")
            ```
        """
        self._object_client.delete(
            owner_id=self._owner_id,
            region=self._region,
            key=key,
        )

    def list(
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
            response = scoped.list()
            for obj in response.objects:
                print(f"{obj.key}: {obj.size} bytes")
            ```
        """
        return self._object_client.list(
            owner_id=self._owner_id,
            region=self._region,
            cursor=cursor,
            limit=limit,
        )
