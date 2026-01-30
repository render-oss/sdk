"""Layer 2: Typed Object API Client

Provides idiomatic Python wrapper around the raw OpenAPI client.
Handles presigned URL flow but still exposes the two-step nature
(get URL, then upload/download). Useful for advanced use cases
requiring fine-grained control.
"""

import builtins
from typing import TYPE_CHECKING

from render_sdk.client.errors import RenderError
from render_sdk.client.util import handle_http_errors
from render_sdk.experimental.object.types import (
    DownloadResponse,
    ListObjectsResponse,
    ObjectMetadata,
    UploadResponse,
)
from render_sdk.public_api.api.blob_storage import (
    delete_blob,
    get_blob,
    list_blobs,
    put_blob,
)
from render_sdk.public_api.models.blob_with_cursor import BlobWithCursor
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.models.get_blob_output import GetBlobOutput
from render_sdk.public_api.models.put_blob_input import (
    PutBlobInput as PutBlobInputModel,
)
from render_sdk.public_api.models.put_blob_output import PutBlobOutput
from render_sdk.public_api.models.region import Region
from render_sdk.public_api.types import UNSET, Response

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient


class ObjectApi:
    """Layer 2: Typed Object API Client

    Provides idiomatic Python wrapper around the raw OpenAPI client.
    Handles presigned URL flow but still exposes the two-step nature.
    """

    def __init__(self, client: "AuthenticatedClient"):
        self.client = client

    async def get_upload_url(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
        size_bytes: int,
    ) -> UploadResponse:
        """Get a presigned URL for uploading an object.

        Args:
            owner_id: Owner ID (workspace team ID)
            region: Storage region
            key: Object key (path)
            size_bytes: Size of the object in bytes

        Returns:
            UploadResponse: Upload URL with expiration and size limit

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out
        """
        response = await self._get_upload_url_api_call(
            owner_id, region, key, size_bytes
        )

        if not isinstance(response.parsed, PutBlobOutput):
            raise RenderError("Failed to get upload URL: unexpected response type")

        return UploadResponse(
            url=response.parsed.url,
            expires_at=response.parsed.expires_at,
            max_size_bytes=response.parsed.max_size_bytes,
        )

    @handle_http_errors("get upload URL")
    async def _get_upload_url_api_call(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
        size_bytes: int,
    ) -> Response[Error | PutBlobOutput]:
        """Internal method to make the get upload URL API call."""
        # Convert region to Region enum if it's a string
        if isinstance(region, str):
            region = Region(region)

        body = PutBlobInputModel(size_bytes=size_bytes)

        return await put_blob.asyncio_detailed(
            owner_id=owner_id,
            region=region,
            key=key,
            client=self.client,
            body=body,
        )

    async def get_download_url(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
    ) -> DownloadResponse:
        """Get a presigned URL for downloading an object.

        Args:
            owner_id: Owner ID (workspace team ID)
            region: Storage region
            key: Object key (path)

        Returns:
            DownloadResponse: Download URL with expiration

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out
        """
        response = await self._get_download_url_api_call(owner_id, region, key)

        if not isinstance(response.parsed, GetBlobOutput):
            raise RenderError("Failed to get download URL: unexpected response type")

        return DownloadResponse(
            url=response.parsed.url,
            expires_at=response.parsed.expires_at,
        )

    @handle_http_errors("get download URL")
    async def _get_download_url_api_call(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
    ) -> Response[Error | GetBlobOutput]:
        """Internal method to make the get download URL API call."""
        # Convert region to Region enum if it's a string
        if isinstance(region, str):
            region = Region(region)

        return await get_blob.asyncio_detailed(
            owner_id=owner_id,
            region=region,
            key=key,
            client=self.client,
        )

    async def delete(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
    ) -> None:
        """Delete an object.

        Args:
            owner_id: Owner ID (workspace team ID)
            region: Storage region
            key: Object key (path)

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out
        """
        await self._delete_api_call(owner_id, region, key)

    @handle_http_errors("delete object")
    async def _delete_api_call(
        self,
        owner_id: str,
        region: Region | str,
        key: str,
    ) -> Response[Error | None]:
        """Internal method to make the delete object API call."""
        # Convert region to Region enum if it's a string
        if isinstance(region, str):
            region = Region(region)

        return await delete_blob.asyncio_detailed(
            owner_id=owner_id,
            region=region,
            key=key,
            client=self.client,
        )

    async def list_objects(
        self,
        owner_id: str,
        region: Region | str,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> ListObjectsResponse:
        """List objects in storage.

        Args:
            owner_id: Owner ID (workspace team ID)
            region: Storage region
            cursor: Pagination cursor from previous response
            limit: Maximum number of objects to return (default 20)

        Returns:
            ListObjectsResponse: List of object metadata with optional next cursor

        Raises:
            ClientError: For 4xx client errors
            ServerError: For 5xx server errors
            TimeoutError: If the request times out
        """
        response = await self._list_objects_api_call(owner_id, region, cursor, limit)

        if not isinstance(response.parsed, builtins.list):
            raise RenderError("Failed to list objects: unexpected response type")

        objects = [
            ObjectMetadata(
                key=item.blob.key,
                size=item.blob.size_bytes,
                last_modified=item.blob.last_modified,
                content_type=item.blob.content_type,
            )
            for item in response.parsed
        ]

        # The cursor for the next page is the cursor of the last item
        next_cursor = response.parsed[-1].cursor if response.parsed else None

        return ListObjectsResponse(objects=objects, next_cursor=next_cursor)

    @handle_http_errors("list objects")
    async def _list_objects_api_call(
        self,
        owner_id: str,
        region: Region | str,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | builtins.list[BlobWithCursor]]:
        """Internal method to make the list objects API call."""
        # Convert region to Region enum if it's a string
        if isinstance(region, str):
            region = Region(region)

        return await list_blobs.asyncio_detailed(
            owner_id=owner_id,
            region=region,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
            client=self.client,
        )
