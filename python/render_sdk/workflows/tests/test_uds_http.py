"""Integration tests for the hand-rolled UDS HTTP transport.

These tests bring up a real ``aiohttp`` server bound to a Unix Domain
Socket so they exercise the actual ``http.client``-based transport
end-to-end against a real socket.
"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile

import pytest
from aiohttp import web

from render_sdk.workflows._uds_http import HttpStatusError, request_json

# Note: we deliberately do NOT import ``TimeoutError`` from
# render_sdk.client.errors here, so the built-in ``TimeoutError`` stays
# in scope for the timeout assertion below (socket.timeout aliases it).


@pytest.fixture
def socket_path(tmp_path):
    """Returns a path suitable for binding a UDS server to."""
    # tmp_path can be longer than the OS-level UDS path limit (~104 chars on
    # macOS), so fall back to a short path under /tmp when needed.
    candidate = str(tmp_path / "render-sdk-test.sock")
    if len(candidate) >= 100:
        with tempfile.NamedTemporaryFile(
            prefix="render-sdk-", suffix=".sock", delete=True
        ) as f:
            candidate = f.name
        if os.path.exists(candidate):
            os.unlink(candidate)
    return candidate


async def _start_server(handler, socket_path: str) -> web.AppRunner:
    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.UnixSite(runner, socket_path)
    await site.start()
    return runner


@pytest.mark.asyncio
async def test_request_json_get_returns_parsed_body(socket_path):
    async def handler(request: web.Request) -> web.Response:
        assert request.method == "GET"
        assert request.path == "/input"
        return web.json_response({"task_name": "t", "input": "blob"})

    runner = await _start_server(handler, socket_path)
    try:
        result = await request_json(
            socket_path,
            "GET",
            "/input",
            body=None,
            user_agent="test",
            timeout=5.0,
        )
        assert result == {"task_name": "t", "input": "blob"}
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_request_json_post_sends_json_body(socket_path):
    received: dict = {}

    async def handler(request: web.Request) -> web.Response:
        received["method"] = request.method
        received["path"] = request.path
        received["content_type"] = request.headers.get("Content-Type")
        received["body"] = await request.json()
        return web.json_response({"task_run_id": "tr-1"})

    runner = await _start_server(handler, socket_path)
    try:
        result = await request_json(
            socket_path,
            "POST",
            "/run-subtask",
            body={"task_name": "x", "input": "y"},
            user_agent="test",
            timeout=5.0,
        )
        assert result == {"task_run_id": "tr-1"}
        assert received["method"] == "POST"
        assert received["path"] == "/run-subtask"
        assert received["content_type"] == "application/json"
        assert received["body"] == {"task_name": "x", "input": "y"}
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_request_json_empty_response_returns_none(socket_path):
    async def handler(request: web.Request) -> web.Response:
        return web.Response(status=200, body=b"")

    runner = await _start_server(handler, socket_path)
    try:
        result = await request_json(
            socket_path,
            "POST",
            "/callback",
            body={"complete": {"output": "ok"}},
            user_agent="test",
            timeout=5.0,
        )
        assert result is None
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_request_json_error_status_raises_http_status_error(socket_path):
    async def handler(request: web.Request) -> web.Response:
        return web.json_response({"message": "bad input"}, status=400)

    runner = await _start_server(handler, socket_path)
    try:
        with pytest.raises(HttpStatusError) as exc_info:
            await request_json(
                socket_path,
                "POST",
                "/run-subtask",
                body={},
                user_agent="test",
                timeout=5.0,
            )
        assert exc_info.value.status == 400
        assert b"bad input" in exc_info.value.body
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_request_json_connection_refused_raises_oserror():
    # Path that doesn't exist -> connection refused / no such file. The
    # transport propagates the OSError unchanged; translation is the
    # caller's responsibility.
    with pytest.raises((ConnectionError, FileNotFoundError)):
        await request_json(
            "/tmp/does-not-exist-render-sdk.sock",  # noqa: S108
            "GET",
            "/input",
            body=None,
            user_agent="test",
            timeout=5.0,
        )


@pytest.mark.asyncio
async def test_request_json_non_json_body_raises_json_decode_error(socket_path):
    async def handler(request: web.Request) -> web.Response:
        return web.Response(status=200, body=b"not json", content_type="text/plain")

    runner = await _start_server(handler, socket_path)
    try:
        with pytest.raises(json.JSONDecodeError):
            await request_json(
                socket_path,
                "GET",
                "/input",
                body=None,
                user_agent="test",
                timeout=5.0,
            )
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_request_json_timeout_raises_timeout_error(socket_path):
    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(2.0)
        return web.json_response({})

    runner = await _start_server(handler, socket_path)
    try:
        with pytest.raises(TimeoutError):
            await request_json(
                socket_path,
                "GET",
                "/input",
                body=None,
                user_agent="test",
                timeout=0.2,
            )
    finally:
        await runner.cleanup()
