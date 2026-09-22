# Auto-generated sync version. Do not edit — run scripts/unasync.py instead.

"""High-level client for creating and operating Render sandboxes."""

from __future__ import annotations

import os
from collections.abc import Iterator, Sequence
from datetime import datetime
from typing import TYPE_CHECKING

from render.client.errors import RenderError
from render.experimental.sandbox.api_sync import SyncSandboxApi
from render.experimental.sandbox.files import normalize_remote_path
from render.experimental.sandbox.types import (
    Sandbox,
    SandboxExecEvent,
    SandboxGroupList,
    SandboxList,
    Snapshot,
    SnapshotList,
)
from render.public_api.types import UNSET, Unset

if TYPE_CHECKING:
    from render.public_api.client import AuthenticatedClient, Client


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
        self.snapshots = SyncSnapshotClient(self)
        self._default_owner_id = default_owner_id
        self._default_region = default_region

    def _resolve_owner_id(self, owner_id: str | None) -> str:
        resolved = owner_id or self._default_owner_id
        if not resolved:
            raise RenderError(
                "owner_id is required. Provide it as a parameter or set the RENDER_WORKSPACE_ID environment variable."
            )
        return resolved

    def _optional_owner_id(self, owner_id: str | None) -> str | Unset:
        return owner_id or self._default_owner_id or UNSET

    def create(
        self,
        *,
        owner_id: str | None = None,
        plan: str | None = None,
        timeout_seconds: int | None = None,
        network_policy: str | None = None,
        region: str | None = None,
        env: dict[str, str] | None = None,
        snapshot_id: str | None = None,
        snapshot_name: str | None = None,
    ) -> Sandbox:
        """Create a sandbox and return its initial state.

        All parameters are optional. Unspecified fields fall back to the
        workspace defaults enforced by the API (plan starter, 7200s timeout,
        workspace default region and network policy).

        snapshot_id starts the sandbox from that snapshot; snapshot_name starts
        it from the available snapshot that name currently resolves to in the
        sandbox group. The two parameters are mutually exclusive. For a runtime
        snapshot, plan must match the snapshot's plan. Raises
        SnapshotNotFoundError if the snapshot ID or name does not resolve,
        SnapshotNotReadyError if it is not available, and
        SnapshotPlanMismatchError on a runtime plan mismatch.
        """
        if snapshot_id is not None and snapshot_name is not None:
            raise ValueError("snapshot_id and snapshot_name are mutually exclusive")
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = region or self._default_region
        return self.api.create(
            owner_id=resolved_owner_id,
            plan=plan,
            timeout_seconds=timeout_seconds,
            network_policy=network_policy,
            region=resolved_region,
            env=env,
            snapshot_id=snapshot_id,
            snapshot_name=snapshot_name,
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
        status: str | Sequence[str] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SandboxList:
        """List sandboxes for a workspace.

        status filters by sandbox status, one or a sequence of them (each one
        of creating, running, suspended, resuming, errored, terminated). limit
        is capped at 100 by the API.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.list(resolved_owner_id, status, cursor, limit)

    def list_groups(self, *, owner_id: str | None = None) -> SandboxGroupList:
        """List the sandbox groups a workspace owns.

        Alpha guarantees at most one group per workspace, so the page holds
        zero or one group. next_cursor carries the cursor of the last entry,
        or None when the page is empty.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.list_groups(resolved_owner_id)

    def terminate(self, sandbox_id: str, *, owner_id: str | None = None) -> None:
        """Terminate a sandbox.

        Idempotent for an already-terminated sandbox (the API returns 204).
        Raises SandboxNotFoundError if the sandbox id was never valid.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        self.api.terminate(sandbox_id, resolved_owner_id)

    def copy_to(
        self,
        sandbox_id: str,
        local_path: str | os.PathLike[str],
        remote_path: str,
        *,
        owner_id: str | None = None,
    ) -> None:
        """Copy a local file or directory into the sandbox at remote_path.

        A relative remote_path resolves under the sandbox's home directory and
        an absolute one addresses the filesystem, as scp does. The path is
        normalized before it is sent, so a trailing slash or a redundant
        separator is accepted rather than rejected by the sandbox.

        A file is uploaded as raw bytes. A directory is streamed as an archive
        that the sandbox extracts at remote_path: names are relative to
        local_path, symlinks are stored rather than followed, and sockets,
        fifos and other special files are skipped. Passing one of those special
        files as local_path raises ValueError.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        self.api.upload(sandbox_id, local_path, remote_path, resolved_owner_id)

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

    def copy_from(
        self,
        sandbox_id: str,
        remote_path: str,
        local_path: str | os.PathLike[str],
        *,
        owner_id: str | None = None,
    ) -> str:
        """Copy a file or directory out of a sandbox, returning the path written.

        A directory is extracted under local_path. A file is written to
        local_path, or into it under the name the sandbox suggests when
        local_path is an existing directory. remote_path is cleaned before it
        is sent, since the API rejects a path carrying "." , ".." or redundant
        separators. Raises SandboxFileNotFoundError if the sandbox has no such
        path. Raises SandboxDownloadError if the response is unsafe or the download
        cannot be written or extracted locally. Directory extraction is not atomic
        and may leave partial contents after a failure.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.download_file(
            sandbox_id,
            normalize_remote_path(remote_path),
            os.fspath(local_path),
            resolved_owner_id,
        )


class SyncSnapshotClient:
    """Snapshots of sandboxes, accessed via ``SyncSandboxClient.snapshots``."""

    def __init__(self, sandboxes: SyncSandboxClient):
        self._sandboxes = sandboxes

    def create(
        self,
        sandbox_id: str,
        *,
        kind: str = "filesystem",
        name: str | None = None,
        expires_at: datetime | None = None,
        owner_id: str | None = None,
    ) -> Snapshot:
        """Capture a snapshot of a running sandbox.

        kind is filesystem (the writable filesystem) or runtime (also memory and
        CPU state). name is case sensitive and can be reused within a sandbox
        group. expires_at must be in the future; omit it for Render's default
        snapshot lifetime. The snapshot is returned in
        status creating; poll from_id until it is available or failed. Raises
        SandboxNotFoundError if the sandbox does not exist, and a ClientError
        with code sandbox_not_running if it is not running.
        """
        return self._sandboxes.api.create_snapshot(
            sandbox_id,
            kind,
            name,
            expires_at,
            self._sandboxes._optional_owner_id(owner_id),
        )

    def from_id(
        self,
        *,
        sandbox_group_id: str,
        snapshot_id: str,
        owner_id: str | None = None,
    ) -> Snapshot:
        """Fetch a snapshot by id.

        Raises SnapshotNotFoundError if the snapshot does not exist, was
        deleted, has expired, or belongs to another sandbox group.
        """
        return self._sandboxes.api.get_snapshot(
            sandbox_group_id, snapshot_id, self._sandboxes._optional_owner_id(owner_id)
        )

    def list(
        self,
        *,
        sandbox_group_id: str,
        status: str | Sequence[str] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        owner_id: str | None = None,
    ) -> SnapshotList:
        """List snapshots of one sandbox group, newest first.

        Deleted and expired snapshots are omitted. status filters by snapshot
        status, one or a sequence of them (each one of creating, available,
        failed). limit is capped at 100 by the API.
        """
        resolved_owner_id = self._sandboxes._resolve_owner_id(owner_id)
        return self._sandboxes.api.list_snapshots(
            resolved_owner_id, sandbox_group_id, status, cursor, limit
        )

    def delete(
        self,
        *,
        sandbox_group_id: str,
        snapshot_id: str,
        owner_id: str | None = None,
    ) -> None:
        """Delete a snapshot.

        Idempotent for an already-deleted or expired snapshot (the API returns
        204). Raises SnapshotNotFoundError if the snapshot never existed, and
        SnapshotNotReadyError if it is still creating.
        """
        self._sandboxes.api.delete_snapshot(
            sandbox_group_id, snapshot_id, self._sandboxes._optional_owner_id(owner_id)
        )
