"""Typed wrapper over the generated public_api sandbox endpoints."""

from __future__ import annotations

import json
import os
import posixpath
import stat
from collections.abc import AsyncIterator, Sequence
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

import httpx

from render.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
)
from render.client.util import (
    handle_api_error,
    handle_http_errors,
    handle_httpx_exception,
)
from render.experimental.sandbox._tar import (
    aclose_content,
    aiter_file,
    aiter_tar_gzip,
    astat_path,
)
from render.experimental.sandbox.errors import (
    SandboxDownloadError,
    SandboxExecError,
    SandboxExecStreamError,
    SandboxFileNotFoundError,
    SandboxNotFoundError,
)
from render.experimental.sandbox.files import (
    PartialDownload,
    arun_blocking,
    check_content_encoding,
    disposition_filename,
    media_type,
    parent_dir,
    prepare_extract_dir,
    resolve_file_dest,
)
from render.experimental.sandbox.types import (
    Sandbox,
    SandboxExecEvent,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxList,
)
from render.public_api.api.sandboxes import (
    create_sandbox,
    list_sandboxes,
    retrieve_sandbox,
    terminate_sandbox,
)
from render.public_api.models.error import Error
from render.public_api.models.sandbox import Sandbox as GeneratedSandbox
from render.public_api.models.sandbox_network_policy import SandboxNetworkPolicy
from render.public_api.models.sandbox_network_policy_default import (
    SandboxNetworkPolicyDefault,
)
from render.public_api.models.sandbox_plan import SandboxPlan
from render.public_api.models.sandbox_post import SandboxPOST
from render.public_api.models.sandbox_post_env import SandboxPOSTEnv
from render.public_api.models.sandbox_status import SandboxStatus
from render.public_api.models.sandbox_with_cursor import SandboxWithCursor
from render.public_api.types import UNSET, Response

if TYPE_CHECKING:
    from render.public_api.client import AuthenticatedClient, Client


# The code the sandbox agent sends in a 404 body when the remote path is missing.
_FILE_NOT_FOUND_CODE = "file_not_found"

# Aliased at module scope so the annotations on _list_api_call resolve the
# builtin list, not the SandboxApi.list method that shadows it in the class body.
_SandboxWithCursorList = list[SandboxWithCursor]
_SandboxStatusList = list[SandboxStatus]

# File transfer content types. The content type states intent and nothing else:
# a single file travels as octet-stream and a directory as an x-tar archive the
# server extracts, with Content-Encoding carrying wire compression separately.
_CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
_CONTENT_TYPE_TAR = "application/x-tar"


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


def _normalize_statuses(status: str | Sequence[str] | None) -> list[SandboxStatus]:
    if status is None:
        return []
    values = [status] if isinstance(status, str) else list(status)
    return [SandboxStatus(value) for value in values]


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
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
    ) -> SandboxList:
        statuses = _normalize_statuses(status)
        response = await self._list_api_call(owner_id, statuses, cursor, limit)
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
        statuses: _SandboxStatusList,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxWithCursorList]:
        return await list_sandboxes.asyncio_detailed(
            client=self.client,
            owner_id=[owner_id],
            status=statuses or UNSET,
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
        self, sandbox_id: str, owner_id: str, operation: str, command: str
    ) -> dict[str, Any]:
        # Command rides along so the API keeps a sanitized copy for the audit trail.
        api_client = self.client.get_async_httpx_client()
        try:
            response = await api_client.post(
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

    async def _mint_file_token(
        self, sandbox_id: str, owner_id: str, operation: str, path: str
    ) -> dict[str, Any]:
        api_client = self.client.get_async_httpx_client()
        try:
            response = await api_client.post(
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

    async def upload(
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
        info = await astat_path(source)
        if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            # Opening a fifo blocks until a writer appears, which may be never,
            # and that open would block the event loop rather than time out.
            # Refuse before the mint so a bad path does not spend a token.
            raise ValueError(
                f"{source} is not a file or directory; "
                "sockets, fifos and devices cannot be copied to a sandbox"
            )
        connection = await self._mint_file_token(
            sandbox_id, owner_id, "upload", remote_path
        )

        headers = {"Authorization": f"Bearer {connection['token']}"}
        content: AsyncIterator[bytes]
        if stat.S_ISDIR(info.st_mode):
            headers["Content-Type"] = _CONTENT_TYPE_TAR
            # The archive's length is not known until it has been produced, so
            # the body goes out chunked. gzip is the wire encoding only: the
            # server gunzips it and extracts the tar underneath.
            headers["Content-Encoding"] = "gzip"
            content = aiter_tar_gzip(source)
        else:
            headers["Content-Type"] = _CONTENT_TYPE_OCTET_STREAM
            # An explicit length keeps httpx from sending an iterator body
            # chunked, and lets the sandbox size the write up front.
            headers["Content-Length"] = str(info.st_size)
            content = aiter_file(source)

        # Keep the connect timeout, but let a large upload take as long as it
        # takes, as the object client does.
        timeout = httpx.Timeout(5.0, read=None, write=None)
        try:
            async with httpx.AsyncClient(timeout=timeout) as proxy_client:
                response = await proxy_client.request(
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
            await aclose_content(content)
        # Any 2xx, not just the 204 the sandbox sends today: the API deploys
        # ahead of the SDK, so pinning the exact code would break on a benign
        # change.
        if not 200 <= response.status_code < 300:
            _raise_sandbox_http_error(
                sandbox_id, response.status_code, response.text, "upload"
            )

    async def download_file(
        self, sandbox_id: str, remote_path: str, local_path: str, owner_id: str
    ) -> str:
        """Copy remote_path out of the sandbox and return the local path written.

        A directory arrives as an x-tar archive and is extracted under
        local_path; anything else is written as a single file.
        """
        connection = await self._mint_file_token(
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
            async with (
                httpx.AsyncClient(timeout=timeout) as proxy_client,
                proxy_client.stream(
                    connection["method"], connection["uri"], headers=headers
                ) as response,
            ):
                if response.status_code >= 400:
                    body = (await response.aread()).decode("utf-8", errors="replace")
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
                        async for chunk in response.aiter_bytes():
                            partial.write(chunk)
                        await arun_blocking(partial.extract, local_path)
                    return local_path

                dest = resolve_file_dest(
                    local_path,
                    disposition_filename(
                        response.headers.get("content-disposition", "")
                    ),
                    remote_path,
                )
                with PartialDownload(parent_dir(dest)) as partial:
                    async for chunk in response.aiter_bytes():
                        partial.write(chunk)
                    return await arun_blocking(partial.commit, dest)
        except httpx.RequestError as exc:
            handle_httpx_exception(exc, "download sandbox file")
        except OSError as exc:
            # Spooling, extracting and renaming all touch the local disk, and a
            # bare OSError from any of them tells a caller nothing about which
            # download failed.
            raise SandboxDownloadError(
                f"could not write the download to {local_path}: {exc}"
            ) from exc

    async def exec_stream(
        self, sandbox_id: str, command: str, owner_id: str, operation: str = "stream"
    ) -> AsyncIterator[SandboxExecEvent]:
        connection = await self._mint_run_token(
            sandbox_id, owner_id, operation, command
        )
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
                    _raise_sandbox_http_error(
                        sandbox_id, response.status_code, body, "exec"
                    )
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


def _file_error_code(body: str) -> str:
    """The ``code`` of a sandbox agent error body, or "" if it has none."""
    try:
        payload = json.loads(body)
    except ValueError:
        return ""
    code = payload.get("code") if isinstance(payload, dict) else None
    return code if isinstance(code, str) else ""


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
        if _file_error_code(body) == _FILE_NOT_FOUND_CODE:
            raise SandboxFileNotFoundError(message)
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
