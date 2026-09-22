# Auto-generated sync version. Do not edit — run scripts/unasync.py instead.

"""Typed wrapper over the generated public_api sandbox endpoints."""

from __future__ import annotations

import json
import os
import posixpath
import stat
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, TypeVar

import httpx

from render.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
)
from render.client.util_sync import (
    handle_api_error,
    handle_http_errors,
    handle_httpx_exception,
    request_errors,
)
from render.experimental.sandbox._tar import (
    close_content,
    iter_file,
    iter_tar_gzip,
    stat_path,
)
from render.experimental.sandbox.errors import (
    SandboxDownloadError,
    SandboxExecError,
    SandboxExecStreamError,
    SandboxFileNotFoundError,
    SandboxNotFoundError,
    SnapshotNotFoundError,
    SnapshotNotReadyError,
    SnapshotPlanMismatchError,
)
from render.experimental.sandbox.files import (
    PartialDownload,
    check_content_encoding,
    disposition_filename,
    media_type,
    parent_dir,
    prepare_extract_dir,
    resolve_file_dest,
    run_blocking,
)
from render.experimental.sandbox.types import (
    Sandbox,
    SandboxExecEvent,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxGroup,
    SandboxGroupList,
    SandboxList,
    Snapshot,
    SnapshotList,
)
from render.public_api.api.sandboxes import (
    create_sandbox,
    create_sandbox_snapshot,
    delete_sandbox_snapshot,
    list_sandbox_groups,
    list_sandbox_snapshots,
    list_sandboxes,
    retrieve_sandbox,
    retrieve_sandbox_snapshot,
    terminate_sandbox,
)
from render.public_api.models.error import Error
from render.public_api.models.sandbox import Sandbox as GeneratedSandbox
from render.public_api.models.sandbox_group import SandboxGroup as GeneratedSandboxGroup
from render.public_api.models.sandbox_group_with_cursor import SandboxGroupWithCursor
from render.public_api.models.sandbox_network_policy import SandboxNetworkPolicy
from render.public_api.models.sandbox_network_policy_default import (
    SandboxNetworkPolicyDefault,
)
from render.public_api.models.sandbox_plan import SandboxPlan
from render.public_api.models.sandbox_post import SandboxPOST
from render.public_api.models.sandbox_post_env import SandboxPOSTEnv
from render.public_api.models.sandbox_snapshot import (
    SandboxSnapshot as GeneratedSandboxSnapshot,
)
from render.public_api.models.sandbox_snapshot_kind import SandboxSnapshotKind
from render.public_api.models.sandbox_snapshot_post import SandboxSnapshotPOST
from render.public_api.models.sandbox_snapshot_status import SandboxSnapshotStatus
from render.public_api.models.sandbox_snapshot_with_cursor import (
    SandboxSnapshotWithCursor,
)
from render.public_api.models.sandbox_status import SandboxStatus
from render.public_api.models.sandbox_with_cursor import SandboxWithCursor
from render.public_api.types import UNSET, Response, Unset

if TYPE_CHECKING:
    from render.public_api.client import AuthenticatedClient, Client


# The code the sandbox agent sends in a 404 body when the remote path is missing.
_FILE_NOT_FOUND_CODE = "file_not_found"
_SNAPSHOT_NOT_FOUND_CODE = "snapshot_not_found"
_SNAPSHOT_NOT_READY_CODES = frozenset({"snapshot_creating", "snapshot_not_available"})
_SNAPSHOT_PLAN_MISMATCH_CODE = "snapshot_plan_mismatch"

# Aliased at module scope so the annotations on the _api_call methods resolve
# the builtin list, not the SyncSandboxApi.list method that shadows it in the class body.
_SandboxWithCursorList = list[SandboxWithCursor]
_SandboxStatusList = list[SandboxStatus]
_SandboxGroupWithCursorList = list[SandboxGroupWithCursor]
_SandboxSnapshotWithCursorList = list[SandboxSnapshotWithCursor]
_SandboxSnapshotStatusList = list[SandboxSnapshotStatus]

_T = TypeVar("_T")
_StatusEnum = TypeVar("_StatusEnum", bound=Enum)

# File transfer content types. The content type states intent and nothing else:
# a single file travels as octet-stream and a directory as an x-tar archive the
# server extracts, with Content-Encoding carrying wire compression separately.
_CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
_CONTENT_TYPE_TAR = "application/x-tar"


def _set_or_none(value: _T | Unset | None) -> _T | None:
    return None if isinstance(value, Unset) else value


def _to_sandbox(model: GeneratedSandbox) -> Sandbox:
    return Sandbox(
        id=model.id,
        status=model.status.value,
        plan=model.plan.value,
        network_policy=model.network_policy.default.value,
        region=model.region,
        timeout_seconds=model.timeout_seconds,
        created_at=model.created_at,
        terminated_at=_set_or_none(model.terminated_at),
    )


def _to_sandbox_group(model: GeneratedSandboxGroup) -> SandboxGroup:
    return SandboxGroup(
        id=model.id,
        owner_id=model.owner_id,
        name=model.name,
        region=model.region,
        is_default=model.is_default,
        concurrency_limit=model.concurrency_limit,
        created_at=model.created_at,
        updated_at=model.updated_at,
        environment_id=_set_or_none(model.environment_id),
    )


def _to_snapshot(model: GeneratedSandboxSnapshot) -> Snapshot:
    return Snapshot(
        id=model.id,
        sandbox_group_id=model.sandbox_group_id,
        source_sandbox_id=model.source_sandbox_id,
        kind=model.kind.value,
        status=model.status.value,
        plan=model.plan.value,
        requested_at=model.requested_at,
        name=_set_or_none(model.name),
        captured_at=_set_or_none(model.captured_at),
        expires_at=model.expires_at,
        size_bytes=_set_or_none(model.size_bytes),
        error=_set_or_none(model.error),
    )


def _normalize_statuses(
    status: str | Sequence[str] | None, status_type: type[_StatusEnum]
) -> list[_StatusEnum]:
    if status is None:
        return []
    values = [status] if isinstance(status, str) else list(status)
    return [status_type(value) for value in values]


@dataclass(frozen=True)
class _ErrorBody:
    message: str | None = None
    code: str | None = None


def _error_body(body: bytes | str) -> _ErrorBody:
    try:
        payload = json.loads(body)
    except ValueError:
        return _ErrorBody()
    if not isinstance(payload, dict):
        return _ErrorBody()
    message = payload.get("message")
    code = payload.get("code")
    return _ErrorBody(
        message=message if isinstance(message, str) else None,
        code=code if isinstance(code, str) else None,
    )


def _handle_snapshot_api_error(
    response: Response[Any],
    snapshot_id: str,
    operation: str,
    *,
    path_names_snapshot: bool = True,
) -> None:
    if response.status_code == 404:
        code = _error_body(response.content).code
        if path_names_snapshot or code == _SNAPSHOT_NOT_FOUND_CODE:
            raise SnapshotNotFoundError(f"snapshot {snapshot_id} not found", code=code)
    if response.status_code == 409:
        error = _error_body(response.content)
        message = f"{operation} failed"
        if error.message:
            message = f"{message}: {error.message}"
        if error.code in _SNAPSHOT_NOT_READY_CODES:
            raise SnapshotNotReadyError(message, code=error.code)
        if error.code == _SNAPSHOT_PLAN_MISMATCH_CODE:
            raise SnapshotPlanMismatchError(message, code=error.code)
    handle_api_error(response, operation)


class SyncSandboxApi:
    """Typed wrapper over the generated sandbox endpoints."""

    def __init__(self, client: AuthenticatedClient | Client):
        self.client = client

    def create(
        self,
        owner_id: str,
        plan: str | None,
        timeout_seconds: int | None,
        network_policy: str | None,
        region: str | None,
        env: dict[str, str] | None,
        snapshot_id: str | None,
        snapshot_name: str | None,
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
        if snapshot_id is not None:
            body.snapshot_id = snapshot_id
        if snapshot_name is not None:
            body.snapshot_name = snapshot_name

        with request_errors("create sandbox"):
            response = create_sandbox.sync_detailed(client=self.client, body=body)
        snapshot_ref = snapshot_id if snapshot_id is not None else snapshot_name
        if snapshot_ref is None:
            handle_api_error(response, "create sandbox")
        else:
            _handle_snapshot_api_error(
                response, snapshot_ref, "create sandbox", path_names_snapshot=False
            )
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to create sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    def get(self, sandbox_id: str, owner_id: str) -> Sandbox:
        with request_errors("retrieve sandbox"):
            response = retrieve_sandbox.sync_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        handle_api_error(response, "retrieve sandbox")
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to retrieve sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    def list(
        self,
        owner_id: str,
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
    ) -> SandboxList:
        statuses = _normalize_statuses(status, SandboxStatus)
        response = self._list_api_call(owner_id, statuses, cursor, limit)
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list sandboxes: unexpected response type")
        sandboxes = [_to_sandbox(item.sandbox) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SandboxList(sandboxes=sandboxes, next_cursor=next_cursor)

    @handle_http_errors("list sandboxes")
    def _list_api_call(
        self,
        owner_id: str,
        statuses: _SandboxStatusList,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxWithCursorList]:
        return list_sandboxes.sync_detailed(
            client=self.client,
            owner_id=owner_id,
            status=statuses or UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    def list_groups(self, owner_id: str) -> SandboxGroupList:
        response = self._list_groups_api_call(owner_id)
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list sandbox groups: unexpected response type")
        groups = [_to_sandbox_group(item.sandbox_group) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SandboxGroupList(groups=groups, next_cursor=next_cursor)

    @handle_http_errors("list sandbox groups")
    def _list_groups_api_call(
        self, owner_id: str
    ) -> Response[Error | _SandboxGroupWithCursorList]:
        return list_sandbox_groups.sync_detailed(
            client=self.client,
            owner_id=owner_id,
        )

    def terminate(self, sandbox_id: str, owner_id: str) -> None:
        with request_errors("terminate sandbox"):
            response = terminate_sandbox.sync_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        handle_api_error(response, "terminate sandbox")

    def create_snapshot(
        self,
        sandbox_id: str,
        kind: str,
        name: str | None,
        expires_at: datetime | None,
        owner_id: str | Unset,
    ) -> Snapshot:
        body = SandboxSnapshotPOST(
            kind=SandboxSnapshotKind(kind),
            name=name if name is not None else UNSET,
            expires_at=expires_at if expires_at is not None else UNSET,
        )
        with request_errors("create snapshot"):
            response = create_sandbox_snapshot.sync_detailed(
                sandbox_id, client=self.client, body=body, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        handle_api_error(response, "create snapshot")
        if not isinstance(response.parsed, GeneratedSandboxSnapshot):
            raise RenderError("Failed to create snapshot: unexpected response type")
        return _to_snapshot(response.parsed)

    def get_snapshot(
        self, sandbox_group_id: str, snapshot_id: str, owner_id: str | Unset
    ) -> Snapshot:
        with request_errors("retrieve snapshot"):
            response = retrieve_sandbox_snapshot.sync_detailed(
                sandbox_group_id, snapshot_id, client=self.client, owner_id=owner_id
            )
        _handle_snapshot_api_error(response, snapshot_id, "retrieve snapshot")
        if not isinstance(response.parsed, GeneratedSandboxSnapshot):
            raise RenderError("Failed to retrieve snapshot: unexpected response type")
        return _to_snapshot(response.parsed)

    def list_snapshots(
        self,
        owner_id: str,
        sandbox_group_id: str,
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
    ) -> SnapshotList:
        statuses = _normalize_statuses(status, SandboxSnapshotStatus)
        response = self._list_snapshots_api_call(
            sandbox_group_id, owner_id, statuses, cursor, limit
        )
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list snapshots: unexpected response type")
        snapshots = [_to_snapshot(item.snapshot) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SnapshotList(snapshots=snapshots, next_cursor=next_cursor)

    @handle_http_errors("list snapshots")
    def _list_snapshots_api_call(
        self,
        sandbox_group_id: str,
        owner_id: str,
        statuses: _SandboxSnapshotStatusList,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxSnapshotWithCursorList]:
        return list_sandbox_snapshots.sync_detailed(
            sandbox_group_id,
            client=self.client,
            owner_id=owner_id,
            status=statuses or UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    def delete_snapshot(
        self, sandbox_group_id: str, snapshot_id: str, owner_id: str | Unset
    ) -> None:
        with request_errors("delete snapshot"):
            response = delete_sandbox_snapshot.sync_detailed(
                sandbox_group_id, snapshot_id, client=self.client, owner_id=owner_id
            )
        _handle_snapshot_api_error(response, snapshot_id, "delete snapshot")

    def _mint_run_token(
        self, sandbox_id: str, owner_id: str, operation: str, command: str
    ) -> dict[str, Any]:
        # Command rides along so the API keeps a sanitized copy for the audit trail.
        api_client = self.client.get_httpx_client()
        try:
            response = api_client.post(
                f"/sandboxes/{sandbox_id}/runs/{operation}/token",
                params={"ownerId": owner_id},
                json={"command": command},
            )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "connect sandbox run")
        if response.status_code >= 400:
            _raise_sandbox_http_error(
                sandbox_id, response.status_code, response.text, "exec"
            )
        return response.json()

    def _mint_file_token(
        self, sandbox_id: str, owner_id: str, operation: str, path: str
    ) -> dict[str, Any]:
        api_client = self.client.get_httpx_client()
        try:
            response = api_client.post(
                f"/sandboxes/{sandbox_id}/files/{operation}/token",
                params={"ownerId": owner_id, "path": path},
            )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "connect sandbox files")
        if response.status_code >= 400:
            _raise_sandbox_http_error(
                sandbox_id, response.status_code, response.text, operation
            )
        return response.json()

    def upload(
        self,
        sandbox_id: str,
        local_path: str | os.PathLike[str],
        remote_path: str,
        owner_id: str,
    ) -> None:
        source = Path(local_path)
        # The server rejects any path it would have to clean, so clean it here
        # instead of turning a trailing slash into a 400. The CLI does the same
        # before minting, which keeps the two clients in step. Guard the empty
        # path first: normpath turns it into ".", which would quietly copy to
        # the home directory instead of failing.
        if not remote_path:
            raise ValueError("remote_path is required")
        remote_path = posixpath.normpath(remote_path)
        # stat, not lstat: a symlinked directory uploads as the directory it
        # points at. Statting before the mint also keeps a missing local path
        # from spending a token.
        info = stat_path(source)
        if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            # Opening a fifo blocks until a writer appears, which may be never,
            # and that open would block the event loop rather than time out.
            # Refuse before the mint so a bad path does not spend a token.
            raise ValueError(
                f"{source} is not a file or directory; "
                "sockets, fifos and devices cannot be copied to a sandbox"
            )
        connection = self._mint_file_token(sandbox_id, owner_id, "upload", remote_path)

        headers = {"Authorization": f"Bearer {connection['token']}"}
        content: Iterator[bytes]
        if stat.S_ISDIR(info.st_mode):
            headers["Content-Type"] = _CONTENT_TYPE_TAR
            # The archive's length is not known until it has been produced, so
            # the body goes out chunked. gzip is the wire encoding only: the
            # server gunzips it and extracts the tar underneath.
            headers["Content-Encoding"] = "gzip"
            content = iter_tar_gzip(source)
        else:
            headers["Content-Type"] = _CONTENT_TYPE_OCTET_STREAM
            # An explicit length keeps httpx from sending an iterator body
            # chunked, and lets the sandbox size the write up front.
            headers["Content-Length"] = str(info.st_size)
            content = iter_file(source)

        # Keep the connect timeout, but let a large upload take as long as it
        # takes, as the object client does.
        timeout = httpx.Timeout(5.0, read=None, write=None)
        try:
            with httpx.Client(timeout=timeout) as proxy_client:
                response = proxy_client.request(
                    connection["method"],
                    connection["uri"],
                    headers=headers,
                    content=content,
                )
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "upload to sandbox")
        finally:
            # httpx closes the body on today's failure paths, but that is its
            # internals, not a contract. Closing here is what actually
            # guarantees the archive producer stops when a request dies early.
            close_content(content)
        # Any 2xx, not just the 204 the sandbox sends today: the API deploys
        # ahead of the SDK, so pinning the exact code would break on a benign
        # change.
        if not 200 <= response.status_code < 300:
            _raise_sandbox_http_error(
                sandbox_id, response.status_code, response.text, "upload"
            )

    def download_file(
        self, sandbox_id: str, remote_path: str, local_path: str, owner_id: str
    ) -> str:
        """Copy remote_path out of the sandbox and return the local path written.

        A directory arrives as an x-tar archive and is extracted under
        local_path; anything else is written as a single file.
        """
        connection = self._mint_file_token(
            sandbox_id, owner_id, "download", remote_path
        )
        headers = {
            "Authorization": f"Bearer {connection['token']}",
            # Ask only for the coding httpx undoes for us. Left to itself it
            # also advertises deflate, and br/zstd when those are installed,
            # any of which would arrive as a body we refuse to write.
            "Accept-Encoding": "gzip",
        }
        # read bounds the wait for the next chunk, not the transfer, so a large
        # download still has as long as it needs while a body that stops
        # arriving fails instead of hanging. Same budget as exec_stream.
        timeout = httpx.Timeout(5.0, read=45.0, write=None)
        try:
            with (
                httpx.Client(timeout=timeout) as proxy_client,
                proxy_client.stream(
                    connection["method"], connection["uri"], headers=headers
                ) as response,
            ):
                if response.status_code >= 400:
                    body = (response.read()).decode("utf-8", errors="replace")
                    _raise_sandbox_http_error(
                        sandbox_id, response.status_code, body, "download"
                    )
                check_content_encoding(response.headers.get("content-encoding", ""))

                if media_type(response.headers.get("content-type", "")) == (
                    _CONTENT_TYPE_TAR
                ):
                    # The archive is spooled next to the destination rather than
                    # extracted as it arrives: feeding tarfile from an async
                    # stream would take a thread to bridge, and the memory
                    # footprint is the same either way.
                    with PartialDownload(prepare_extract_dir(local_path)) as partial:
                        for chunk in response.iter_bytes():
                            partial.write(chunk)
                        run_blocking(partial.extract, local_path)
                    return local_path

                dest = resolve_file_dest(
                    local_path,
                    disposition_filename(
                        response.headers.get("content-disposition", "")
                    ),
                    remote_path,
                )
                with PartialDownload(parent_dir(dest)) as partial:
                    for chunk in response.iter_bytes():
                        partial.write(chunk)
                    return run_blocking(partial.commit, dest)
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "download sandbox file")
        except OSError as exc:
            # Spooling, extracting and renaming all touch the local disk, and a
            # bare OSError from any of them tells a caller nothing about which
            # download failed.
            raise SandboxDownloadError(
                f"could not write the download to {local_path}: {exc}"
            ) from exc

    def exec_stream(
        self, sandbox_id: str, command: str, owner_id: str, operation: str = "stream"
    ) -> Iterator[SandboxExecEvent]:
        connection = self._mint_run_token(sandbox_id, owner_id, operation, command)
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
            with (
                httpx.Client(timeout=timeout) as proxy_client,
                proxy_client.stream(
                    method, uri, headers=headers, json={"command": command}
                ) as response,
            ):
                if response.status_code >= 400:
                    body = (response.read()).decode("utf-8", errors="replace")
                    _raise_sandbox_http_error(
                        sandbox_id, response.status_code, body, "exec"
                    )
                for name, data in _iter_sse_events(response.iter_lines()):
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


def _load_event(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise SandboxExecError(
            f"failed to parse sandbox exec event data: {data}"
        ) from exc


def _raise_sandbox_http_error(
    sandbox_id: str, status_code: int, body: str, action: str
) -> NoReturn:
    message = f"{action} failed with status {status_code}"
    if body:
        message = f"{message}: {body}"
    if status_code == 404:
        # The agent 404s a missing remote path with this code, and the sandbox
        # is alive when it does. Any other 404 is the sandbox itself being gone,
        # including the one the mint endpoint returns.
        if _error_body(body).code == _FILE_NOT_FOUND_CODE:
            raise SandboxFileNotFoundError(message)
        raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
    if status_code == 429:
        raise RateLimitError(message)
    if 400 <= status_code < 500:
        raise ClientError(message)
    raise ServerError(message)


def _iter_sse_events(
    lines: Iterator[str],
) -> Iterator[tuple[str, str]]:
    event_name = ""
    data_parts: list[str] = []
    for raw in lines:
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
