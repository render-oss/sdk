"""Minimal HTTP/1.1 over Unix Domain Socket client.

Built on :class:`http.client.HTTPConnection` so request construction,
header formatting, Content-Length handling, and response parsing
(including chunked, content-length, and connection-close framing) are
all delegated to the standard library. The only custom piece is the
UDS connector: a subclass that overrides ``connect()`` to dial an
``AF_UNIX`` socket instead of TCP.

``http.client`` is sync, so each request runs on the asyncio
threadpool via :func:`asyncio.to_thread`. The thread context switch is
in the microseconds — imperceptible next to the actual UDS round trip
— and keeps the event loop free for the workflow runner.

This module raises only stdlib exceptions and :class:`HttpStatusError`.
Translation to ``render_sdk.client.errors`` types happens at the call
site in ``client.py`` via the ``_translate_errors`` decorator, so the
transport stays unaware of domain-level error vocabulary or operation
labels.
"""

from __future__ import annotations

import asyncio
import http.client
import json
import logging
import socket
from typing import Any

logger = logging.getLogger(__name__)


class HttpStatusError(Exception):
    """Raised when an HTTP request completes with a 4xx or 5xx status.

    Carries the status code and raw response body so the caller can
    translate the failure into the appropriate domain-level error.
    """

    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}")


class _UnixHTTPConnection(http.client.HTTPConnection):
    """HTTPConnection that dials a Unix Domain Socket instead of TCP."""

    def __init__(self, socket_path: str, timeout: float) -> None:
        super().__init__("localhost", timeout=timeout)
        self._socket_path = socket_path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self._socket_path)
        self.sock = sock


def _request_sync(
    socket_path: str,
    method: str,
    path: str,
    *,
    body: bytes | None,
    content_type: str | None,
    user_agent: str,
    timeout: float,
) -> tuple[int, bytes]:
    conn = _UnixHTTPConnection(socket_path, timeout)
    try:
        headers: dict[str, str] = {
            "Connection": "close",
            "User-Agent": user_agent,
            "Accept": "application/json",
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        return resp.status, resp.read()
    finally:
        conn.close()


async def request_json(
    socket_path: str,
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None,
    user_agent: str,
    timeout: float,
) -> Any:
    """Make a JSON HTTP request over UDS and return the parsed body.

    Returns ``None`` if the response has an empty body. HTTP error
    statuses (4xx, 5xx) raise :class:`HttpStatusError`; all other
    transport failures propagate as their stdlib exception types
    (``TimeoutError``, ``ConnectionError``, ``OSError``,
    ``http.client.HTTPException``, ``json.JSONDecodeError``).
    """
    body_bytes: bytes | None = None
    content_type: str | None = None
    if body is not None:
        body_bytes = json.dumps(body).encode("utf-8")
        content_type = "application/json"

    status_code, content = await asyncio.to_thread(
        _request_sync,
        socket_path,
        method,
        path,
        body=body_bytes,
        content_type=content_type,
        user_agent=user_agent,
        timeout=timeout,
    )

    if status_code >= 400:
        raise HttpStatusError(status_code, content)

    if not content:
        return None
    # JSONDecodeError intentionally propagates — the call-site decorator
    # turns it into a typed RenderError with operation context.
    return json.loads(content)
