"""Typed wrapper over the generated public_api sandbox endpoints."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import datetime
from typing import TYPE_CHECKING, Any, NoReturn

import httpx

from render_sdk.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
)
from render_sdk.client.util import (
    handle_api_error,
    handle_http_errors,
    handle_httpx_exception,
)
from render_sdk.experimental.sandbox.errors import (
    SandboxExecError,
    SandboxExecStreamError,
    SandboxNotFoundError,
)
from render_sdk.experimental.sandbox.types import (
    Sandbox,
    SandboxExecEvent,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxList,
)
from render_sdk.public_api.api.sandboxes import (
    create_sandbox,
    list_sandboxes,
    retrieve_sandbox,
    terminate_sandbox,
)
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.models.sandbox import Sandbox as GeneratedSandbox
from render_sdk.public_api.models.sandbox_network_policy import SandboxNetworkPolicy
from render_sdk.public_api.models.sandbox_network_policy_default import (
    SandboxNetworkPolicyDefault,
)
from render_sdk.public_api.models.sandbox_plan import SandboxPlan
from render_sdk.public_api.models.sandbox_post import SandboxPOST
from render_sdk.public_api.models.sandbox_post_env import SandboxPOSTEnv
from render_sdk.public_api.models.sandbox_status import SandboxStatus
from render_sdk.public_api.models.sandbox_with_cursor import SandboxWithCursor
from render_sdk.public_api.types import UNSET, Response

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient, Client


# Aliased at module scope so the annotation on _list_api_call resolves the
# builtin list, not the SandboxApi.list method that shadows it in the class body.
_SandboxWithCursorList = list[SandboxWithCursor]


def _to_sandbox(model: GeneratedSandbox) -> Sandbox:
    terminated = model.terminated_at
    return Sandbox(
        id=model.id,
        status=model.status.value,
        plan=model.plan.value,
        network_policy=model.network_policy.default.value,
        region=model.region,
        timeout_seconds=model.timeout_seconds,
        created_at=model.created_at,
        terminated_at=terminated if isinstance(terminated, datetime) else None,
    )


class SandboxApi:
    """Typed wrapper over the generated sandbox endpoints."""

    def __init__(self, client: AuthenticatedClient | Client):
        self.client = client

    async def create(
        self,
        owner_id: str,
        plan: str | None,
        timeout_seconds: int | None,
        network_policy: str | None,
        region: str | None,
        env: dict[str, str] | None,
    ) -> Sandbox:
        body = SandboxPOST(owner_id=owner_id)
        if plan is not None:
            body.plan = SandboxPlan(plan)
        if timeout_seconds is not None:
            body.timeout_seconds = timeout_seconds
        if region is not None:
            body.region = region
        if network_policy is not None:
            body.network_policy = SandboxNetworkPolicy(
                default=SandboxNetworkPolicyDefault(network_policy)
            )
        if env is not None:
            body.env = SandboxPOSTEnv.from_dict(env)

        response = await self._create_api_call(body)
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to create sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    async def get(self, sandbox_id: str, owner_id: str) -> Sandbox:
        try:
            response = await retrieve_sandbox.asyncio_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "retrieve sandbox")
        except json.JSONDecodeError as exc:
            body = exc.doc.strip() if exc.doc else "empty response"
            raise RenderError(
                f"retrieve sandbox failed: server returned a non-JSON response: {body}"
            ) from exc
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        handle_api_error(response, "retrieve sandbox")
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to retrieve sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    async def list(
        self,
        owner_id: str,
        status: str | None,
        cursor: str | None,
        limit: int | None,
    ) -> SandboxList:
        response = await self._list_api_call(owner_id, status, cursor, limit)
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list sandboxes: unexpected response type")
        sandboxes = [_to_sandbox(item.sandbox) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SandboxList(sandboxes=sandboxes, next_cursor=next_cursor)

    @handle_http_errors("list sandboxes")
    async def _list_api_call(
        self,
        owner_id: str,
        status: str | None,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxWithCursorList]:
        return await list_sandboxes.asyncio_detailed(
            client=self.client,
            owner_id=[owner_id],
            status=[SandboxStatus(status)] if status is not None else UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    async def terminate(self, sandbox_id: str, owner_id: str) -> None:
        try:
            response = await terminate_sandbox.asyncio_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "terminate sandbox")
        except json.JSONDecodeError as exc:
            body = exc.doc.strip() if exc.doc else "empty response"
            raise RenderError(
                f"terminate sandbox failed: server returned a non-JSON response: {body}"
            ) from exc
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        handle_api_error(response, "terminate sandbox")

    async def _mint_run_token(
        self, sandbox_id: str, owner_id: str, operation: str
    ) -> dict[str, Any]:
        api_client = self.client.get_async_httpx_client()
        try:
            response = await api_client.post(
                f"/sandboxes/{sandbox_id}/runs/{operation}/token",
                params={"ownerId": owner_id},
            )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "connect sandbox run")
        if response.status_code >= 400:
            _raise_exec_http_error(sandbox_id, response.status_code, response.text)
        return response.json()

    async def exec_stream(
        self, sandbox_id: str, command: str, owner_id: str, operation: str = "stream"
    ) -> AsyncIterator[SandboxExecEvent]:
        connection = await self._mint_run_token(sandbox_id, owner_id, operation)
        token = connection["token"]
        uri = connection["uri"]
        method = connection["method"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }
        # Read timeout at 3x the server's 15s SSE keep-alive interval, so a dead
        # connection is detected without cutting off a live but idle stream.
        timeout = httpx.Timeout(5.0, read=45.0, write=None)
        try:
            async with (
                httpx.AsyncClient(timeout=timeout) as proxy_client,
                proxy_client.stream(
                    method, uri, headers=headers, json={"command": command}
                ) as response,
            ):
                if response.status_code >= 400:
                    body = (await response.aread()).decode("utf-8", errors="replace")
                    _raise_exec_http_error(sandbox_id, response.status_code, body)
                async for name, data in _iter_sse_events(response.aiter_lines()):
                    if name == "output":
                        payload = _load_event(data)
                        yield SandboxExecOutput(
                            stream=payload["stream"], data=payload["data"]
                        )
                    elif name == "exit":
                        payload = _load_event(data)
                        yield SandboxExecExit(exit_code=payload["exit_code"])
                        return
                    elif name == "error":
                        payload = _load_event(data)
                        raise SandboxExecStreamError(
                            payload.get("status", 0), payload.get("message", "")
                        )
                    else:
                        raise SandboxExecError(f"unknown sandbox exec event {name!r}")
                raise SandboxExecError(
                    "sandbox exec stream ended without an exit event"
                )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "exec sandbox")

    @handle_http_errors("create sandbox")
    async def _create_api_call(
        self, body: SandboxPOST
    ) -> Response[Error | GeneratedSandbox]:
        return await create_sandbox.asyncio_detailed(client=self.client, body=body)


def _load_event(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise SandboxExecError(
            f"failed to parse sandbox exec event data: {data}"
        ) from exc


def _raise_exec_http_error(sandbox_id: str, status_code: int, body: str) -> NoReturn:
    message = f"exec failed with status {status_code}"
    if body:
        message = f"{message}: {body}"
    if status_code == 404:
        raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
    if status_code == 429:
        raise RateLimitError(message)
    if 400 <= status_code < 500:
        raise ClientError(message)
    raise ServerError(message)


async def _iter_sse_events(
    lines: AsyncIterator[str],
) -> AsyncIterator[tuple[str, str]]:
    event_name = ""
    data_parts: list[str] = []
    async for raw in lines:
        line = raw.rstrip("\r")
        if line == "":
            if event_name or data_parts:
                yield event_name, "\n".join(data_parts)
                event_name = ""
                data_parts = []
            continue
        if line.startswith(":"):
            continue
        if line.startswith("event:"):
            event_name = line[len("event:") :].strip()
        elif line.startswith("data:"):
            chunk = line[len("data:") :]
            if chunk.startswith(" "):
                chunk = chunk[1:]
            data_parts.append(chunk)
    if event_name or data_parts:
        yield event_name, "\n".join(data_parts)
