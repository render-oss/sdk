"""Typed wrapper over the generated public_api sandbox endpoints."""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

import httpx

from render_sdk.client.errors import RenderError
from render_sdk.client.util import (
    handle_api_error,
    handle_http_errors,
    handle_httpx_exception,
)
from render_sdk.experimental.sandbox.errors import SandboxNotFoundError
from render_sdk.experimental.sandbox.types import Sandbox, SandboxList
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

    @handle_http_errors("create sandbox")
    async def _create_api_call(
        self, body: SandboxPOST
    ) -> Response[Error | GeneratedSandbox]:
        return await create_sandbox.asyncio_detailed(client=self.client, body=body)
