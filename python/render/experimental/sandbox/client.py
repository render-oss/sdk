"""High-level client for creating and operating Render sandboxes."""

from __future__ import annotations

import os
import re
import warnings
from collections.abc import AsyncIterator, Mapping, Sequence
from datetime import datetime
from typing import TYPE_CHECKING

from render.client.errors import RenderError
from render.experimental.sandbox import _wait
from render.experimental.sandbox.api import SandboxApi
from render.experimental.sandbox.errors import (
    ImageWaitTimeoutError,
    SandboxCreateWaitError,
    SandboxWaitTimeoutError,
    SnapshotCreateWaitError,
    SnapshotWaitTimeoutError,
)
from render.experimental.sandbox.files import normalize_remote_path
from render.experimental.sandbox.types import (
    Image,
    NetworkPolicy,
    RegistryCredentials,
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

# The format of an image ID; create(image=...) treats anything else as a name.
_IMAGE_ID_PATTERN = re.compile(r"sbb-[0-9a-v]{20}")


class SandboxClient:
    """High-level client for creating and operating Render sandboxes."""

    def __init__(
        self,
        client: AuthenticatedClient | Client,
        default_owner_id: str | None = None,
        default_region: str | None = None,
    ):
        self.client = client
        self.api = SandboxApi(client)
        self.snapshots = SnapshotClient(self)
        self.images = ImageClient(self)
        self.builds = BuildClient(self)
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

    async def create(
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
        image: str | None = None,
        build_id: str | None = None,
        build_name: str | None = None,
        sandbox_group_id: str | None = None,
        wait: bool | SandboxWaitOptions = False,
    ) -> Sandbox:
        """Create a sandbox and return its initial state.

        All parameters are optional. Unspecified fields fall back to the
        workspace defaults enforced by the API (plan 1c-2g, 24-hour lifetime,
        15-minute idle timeout, workspace default region and network policy).
        Set timeout_seconds to 0 to disable the lifetime limit.
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

        image starts the sandbox from an image imported with images.import_
        instead of the base image. An image ID (``sbb-`` and 20 characters,
        like ``sbb-cph1rs3idesc73a2b2mg``) pins that version; any other value
        is a name and uses the newest succeeded version with that name in the
        sandbox group. image is mutually exclusive with the snapshot
        parameters. Raises ImageNotFoundError if the group has no image with
        the ID or name, and ImageNotReadyError if it has not succeeded.
        build_id and build_name are deprecated aliases for image.

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
        if build_id is not None or build_name is not None:
            warnings.warn(
                "build_id and build_name are deprecated; use image",
                DeprecationWarning,
                stacklevel=2,
            )
        image_refs = [ref for ref in (image, build_id, build_name) if ref is not None]
        if len(image_refs) > 1:
            raise ValueError("image, build_id and build_name are mutually exclusive")
        if image_refs and (snapshot_id is not None or snapshot_name is not None):
            raise ValueError("an image and a snapshot are mutually exclusive")
        image_id = build_id
        image_name = build_name
        if image is not None:
            if _IMAGE_ID_PATTERN.fullmatch(image):
                image_id = image
            else:
                image_name = image
        wait_settings = _wait.resolve_create_wait(
            wait, _wait.DEFAULT_SANDBOX_TIMEOUT_SECONDS
        )
        resolved_owner_id = self._resolve_owner_id(owner_id)
        resolved_region = region or self._default_region
        sandbox = await self.api.create(
            owner_id=resolved_owner_id,
            plan=plan,
            timeout_seconds=timeout_seconds,
            idle_timeout_seconds=idle_timeout_seconds,
            network_policy=network_policy,
            region=resolved_region,
            env=env,
            snapshot_id=snapshot_id,
            snapshot_name=snapshot_name,
            image_id=image_id,
            image_name=image_name,
            sandbox_group_id=sandbox_group_id,
        )
        if wait_settings is None:
            return sandbox
        # The sandbox exists from here on, so every failure must give the
        # caller its id.
        try:
            return _wait.running_sandbox(sandbox) or await self.wait_until_running(
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

    async def wait_until_running(
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

        return await _wait.apoll_until(
            lambda: self.api.get(sandbox_id, resolved_owner_id),
            _wait.running_sandbox,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            timeout_error=timeout_error,
        )

    async def from_id(self, sandbox_id: str, *, owner_id: str | None = None) -> Sandbox:
        """Reconnect to an existing sandbox by id.

        Raises SandboxNotFoundError if the sandbox does not exist or has been
        terminated.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return await self.api.get(sandbox_id, resolved_owner_id)

    async def list(
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
        return await self.api.list(
            resolved_owner_id, status, cursor, limit, sandbox_group_id
        )

    async def list_groups(
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
        return await self.api.list_groups(resolved_owner_id, cursor, limit)

    async def create_group(
        self, name: str, *, owner_id: str | None = None, region: str | None = None
    ) -> SandboxGroup:
        """Create a group within the workspace's configured group count limit."""
        return await self.api.create_group(
            self._resolve_owner_id(owner_id), name, region
        )

    async def get_group(self, sandbox_group_id: str) -> SandboxGroup:
        """Retrieve a sandbox group by ID."""
        return await self.api.get_group(sandbox_group_id)

    async def update_group(
        self, sandbox_group_id: str, *, concurrency_limit: int
    ) -> SandboxGroup:
        """Set concurrency and return the effective limit after Render's cap."""
        return await self.api.update_group(sandbox_group_id, concurrency_limit)

    async def terminate(self, sandbox_id: str, *, owner_id: str | None = None) -> None:
        """Terminate a sandbox.

        Idempotent for an already-terminated sandbox (the API returns 204).
        Raises SandboxNotFoundError if the sandbox id was never valid.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        await self.api.terminate(sandbox_id, resolved_owner_id)

    async def copy_to(
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
        await self.api.upload(sandbox_id, local_path, remote_path, resolved_owner_id)

    def exec(
        self,
        sandbox_id: str,
        command: str,
        *,
        owner_id: str | None = None,
    ) -> AsyncIterator[SandboxExecEvent]:
        """Run a command in a sandbox and stream its output.

        command is passed to ``bash -c`` in the sandbox. Yields
        SandboxExecOutput chunks as they arrive and a final SandboxExecExit.
        A non-zero exit code is reported via SandboxExecExit, not an exception.
        Raises SandboxExecStreamError if the sandbox reports a terminal error.
        """
        resolved_owner_id = self._resolve_owner_id(owner_id)
        return self.api.exec_stream(sandbox_id, command, resolved_owner_id)

    async def copy_from(
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
        return await self.api.download_file(
            sandbox_id,
            normalize_remote_path(remote_path),
            os.fspath(local_path),
            resolved_owner_id,
        )


class SnapshotClient:
    """Snapshots of sandboxes, accessed via ``SandboxClient.snapshots``."""

    def __init__(self, sandboxes: SandboxClient):
        self._sandboxes = sandboxes

    async def create(
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
        snapshot = await self._sandboxes.api.create_snapshot(
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
            return available or await self.wait_until_available(
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

    async def from_id(
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
        return await self._sandboxes.api.get_snapshot(
            sandbox_group_id, snapshot_id, self._sandboxes._optional_owner_id(owner_id)
        )

    async def wait_until_available(
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

        return await _wait.apoll_until(
            lambda: self._sandboxes.api.get_snapshot(
                sandbox_group_id, snapshot_id, resolved_owner_id
            ),
            _wait.available_snapshot,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            timeout_error=timeout_error,
        )

    async def list(
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
        return await self._sandboxes.api.list_snapshots(
            resolved_owner_id, sandbox_group_id, status, cursor, limit
        )

    async def delete(
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
        await self._sandboxes.api.delete_snapshot(
            sandbox_group_id, snapshot_id, self._sandboxes._optional_owner_id(owner_id)
        )


class ImageClient:
    """Images that sandboxes start from, accessed via ``SandboxClient.images``."""

    def __init__(self, sandboxes: SandboxClient):
        self._sandboxes = sandboxes

    async def import_(
        self,
        *,
        sandbox_group_id: str,
        name: str,
        source: str,
        registry_credentials: RegistryCredentials | Mapping[str, str] | None = None,
    ) -> Image:
        """Start importing an OCI image so sandboxes can start from it.

        source is an image by tag or digest, like
        ``ghcr.io/acme/agent-runtime:v1``. It must be linux/amd64. name
        identifies the image and is reused across its versions, so a sandbox
        created with image=name starts from the newest one that succeeded.
        registry_credentials pulls source from a private registry, as a
        RegistryCredentials or a mapping with username and password keys.

        The image is returned before the import finishes; call
        wait_until_ready to wait for it. Importing a name and digest the group
        already has, or is importing, returns that image instead of starting
        another. Raises RateLimitError when the group has too many imports in
        progress.
        """
        return await self._sandboxes.api.import_image(
            sandbox_group_id, name, source, registry_credentials
        )

    async def from_id(self, *, sandbox_group_id: str, image_id: str) -> Image:
        """Fetch an image by id.

        Raises ImageNotFoundError if the image does not exist or belongs to
        another sandbox group.
        """
        return await self._sandboxes.api.get_image(sandbox_group_id, image_id)

    async def wait_until_ready(
        self,
        *,
        sandbox_group_id: str,
        image_id: str,
        timeout_seconds: float = _wait.DEFAULT_IMAGE_TIMEOUT_SECONDS,
        interval_seconds: float = _wait.DEFAULT_INTERVAL_SECONDS,
    ) -> Image:
        """Wait until the image has succeeded, so sandboxes can start from it.

        Checks the status every interval_seconds, doubling the delay after each
        check up to 2 seconds. timeout_seconds bounds the whole wait, including
        status checks. Raises ImageFailedError, with the API's reason, as soon
        as the import fails, and ImageWaitTimeoutError after timeout_seconds.
        Errors from a status check, such as ImageNotFoundError, propagate
        unchanged.
        """

        def timeout_error(last: Image | None) -> ImageWaitTimeoutError:
            return ImageWaitTimeoutError(
                f"timed out waiting for image {image_id} to be ready",
                image_id=image_id,
                timeout_seconds=timeout_seconds,
                last_status=last.status if last else None,
            )

        return await _wait.apoll_until(
            lambda: self._sandboxes.api.get_image(sandbox_group_id, image_id),
            _wait.ready_image,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            timeout_error=timeout_error,
        )


class BuildClient:
    """Deprecated: use ``SandboxClient.images``."""

    def __init__(self, sandboxes: SandboxClient):
        self._sandboxes = sandboxes

    async def create(
        self,
        *,
        sandbox_group_id: str,
        name: str,
        source_image: str,
        registry_credential: RegistryCredentials | None = None,
    ) -> Image:
        """Deprecated: use images.import_."""
        warnings.warn(
            "builds.create is deprecated; use images.import_",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self._sandboxes.api.import_image(
            sandbox_group_id, name, source_image, registry_credential
        )

    async def from_id(self, *, sandbox_group_id: str, build_id: str) -> Image:
        """Deprecated: use images.from_id."""
        warnings.warn(
            "builds.from_id is deprecated; use images.from_id",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self._sandboxes.api.get_image(sandbox_group_id, build_id)
