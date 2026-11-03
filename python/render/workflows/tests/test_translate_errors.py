"""Unit tests for the ``_translate_errors`` decorator in client.py."""

from __future__ import annotations

import http.client
import json

import pytest

from render.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
)
from render.client.errors import TimeoutError as SdkTimeoutError
from render.workflows._uds_http import HttpStatusError
from render.workflows.client import _translate_errors, _translate_errors_sync


def _wrap_raises(operation: str, exc: BaseException):
    """Build a ``_translate_errors``-decorated coroutine that raises ``exc``."""

    @_translate_errors(operation)
    async def fn():
        raise exc

    return fn


@pytest.mark.asyncio
async def test_builtin_timeout_becomes_sdk_timeout():
    fn = _wrap_raises("get input", TimeoutError("read timed out"))
    with pytest.raises(SdkTimeoutError) as exc_info:
        await fn()
    assert "get input timed out" in str(exc_info.value)
    assert "read timed out" in str(exc_info.value)


@pytest.mark.asyncio
async def test_connection_refused_becomes_server_error():
    fn = _wrap_raises("get input", ConnectionRefusedError("no such file"))
    with pytest.raises(ServerError) as exc_info:
        await fn()
    assert "get input failed to connect" in str(exc_info.value)


@pytest.mark.asyncio
async def test_file_not_found_becomes_server_error():
    fn = _wrap_raises("get input", FileNotFoundError("missing socket"))
    with pytest.raises(ServerError):
        await fn()


@pytest.mark.asyncio
async def test_generic_oserror_becomes_server_error():
    fn = _wrap_raises("get input", OSError("network blip"))
    with pytest.raises(ServerError) as exc_info:
        await fn()
    assert "get input network error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_http_exception_becomes_server_error():
    fn = _wrap_raises("get input", http.client.BadStatusLine("garbled\r\n"))
    with pytest.raises(ServerError) as exc_info:
        await fn()
    assert "get input got invalid HTTP response" in str(exc_info.value)


@pytest.mark.asyncio
async def test_4xx_status_becomes_client_error():
    fn = _wrap_raises("run subtask", HttpStatusError(400, b'{"message": "bad input"}'))
    with pytest.raises(ClientError) as exc_info:
        await fn()
    msg = str(exc_info.value)
    assert "run subtask failed with status 400" in msg
    assert "bad input" in msg


@pytest.mark.parametrize(
    "body, code",
    [
        (b'{"code": "run_cancelled", "message": "run was cancelled"}', "run_cancelled"),
        (b'{"code": 409}', None),
        (b"raw error string", None),
        (b"", None),
    ],
    ids=["code", "non-string-code", "non-json", "empty"],
)
@pytest.mark.asyncio
async def test_4xx_status_keeps_the_body_code(body, code):
    fn = _wrap_raises("record step", HttpStatusError(409, body))
    with pytest.raises(ClientError) as exc_info:
        await fn()
    assert exc_info.value.code == code


@pytest.mark.parametrize(
    "body, json_body",
    [
        (
            b'{"code": "workflow_payload_too_large", "limit": 1024, "value": 2048}',
            {"code": "workflow_payload_too_large", "limit": 1024, "value": 2048},
        ),
        (b"[1, 2]", None),
        (b"raw error string", None),
    ],
    ids=["object", "non-object", "non-json"],
)
@pytest.mark.asyncio
async def test_4xx_status_keeps_the_decoded_body(body, json_body):
    fn = _wrap_raises("record step", HttpStatusError(422, body))
    with pytest.raises(ClientError) as exc_info:
        await fn()
    assert exc_info.value.status_code == 422
    assert exc_info.value.json_body == json_body


@pytest.mark.asyncio
async def test_429_status_becomes_rate_limit_error():
    fn = _wrap_raises("get input", HttpStatusError(429, b""))
    with pytest.raises(RateLimitError) as exc_info:
        await fn()
    assert "429" in str(exc_info.value)


@pytest.mark.asyncio
async def test_5xx_status_becomes_server_error():
    fn = _wrap_raises("get input", HttpStatusError(503, b'{"error": "boom"}'))
    with pytest.raises(ServerError) as exc_info:
        await fn()
    msg = str(exc_info.value)
    assert "503" in msg
    assert "boom" in msg


@pytest.mark.asyncio
async def test_status_error_with_non_json_body_uses_raw_text():
    fn = _wrap_raises("get input", HttpStatusError(503, b"raw error string"))
    with pytest.raises(ServerError) as exc_info:
        await fn()
    assert "raw error string" in str(exc_info.value)


@pytest.mark.asyncio
async def test_json_decode_error_becomes_render_error():
    fn = _wrap_raises("get input", json.JSONDecodeError("expecting value", "doc", 0))
    with pytest.raises(RenderError) as exc_info:
        await fn()
    msg = str(exc_info.value)
    assert "get input failed" in msg
    assert "non-JSON response" in msg


@pytest.mark.asyncio
async def test_render_error_propagates_unchanged():
    """RenderError subclasses raised inside the wrapped function (e.g.,
    a method's own "unexpected response shape" guard) pass through with
    their original identity — no re-wrapping."""
    original = ClientError("already typed")
    fn = _wrap_raises("op", original)
    with pytest.raises(ClientError) as exc_info:
        await fn()
    assert exc_info.value is original


def test_sync_variant_translates_the_same_way():
    @_translate_errors_sync("record step")
    def fn():
        raise HttpStatusError(429, b'{"message": "slow down"}')

    with pytest.raises(RateLimitError, match="record step failed with status 429"):
        fn()
