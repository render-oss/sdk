"""Tests for the experimental object storage client."""

from datetime import datetime
from io import BytesIO
from types import SimpleNamespace

import httpx
import pytest

from render_sdk.experimental.object.client import ObjectClient
from render_sdk.experimental.object.types import UploadResponse


@pytest.mark.asyncio
async def test_put_streams_binary_file_objects(mocker):
    content = b"hello world - streamed from file-like object"
    captured: dict[str, bytes | str | None] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["content_length"] = request.headers.get("content-length")
        captured["body"] = await request.aread()
        return httpx.Response(200, headers={"ETag": '"test-etag"'})

    transport = httpx.MockTransport(handler)
    mock_http_client = httpx.AsyncClient(transport=transport)
    mocker.patch(
        "render_sdk.experimental.object.client.httpx.AsyncClient",
        return_value=mock_http_client,
    )

    object_client = ObjectClient(SimpleNamespace())
    mocker.patch.object(
        object_client.api,
        "get_upload_url",
        new=mocker.AsyncMock(
            return_value=UploadResponse(
                url="https://storage.example/upload",
                expires_at=datetime.now(),
                max_size_bytes=len(content),
            )
        ),
    )

    result = await object_client.put(
        owner_id="tea-test",
        region="oregon",
        key="stream-test.txt",
        data=BytesIO(content),
        size=len(content),
    )

    assert result.etag == '"test-etag"'
    assert captured["content_length"] == str(len(content))
    assert captured["body"] == content


@pytest.mark.asyncio
async def test_put_accepts_async_byte_iterators(mocker):
    content_chunks = [b"hello ", b"world", b" from async iterator"]
    content = b"".join(content_chunks)
    captured: dict[str, bytes | str | None] = {}

    async def data_stream():
        for chunk in content_chunks:
            yield chunk

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["content_length"] = request.headers.get("content-length")
        captured["body"] = await request.aread()
        return httpx.Response(200, headers={"ETag": '"test-etag-async"'})

    transport = httpx.MockTransport(handler)
    mock_http_client = httpx.AsyncClient(transport=transport)
    mocker.patch(
        "render_sdk.experimental.object.client.httpx.AsyncClient",
        return_value=mock_http_client,
    )

    object_client = ObjectClient(SimpleNamespace())
    mocker.patch.object(
        object_client.api,
        "get_upload_url",
        new=mocker.AsyncMock(
            return_value=UploadResponse(
                url="https://storage.example/upload",
                expires_at=datetime.now(),
                max_size_bytes=len(content),
            )
        ),
    )

    result = await object_client.put(
        owner_id="tea-test",
        region="oregon",
        key="stream-test-async-iter.txt",
        data=data_stream(),
        size=len(content),
    )

    assert result.etag == '"test-etag-async"'
    assert captured["content_length"] == str(len(content))
    assert captured["body"] == content
