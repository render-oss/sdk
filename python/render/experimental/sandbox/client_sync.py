# Auto-generated sync version. Do not edit — run scripts/unasync.py instead.

"""High-level client for creating and operating Render sandboxes."""

from __future__ import annotations

import os
from collections.abc import Iterator, Sequence
from datetime import datetime
from typing import TYPE_CHECKING

from render.client.errors import RenderError
from render.experimental.sandbox import _wait
from render.experimental.sandbox.api_sync import SyncSandboxApi
from render.experimental.sandbox.errors import (
    SandboxCreateWaitError,
    SandboxWaitTimeoutError,
    SnapshotCreateWaitError,
    SnapshotWaitTimeoutError,
)
from render.experimental.sandbox.files import normalize_remote_path
from render.experimental.sandbox.types import (
    Build,
    NetworkPolicy,
    RegistryCredential,
    Sandbox,
    SandboxExecEvent,
    SandboxGroup,
    SandboxGroupList,
    SandboxList,
    SandboxPlan,
    SandboxWaitOptions,
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
        self.builds = SyncBuildClient(self)
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
        plan: SandboxPlan | str | None = None,
        timeout_seconds: int | None = None,
        idle_timeout_seconds: int | None = None,
        network_policy: NetworkPolicy | str | None = None,
        region: str | None = None,
        env: dict[str, str] | None = None,
        snapshot_id: str | None = None,
        snapshot_name: str | None = None,
        build_id: str | None = None,
        build_name: str | None = None,
        sandbox_group_id: str | None = None,
        wait: bool | SandboxWaitOptions = False,
    ) -> Sandbox:
        """Create a sandbox and return its initial state.

        All parameters are optional. Unspecified fields fall back to the
        workspace defaults enforced by the API (plan 1c-2g, 24-hour lifetime,
        15-minute idle timeout, workspace default region and network policy).
        Set idle_timeout_seconds to 0 to disable automatic idle suspension.
        sandbox_group_id defaults to the workspace's default group. The group
        determines placement; region is accepted for compatibility and ignored.

        network_policy is a NetworkPolicy, or a policy type string as a
        shorthand for one without rules. To restrict outbound traffic to
        specific destinations, pass
        NetworkPolicy(type="allow-list", rules=[EgressRule(domain=...)]).

        snapshot_id starts the sandbox from that snapshot; snapshot_name starts
        it from the available snapshot that name currently resolves to in the
        sandbox group. The two parameters are mutually exclusive. For a runtime
        snapshot, plan must match the snapshot's plan. Raises
        SnapshotNotFoundError if the snapshot ID or name does not resolve,
        SnapshotNotReadyError if it is not available, and
        SnapshotPlanMismatchError on a runtime plan mismatch.

        build_id starts the sandbox from that build's image instead of the
        base image; build_name starts it from the newest succeeded build with
        that name in the sandbox group. The two are mutually exclusive with
        each other and with the snapshot parameters. Raises BuildNotFoundError
        if the group has no build with the ID or name, and BuildNotReadyError
        if the build has not succeeded.

        wait returns the sandbox only once it is running, as wait_until_running
        does. True uses the default wait; a SandboxWaitOptions sets its timeout
        and interval. The wait starts after the create request returns. If it
        fails, create raises SandboxCreateWaitError with the new sandbox's id,
        so you can terminate it.

        To bound the wait, set SandboxWaitOptions(timeout_seconds=...). Don't
        wrap create(wait=...) in asyncio.wait_for: its timeout cancels the task,
        and a cancelled create loses the new sandbox's id.
        """
        if snapshot_id is not None and snapshot_name is not None:
            raise ValueError("snapshot_id and snapshot_name are mutually exclusive")
        if build_id is not None and build_name is not None:
            raise ValueError("build_id and build_name are mutually exclusive")
        if (build_id is not None or build_name is not None) and (
            snapshot_id is not None or snapshot_name is not None
        ):
            raise ValueError("a build and a snapshot are mutually exclusive")
        wait_settings = _wait.resolve_create_wait(
            wait, _wait.DEFAULT_SANDBOX_TIMEOUT_SECONDS
        )
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = region or self._default_region
        sandbox = self.api.create(
            owner_id=resolved_owner_id,
            plan=plan,
            timeout_seconds=timeout_seconds,
            idle_timeout_seconds=idle_timeout_seconds,
            network_policy=network_policy,
            region=resolved_region,
            env=env,
            snapshot_id=snapshot_id,
            snapshot_name=snapshot_name,
            build_id=build_id,
            build_name=build_name,
            sandbox_group_id=sandbox_group_id,
        )
        if wait_settings is None:
            return sandbox
        # The sandbox exists from here on, so every failure must give the
        # caller its id.
        try:
            return _wait.running_sandbox(sandbox) or self.wait_until_running(
                sandbox.id,
                timeout_seconds=wait_settings.timeout_seconds,
                interval_seconds=wait_settings.interval_seconds,
                owner_id=resolved_owner_id,
            )
        except Exception as exc:
            raise SandboxCreateWaitError(
                f"created sandbox {sandbox.id}, but it is not running: {exc}",
                sandbox_id=sandbox.id,
                cause=exc,
            ) from exc

    def wait_until_running(
        self,
        sandbox_id: str,
        *,
        timeout_seconds: float = _wait.DEFAULT_SANDBOX_TIMEOUT_SECONDS,
        interval_seconds: float = _wait.DEFAULT_INTERVAL_SECONDS,
        owner_id: str | None = None,
    ) -> Sandbox:
        """Wait until the sandbox is running, so it can run commands, and return it.

        Checks the status every interval_seconds, doubling the delay after each
        check up to 2 seconds. timeout_seconds bounds the whole wait, including
        status checks. Raises SandboxNotRunningError as soon as the sandbox is
        errored, terminated, suspending, or suspended, and
        SandboxWaitTimeoutError after timeout_seconds. Neither terminates the
        sandbox. Errors from a status check, such as SandboxNotFoundError,
        propagate unchanged.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)

        def timeout_error(last: Sandbox | None) -> SandboxWaitTimeoutError:
            return SandboxWaitTimeoutError(
                f"timed out waiting for sandbox {sandbox_id} to be running",
                sandbox_id=sandbox_id,
                timeout_seconds=timeout_seconds,
                last_status=last.status if last else None,
            )

        return _wait.poll_until(
            lambda: self.api.get(sandbox_id, resolved_owner_id),
            _wait.running_sandbox,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            timeout_error=timeout_error,
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
        sandbox_group_id: str | None = None,
    ) -> SandboxList:
        """List sandboxes for a workspace.

        status filters by sandbox status, one or a sequence of them (each one
        of creating, running, suspended, resuming, errored, terminated). limit
        is capped at 100 by the API.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.list(resolved_owner_id, status, cursor, limit, sandbox_group_id)

    def list_groups(
        self,
        *,
        owner_id: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SandboxGroupList:
        """List the sandbox groups a workspace owns.

        Omit cursor and limit to return all groups. When paging, continue
        until the page is empty. next_cursor carries the last entry's cursor,
        or None when the page is empty.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.list_groups(resolved_owner_id, cursor, limit)

    def create_group(
        self, name: str, *, owner_id: str | None = None, region: str | None = None
    ) -> SandboxGroup:
        """Create a group within the workspace's configured group count limit."""
        return self.api.create_group(self._resolve_owner_id(owner_id), name, region)

    def get_group(self, sandbox_group_id: str) -> SandboxGroup:
        """Retrieve a sandbox group by ID."""
        return self.api.get_group(sandbox_group_id)

    def update_group(
        self, sandbox_group_id: str, *, concurrency_limit: int
    ) -> SandboxGroup:
        """Set concurrency and return the effective limit after Render's cap."""
        return self.api.update_group(sandbox_group_id, concurrency_limit)

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
        kind: str | None = None,
        name: str | None = None,
        expires_at: datetime | None = None,
        owner_id: str | None = None,
        wait: bool | SandboxWaitOptions = False,
    ) -> Snapshot:
        """Capture a snapshot of a running sandbox.

        kind is filesystem (the writable filesystem) or runtime (also memory and
        CPU state). name is case sensitive and can be reused within a sandbox
        group. expires_at must be in the future; omit it for Render's default
        snapshot lifetime. The snapshot is returned in
        status creating; call wait_until_available to wait for it. Raises
        SandboxNotFoundError if the sandbox does not exist, and a ClientError
        with code sandbox_not_running if it is not running.

        wait returns the snapshot only once it is available, as
        wait_until_available does. True uses the default wait; a
        SandboxWaitOptions sets its timeout and interval. Bad options raise
        ValueError before the create request. If the wait fails, create raises
        SnapshotCreateWaitError with the new snapshot's ids.

        To bound the wait, set SandboxWaitOptions(timeout_seconds=...). Don't
        wrap create(wait=...) in asyncio.wait_for: its timeout cancels the task,
        and a cancelled create loses the new snapshot's ids.
        """
        wait_settings = _wait.resolve_create_wait(
            wait, _wait.DEFAULT_SNAPSHOT_TIMEOUT_SECONDS
        )
        snapshot = self._sandboxes.api.create_snapshot(
            sandbox_id,
            kind,
            name,
            expires_at,
            self._sandboxes._optional_owner_id(owner_id),
        )
        if wait_settings is None:
            return snapshot
        # The snapshot exists from here on, so every failure must give the
        # caller its ids.
        try:
            available = _wait.available_snapshot(snapshot)
            return available or self.wait_until_available(
                sandbox_group_id=snapshot.sandbox_group_id,
                snapshot_id=snapshot.id,
                timeout_seconds=wait_settings.timeout_seconds,
                interval_seconds=wait_settings.interval_seconds,
                owner_id=owner_id,
            )
        except Exception as exc:
            raise SnapshotCreateWaitError(
                f"created snapshot {snapshot.id}, but it is not available: {exc}",
                snapshot_id=snapshot.id,
                sandbox_group_id=snapshot.sandbox_group_id,
                cause=exc,
            ) from exc

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

    def wait_until_available(
        self,
        *,
        sandbox_group_id: str,
        snapshot_id: str,
        timeout_seconds: float = _wait.DEFAULT_SNAPSHOT_TIMEOUT_SECONDS,
        interval_seconds: float = _wait.DEFAULT_INTERVAL_SECONDS,
        owner_id: str | None = None,
    ) -> Snapshot:
        """Wait until the snapshot is available, so sandboxes can start from it.

        Checks the status every interval_seconds, doubling the delay after each
        check up to 2 seconds. timeout_seconds bounds the whole wait, including
        status checks. Raises SnapshotFailedError, with the API's reason, as
        soon as the capture fails, and SnapshotWaitTimeoutError after
        timeout_seconds. Errors from a status check, such as
        SnapshotNotFoundError, propagate unchanged.
        """
        resolved_owner_id = self._sandboxes._optional_owner_id(owner_id)

        def timeout_error(last: Snapshot | None) -> SnapshotWaitTimeoutError:
            return SnapshotWaitTimeoutError(
                f"timed out waiting for snapshot {snapshot_id} to be available",
                snapshot_id=snapshot_id,
                timeout_seconds=timeout_seconds,
                last_status=last.status if last else None,
            )

        return _wait.poll_until(
            lambda: self._sandboxes.api.get_snapshot(
                sandbox_group_id, snapshot_id, resolved_owner_id
            ),
            _wait.available_snapshot,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            timeout_error=timeout_error,
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


class SyncBuildClient:
    """Builds of sandbox base images, accessed via ``SyncSandboxClient.builds``."""

    def __init__(self, sandboxes: SyncSandboxClient):
        self._sandboxes = sandboxes

    def create(
        self,
        *,
        sandbox_group_id: str,
        name: str,
        source_image: str,
        registry_credential: RegistryCredential | None = None,
    ) -> Build:
        """Start converting source_image into a sandbox base image.

        source_image is an image by tag or digest, like ``python:3.13``. It
        must be linux/amd64. name identifies the image and is reused across
        its builds. The build is returned before it finishes; poll from_id until
        its status is succeeded or failed. A build the group already has, or
        is running, for the same name and resolved digest is returned instead
        of starting another. Raises RateLimitError when the group has too
        many builds in progress.
        """
        return self._sandboxes.api.create_build(
            sandbox_group_id, name, source_image, registry_credential
        )

    def from_id(self, *, sandbox_group_id: str, build_id: str) -> Build:
        """Fetch a build by id.

        Raises BuildNotFoundError if the build does not exist or belongs to
        another sandbox group.
        """
        return self._sandboxes.api.get_build(sandbox_group_id, build_id)
