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


# --- env var / default scope resolution tests ---


class TestDefaultScopeResolution:
    """Tests for owner_id/region default resolution via constructor and env vars."""

    def _make_client(
        self,
        default_owner_id: str | None = None,
        default_region: str | None = None,
    ) -> ObjectClient:
        return ObjectClient(
            SimpleNamespace(),  # type: ignore[arg-type]
            default_owner_id=default_owner_id,
            default_region=default_region,
        )

    def test_resolve_owner_id_from_param(self):
        client = self._make_client()
        assert client._resolve_owner_id("tea-explicit") == "tea-explicit"

    def test_resolve_owner_id_from_default(self):
        client = self._make_client(default_owner_id="tea-default")
        assert client._resolve_owner_id(None) == "tea-default"

    def test_resolve_owner_id_param_overrides_default(self):
        client = self._make_client(default_owner_id="tea-default")
        assert client._resolve_owner_id("tea-explicit") == "tea-explicit"

    def test_resolve_owner_id_missing_raises(self):
        client = self._make_client()
        with pytest.raises(Exception, match="owner_id is required"):
            client._resolve_owner_id(None)

    def test_resolve_region_from_param(self):
        client = self._make_client()
        assert client._resolve_region("oregon") == "oregon"

    def test_resolve_region_from_default(self):
        client = self._make_client(default_region="oregon")
        assert client._resolve_region(None) == "oregon"

    def test_resolve_region_param_overrides_default(self):
        client = self._make_client(default_region="oregon")
        assert client._resolve_region("frankfurt") == "frankfurt"

    def test_resolve_region_missing_raises(self):
        client = self._make_client()
        with pytest.raises(Exception, match="region is required"):
            client._resolve_region(None)

    def test_partial_defaults_owner_only(self):
        client = self._make_client(default_owner_id="tea-default")
        assert client._resolve_owner_id(None) == "tea-default"
        with pytest.raises(Exception, match="region is required"):
            client._resolve_region(None)

    def test_partial_defaults_region_only(self):
        client = self._make_client(default_region="oregon")
        with pytest.raises(Exception, match="owner_id is required"):
            client._resolve_owner_id(None)
        assert client._resolve_region(None) == "oregon"


class TestEnvVarResolution:
    """Tests for env var fallback via the Client constructor chain."""

    def test_env_vars_set(self, monkeypatch):
        monkeypatch.setenv("RENDER_WORKSPACE_ID", "tea-from-env")
        monkeypatch.setenv("RENDER_REGION", "frankfurt")

        from render_sdk.client.client import Client

        # Provide a token to avoid RENDER_API_KEY requirement
        c = Client(token="test-token")
        assert c.owner_id == "tea-from-env"
        assert c.region == "frankfurt"

    def test_empty_env_vars_treated_as_unset(self, monkeypatch):
        monkeypatch.setenv("RENDER_WORKSPACE_ID", "")
        monkeypatch.setenv("RENDER_REGION", "")

        from render_sdk.client.client import Client

        c = Client(token="test-token")
        assert c.owner_id is None
        assert c.region is None

    def test_constructor_params_override_env_vars(self, monkeypatch):
        monkeypatch.setenv("RENDER_WORKSPACE_ID", "tea-from-env")
        monkeypatch.setenv("RENDER_REGION", "frankfurt")

        from render_sdk.client.client import Client

        c = Client(
            token="test-token",
            owner_id="tea-from-param",
            region="oregon",
        )
        assert c.owner_id == "tea-from-param"
        assert c.region == "oregon"

    def test_env_vars_not_set(self, monkeypatch):
        monkeypatch.delenv("RENDER_WORKSPACE_ID", raising=False)
        monkeypatch.delenv("RENDER_REGION", raising=False)

        from render_sdk.client.client import Client

        c = Client(token="test-token")
        assert c.owner_id is None
        assert c.region is None

    def test_scoped_still_requires_explicit_params(self):
        """scoped() always requires explicit owner_id and region."""
        client = ObjectClient(
            SimpleNamespace(),
            default_owner_id="tea-default",
            default_region="oregon",
        )
        # scoped() signature requires both params — this is a type-level
        # guarantee, but verify it works at runtime too
        scoped = client.scoped(owner_id="tea-explicit", region="frankfurt")
        assert scoped._owner_id == "tea-explicit"
        assert scoped._region == "frankfurt"
