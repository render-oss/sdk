# Auto-generated sync version. Do not edit — run scripts/unasync.py instead.

"""High-level client for creating and operating Render sandboxes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from render_sdk.client.errors import RenderError
from render_sdk.experimental.sandbox.api_sync import SyncSandboxApi
from render_sdk.experimental.sandbox.types import Sandbox, SandboxExecEvent, SandboxList

if TYPE_CHECKING:
    from render_sdk.public_api.client import AuthenticatedClient, Client


class SyncSandboxClient:
    """High-level client for creating and operating Render sandboxes."""

    def __init__(
        self,
        client: AuthenticatedClient | Client,
        default_owner_id: str | None = None,
        default_region: str | None = None,
    ):
        self.client = client
        self.api = SyncSandboxApi(client)
        self._default_owner_id = default_owner_id
        self._default_region = default_region

    def _resolve_owner_id(self, owner_id: str | None) -> str:
        resolved = owner_id or self._default_owner_id
        if not resolved:
            raise RenderError(
                "owner_id is required. Provide it as a parameter or set the RENDER_WORKSPACE_ID environment variable."
            )
        return resolved

    def create(
        self,
        *,
        owner_id: str | None = None,
        plan: str | None = None,
        timeout_seconds: int | None = None,
        network_policy: str | None = None,
        region: str | None = None,
    ) -> Sandbox:
        """Create a sandbox and return its initial snapshot.

        All parameters are optional. Unspecified fields fall back to the
        workspace defaults enforced by the API (plan starter, 7200s timeout,
        workspace default region and network policy).
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = region or self._default_region
        return self.api.create(
            owner_id=resolved_owner_id,
            plan=plan,
            timeout_seconds=timeout_seconds,
            network_policy=network_policy,
            region=resolved_region,
        )

    def from_id(self, sandbox_id: str, *, owner_id: str | None = None) -> Sandbox:
        """Reconnect to an existing sandbox by id.

        Raises SandboxNotFoundError if the sandbox does not exist or has been
        terminated.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.get(sandbox_id, resolved_owner_id)

    def list(
        self,
        *,
        owner_id: str | None = None,
        status: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SandboxList:
        """List sandboxes for a workspace.

        status filters by a single sandbox status (one of creating, running,
        suspended, resuming, errored, terminated). limit is capped at 100 by
        the API.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.list(resolved_owner_id, status, cursor, limit)

    def terminate(self, sandbox_id: str, *, owner_id: str | None = None) -> None:
        """Terminate a sandbox.

        Idempotent for an already-terminated sandbox (the API returns 204).
        Raises SandboxNotFoundError if the sandbox id was never valid.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        self.api.terminate(sandbox_id, resolved_owner_id)

    def exec(
        self,
        sandbox_id: str,
        command: str,
        *,
        owner_id: str | None = None,
    ) -> Iterator[SandboxExecEvent]:
        """Run a command in a sandbox and stream its output.

        command is passed to ``bash -c`` in the sandbox. Yields
        SandboxExecOutput chunks as they arrive and a final SandboxExecExit.
        A non-zero exit code is reported via SandboxExecExit, not an exception.
        Raises SandboxExecStreamError if the sandbox reports a terminal error.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.exec_stream(sandbox_id, command, resolved_owner_id)
