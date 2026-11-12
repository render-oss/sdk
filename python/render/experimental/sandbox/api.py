"""Typed wrapper over the generated public_api sandbox endpoints."""

from __future__ import annotations

import json
import os
import stat
from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass
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
from render.client.util import (
    handle_api_error,
    handle_http_errors,
    handle_httpx_exception,
    request_errors,
)
from render.experimental.sandbox._tar import (
    aclose_content,
    aiter_file,
    aiter_tar_gzip,
    astat_path,
)
from render.experimental.sandbox.errors import (
    CredentialNotFoundError,
    ImageNotFoundError,
    ImageNotReadyError,
    SandboxDownloadError,
    SandboxEndedError,
    SandboxExecError,
    SandboxExecStreamError,
    SandboxFileNotFoundError,
    SandboxGroupDefaultNotDeletableError,
    SandboxGroupSuspendedError,
    SandboxNotFoundError,
    SnapshotNotFoundError,
    SnapshotNotReadyError,
    SnapshotPlanMismatchError,
)
from render.experimental.sandbox.files import (
    PartialDownload,
    arun_blocking,
    check_content_encoding,
    disposition_filename,
    media_type,
    normalize_remote_path,
    parent_dir,
    prepare_extract_dir,
    resolve_file_dest,
)
from render.experimental.sandbox.types import (
    Credential,
    CredentialInjection,
    CredentialVersion,
    EgressRule,
    Image,
    ImageList,
    ImageSource,
    NetworkPolicy,
    RegistryCredentials,
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
    create_sandbox_build,
    create_sandbox_group,
    create_sandbox_group_credential,
    create_sandbox_snapshot,
    delete_sandbox_group,
    delete_sandbox_group_credential,
    delete_sandbox_snapshot,
    list_sandbox_builds,
    list_sandbox_group_credential_versions,
    list_sandbox_group_credentials,
    list_sandbox_groups,
    list_sandbox_snapshots,
    list_sandboxes,
    restore_sandbox_group_credential,
    retrieve_sandbox,
    retrieve_sandbox_build,
    retrieve_sandbox_group,
    retrieve_sandbox_group_credential,
    retrieve_sandbox_snapshot,
    set_default_sandbox_group,
    terminate_sandbox,
    update_sandbox_group,
    update_sandbox_group_credential,
)
from render.public_api.models.error import Error
from render.public_api.models.sandbox import Sandbox as GeneratedSandbox
from render.public_api.models.sandbox_build import SandboxBuild as GeneratedSandboxBuild
from render.public_api.models.sandbox_build_post import SandboxBuildPOST
from render.public_api.models.sandbox_build_post_registry_credential import (
    SandboxBuildPOSTRegistryCredential,
)
from render.public_api.models.sandbox_build_status import SandboxBuildStatus
from render.public_api.models.sandbox_build_with_cursor import SandboxBuildWithCursor
from render.public_api.models.sandbox_credential import (
    SandboxCredential as GeneratedCredential,
)
from render.public_api.models.sandbox_credential_create import SandboxCredentialCreate
from render.public_api.models.sandbox_credential_injection import (
    SandboxCredentialInjection,
)
from render.public_api.models.sandbox_credential_injection_type import (
    SandboxCredentialInjectionType,
)
from render.public_api.models.sandbox_credential_restore import (
    SandboxCredentialRestore,
)
from render.public_api.models.sandbox_credential_update import SandboxCredentialUpdate
from render.public_api.models.sandbox_credential_version import (
    SandboxCredentialVersion,
)
from render.public_api.models.sandbox_egress_rule import SandboxEgressRule
from render.public_api.models.sandbox_egress_rule_protocol import (
    SandboxEgressRuleProtocol,
)
from render.public_api.models.sandbox_group import SandboxGroup as GeneratedSandboxGroup
from render.public_api.models.sandbox_group_patch import SandboxGroupPATCH
from render.public_api.models.sandbox_group_post import SandboxGroupPOST
from render.public_api.models.sandbox_group_with_cursor import SandboxGroupWithCursor
from render.public_api.models.sandbox_network_policy import (
    SandboxNetworkPolicy as GeneratedNetworkPolicy,
)
from render.public_api.models.sandbox_network_policy_post import (
    SandboxNetworkPolicyPOST,
)
from render.public_api.models.sandbox_network_policy_type import (
    SandboxNetworkPolicyType,
)
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


# The code the API sends in a 409 body when the sandbox has ended.
_SANDBOX_NOT_RUNNING_CODE = "sandbox_not_running"

# The code the sandbox agent sends in a 404 body when the remote path is missing.
_FILE_NOT_FOUND_CODE = "file_not_found"
_SNAPSHOT_NOT_FOUND_CODE = "snapshot_not_found"
# The API still calls images builds, in its paths and error codes.
_IMAGE_NOT_FOUND_CODE = "build_not_found"
_CLIENT_ERRORS_BY_CODE: dict[str, type[ClientError]] = {
    "snapshot_creating": SnapshotNotReadyError,
    "snapshot_not_available": SnapshotNotReadyError,
    "snapshot_plan_mismatch": SnapshotPlanMismatchError,
    "build_not_succeeded": ImageNotReadyError,
    "default_sandbox_group_not_deletable": SandboxGroupDefaultNotDeletableError,
    "sandbox_group_suspended": SandboxGroupSuspendedError,
}

# Aliased at module scope so the annotations on the _api_call methods resolve
# the builtin list, not the SandboxApi.list method that shadows it in the class body.
_SandboxWithCursorList = list[SandboxWithCursor]
_SandboxStatusList = list[SandboxStatus]
_SandboxGroupWithCursorList = list[SandboxGroupWithCursor]
_SandboxSnapshotWithCursorList = list[SandboxSnapshotWithCursor]
_SandboxSnapshotStatusList = list[SandboxSnapshotStatus]
_SandboxBuildWithCursorList = list[SandboxBuildWithCursor]
_SandboxBuildStatusList = list[SandboxBuildStatus]
_CredentialList = list[Credential]
_CredentialVersionList = list[CredentialVersion]

_T = TypeVar("_T")
_StatusEnum = TypeVar("_StatusEnum", bound=Enum)

# File transfer content types. The content type states intent and nothing else:
# a single file travels as octet-stream and a directory as an x-tar archive the
# server extracts, with Content-Encoding carrying wire compression separately.
_CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
_CONTENT_TYPE_TAR = "application/x-tar"


def _set_or_none(value: _T | Unset | None) -> _T | None:
    return None if isinstance(value, Unset) else value


def _to_egress_rule(model: SandboxEgressRule) -> EgressRule:
    if isinstance(model.protocol, Unset):
        return EgressRule(domain=model.domain)
    return EgressRule(domain=model.domain, protocol=model.protocol.value)


def _to_network_policy(model: GeneratedNetworkPolicy) -> NetworkPolicy:
    rules = _set_or_none(model.rules) or []
    return NetworkPolicy(
        type=model.type_.value,
        rules=[_to_egress_rule(rule) for rule in rules],
    )


def _to_network_policy_post(policy: NetworkPolicy | str) -> SandboxNetworkPolicyPOST:
    if isinstance(policy, str):
        policy = NetworkPolicy(type=policy)
    body = SandboxNetworkPolicyPOST(type_=SandboxNetworkPolicyType(policy.type))
    if policy.type == "allow-list":
        body.rules = [
            SandboxEgressRule(
                domain=rule.domain, protocol=SandboxEgressRuleProtocol(rule.protocol)
            )
            for rule in policy.rules
        ]
    elif policy.rules:
        raise ValueError("rules are only allowed for an allow-list network policy")
    return body


def _to_sandbox(model: GeneratedSandbox) -> Sandbox:
    return Sandbox(
        id=model.id,
        sandbox_group_id=_set_or_none(model.sandbox_group_id),
        name=_set_or_none(model.name),
        status=model.status.value,
        plan=str(model.plan),
        network_policy=_to_network_policy(model.network_policy),
        region=model.region,
        timeout_seconds=model.timeout_seconds,
        idle_timeout_seconds=model.idle_timeout_seconds,
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
        plan=str(model.plan),
        requested_at=model.requested_at,
        name=_set_or_none(model.name),
        captured_at=_set_or_none(model.captured_at),
        expires_at=model.expires_at,
        size_bytes=_set_or_none(model.size_bytes),
        error=_set_or_none(model.error),
        ttl_seconds=_set_or_none(model.ttl_seconds),
    )


def _to_image(model: GeneratedSandboxBuild) -> Image:
    return Image(
        id=model.id,
        sandbox_group_id=model.sandbox_group_id,
        name=model.name,
        source=ImageSource(
            repository=model.source.repository,
            image=model.source.image,
            reference=model.source.reference,
        ),
        source_digest=model.source_digest,
        status=model.status.value,
        created_at=model.created_at,
        failure_reason=_set_or_none(model.failure_reason),
        finished_at=_set_or_none(model.finished_at),
    )


def _to_credential_injection(model: SandboxCredentialInjection) -> CredentialInjection:
    return CredentialInjection(
        type=model.type_.value,
        name=_set_or_none(model.name),
        template=_set_or_none(model.template),
    )


def _to_credential_injection_body(
    injection: CredentialInjection,
) -> SandboxCredentialInjection:
    return SandboxCredentialInjection(
        type_=SandboxCredentialInjectionType(injection.type),
        name=injection.name if injection.name is not None else UNSET,
        template=injection.template if injection.template is not None else UNSET,
    )


def _to_credential_version(model: SandboxCredentialVersion) -> CredentialVersion:
    return CredentialVersion(
        id=model.id,
        updated_at=model.updated_at,
        updated_by=model.updated_by,
        fingerprint=model.fingerprint,
        restored_from_version_id=_set_or_none(model.restored_from_version_id),
    )


def _to_credential(model: GeneratedCredential) -> Credential:
    version = _set_or_none(model.version)
    return Credential(
        id=model.id,
        domain=model.domain,
        enabled=model.enabled,
        methods=list(model.methods),
        paths=list(model.paths),
        injection=_to_credential_injection(model.injection),
        version=_to_credential_version(version) if version is not None else None,
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


def _raise_for_error_code(status_code: int, body: bytes | str, operation: str) -> None:
    if not 400 <= status_code < 500:
        return
    error = _error_body(body)
    error_type = _CLIENT_ERRORS_BY_CODE.get(error.code or "")
    if error_type is None:
        return
    message = f"{operation} failed"
    if error.message:
        message = f"{message}: {error.message}"
    raise error_type(message, code=error.code, status_code=status_code)


def _handle_sandbox_api_error(response: Response[Any], operation: str) -> None:
    _raise_for_error_code(response.status_code, response.content, operation)
    handle_api_error(response, operation)


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
    _handle_sandbox_api_error(response, operation)


def _handle_image_api_error(
    response: Response[Any], image_ref: str, operation: str
) -> None:
    if response.status_code == 404:
        code = _error_body(response.content).code
        if code == _IMAGE_NOT_FOUND_CODE:
            raise ImageNotFoundError(f"image {image_ref} not found", code=code)
    _handle_sandbox_api_error(response, operation)


def _string_list(values: Sequence[str]) -> list[str]:
    # A str is a Sequence[str], so list("POST") would split it into characters.
    return [values] if isinstance(values, str) else list(values)


def _handle_credential_api_error(
    response: Response[Any], not_found_message: str, operation: str
) -> None:
    # The API sends no code with a credential 404, and the same 404 for a
    # missing sandbox group, so only paths that name a credential use this.
    if response.status_code == 404:
        raise CredentialNotFoundError(
            not_found_message,
            code=_error_body(response.content).code,
            status_code=404,
        )
    _handle_sandbox_api_error(response, operation)


class SandboxApi:
    """Typed wrapper over the generated sandbox endpoints."""

    def __init__(self, client: AuthenticatedClient | Client):
        self.client = client

    async def create(
        self,
        owner_id: str,
        plan: str | None,
        timeout_seconds: int | None,
        idle_timeout_seconds: int | None,
        network_policy: NetworkPolicy | str | None,
        region: str | None,
        env: dict[str, str] | None,
        snapshot_id: str | None,
        snapshot_name: str | None,
        image_id: str | None = None,
        image_name: str | None = None,
        sandbox_group_id: str | None = None,
        name: str | None = None,
    ) -> Sandbox:
        body = SandboxPOST(owner_id=owner_id)
        if sandbox_group_id is not None:
            body.sandbox_group_id = sandbox_group_id
        if name is not None:
            body.name = name
        if plan is not None:
            body.plan = plan
        if timeout_seconds is not None:
            body.timeout_seconds = timeout_seconds
        if idle_timeout_seconds is not None:
            body.idle_timeout_seconds = idle_timeout_seconds
        if network_policy is not None:
            body.network_policy = _to_network_policy_post(network_policy)
        if env is not None:
            body.env = SandboxPOSTEnv.from_dict(env)
        if snapshot_id is not None:
            body.snapshot_id = snapshot_id
        if snapshot_name is not None:
            body.snapshot_name = snapshot_name
        if image_id is not None:
            body.build_id = image_id
        if image_name is not None:
            body.build_name = image_name

        with request_errors("create sandbox"):
            response = await create_sandbox.asyncio_detailed(
                client=self.client, body=body
            )
        snapshot_ref = snapshot_id if snapshot_id is not None else snapshot_name
        image_ref = image_id if image_id is not None else image_name
        if snapshot_ref is not None:
            _handle_snapshot_api_error(
                response, snapshot_ref, "create sandbox", path_names_snapshot=False
            )
        elif image_ref is not None:
            _handle_image_api_error(response, image_ref, "create sandbox")
        else:
            _handle_sandbox_api_error(response, "create sandbox")
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to create sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    async def get(self, sandbox_id: str, owner_id: str) -> Sandbox:
        with request_errors("retrieve sandbox"):
            response = await retrieve_sandbox.asyncio_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        _handle_sandbox_api_error(response, "retrieve sandbox")
        if not isinstance(response.parsed, GeneratedSandbox):
            raise RenderError("Failed to retrieve sandbox: unexpected response type")
        return _to_sandbox(response.parsed)

    async def list(
        self,
        owner_id: str,
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
        sandbox_group_id: str | None = None,
        name: str | None = None,
    ) -> SandboxList:
        statuses = _normalize_statuses(status, SandboxStatus)
        response = await self._list_api_call(
            owner_id, statuses, cursor, limit, sandbox_group_id, name
        )
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
        sandbox_group_id: str | None = None,
        name: str | None = None,
    ) -> Response[Error | _SandboxWithCursorList]:
        return await list_sandboxes.asyncio_detailed(
            client=self.client,
            owner_id=owner_id,
            status=statuses or UNSET,
            sandbox_group_id=sandbox_group_id
            if sandbox_group_id is not None
            else UNSET,
            name=name if name is not None else UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    async def list_groups(
        self, owner_id: str, cursor: str | None = None, limit: int | None = None
    ) -> SandboxGroupList:
        response = await self._list_groups_api_call(owner_id, cursor, limit)
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list sandbox groups: unexpected response type")
        groups = [_to_sandbox_group(item.sandbox_group) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SandboxGroupList(groups=groups, next_cursor=next_cursor)

    @handle_http_errors("list sandbox groups")
    async def _list_groups_api_call(
        self, owner_id: str, cursor: str | None = None, limit: int | None = None
    ) -> Response[Error | _SandboxGroupWithCursorList]:
        return await list_sandbox_groups.asyncio_detailed(
            client=self.client,
            owner_id=owner_id,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    async def create_group(
        self, owner_id: str, name: str, region: str | None
    ) -> SandboxGroup:
        body = SandboxGroupPOST(
            owner_id=owner_id, name=name, region=region if region is not None else UNSET
        )
        with request_errors("create sandbox group"):
            response = await create_sandbox_group.asyncio_detailed(
                client=self.client, body=body
            )
        _handle_sandbox_api_error(response, "create sandbox group")
        if not isinstance(response.parsed, GeneratedSandboxGroup):
            raise RenderError(
                "Failed to create sandbox group: unexpected response type"
            )
        return _to_sandbox_group(response.parsed)

    async def get_group(self, sandbox_group_id: str) -> SandboxGroup:
        with request_errors("retrieve sandbox group"):
            response = await retrieve_sandbox_group.asyncio_detailed(
                sandbox_group_id, client=self.client
            )
        _handle_sandbox_api_error(response, "retrieve sandbox group")
        if not isinstance(response.parsed, GeneratedSandboxGroup):
            raise RenderError(
                "Failed to retrieve sandbox group: unexpected response type"
            )
        return _to_sandbox_group(response.parsed)

    async def update_group(
        self, sandbox_group_id: str, concurrency_limit: int
    ) -> SandboxGroup:
        with request_errors("update sandbox group"):
            response = await update_sandbox_group.asyncio_detailed(
                sandbox_group_id,
                client=self.client,
                body=SandboxGroupPATCH(concurrency_limit=concurrency_limit),
            )
        _handle_sandbox_api_error(response, "update sandbox group")
        if not isinstance(response.parsed, GeneratedSandboxGroup):
            raise RenderError(
                "Failed to update sandbox group: unexpected response type"
            )
        return _to_sandbox_group(response.parsed)

    async def delete_group(self, sandbox_group_id: str) -> None:
        with request_errors("delete sandbox group"):
            response = await delete_sandbox_group.asyncio_detailed(
                sandbox_group_id, client=self.client
            )
        _handle_sandbox_api_error(response, "delete sandbox group")

    async def set_default_group(self, sandbox_group_id: str) -> SandboxGroup:
        with request_errors("set default sandbox group"):
            response = await set_default_sandbox_group.asyncio_detailed(
                sandbox_group_id, client=self.client
            )
        _handle_sandbox_api_error(response, "set default sandbox group")
        if not isinstance(response.parsed, GeneratedSandboxGroup):
            raise RenderError(
                "Failed to set default sandbox group: unexpected response type"
            )
        return _to_sandbox_group(response.parsed)

    async def terminate(self, sandbox_id: str, owner_id: str) -> None:
        with request_errors("terminate sandbox"):
            response = await terminate_sandbox.asyncio_detailed(
                sandbox_id, client=self.client, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        _handle_sandbox_api_error(response, "terminate sandbox")

    async def create_snapshot(
        self,
        sandbox_id: str,
        kind: str | None,
        name: str | None,
        ttl_seconds: int | None,
        owner_id: str | Unset,
    ) -> Snapshot:
        body = SandboxSnapshotPOST(
            kind=SandboxSnapshotKind(kind) if kind is not None else UNSET,
            name=name if name is not None else UNSET,
            ttl_seconds=ttl_seconds if ttl_seconds is not None else UNSET,
        )
        with request_errors("create snapshot"):
            response = await create_sandbox_snapshot.asyncio_detailed(
                sandbox_id, client=self.client, body=body, owner_id=owner_id
            )
        if response.status_code == 404:
            raise SandboxNotFoundError(f"sandbox {sandbox_id} not found")
        _handle_sandbox_api_error(response, "create snapshot")
        if not isinstance(response.parsed, GeneratedSandboxSnapshot):
            raise RenderError("Failed to create snapshot: unexpected response type")
        return _to_snapshot(response.parsed)

    async def get_snapshot(
        self, sandbox_group_id: str, snapshot_id: str, owner_id: str | Unset
    ) -> Snapshot:
        with request_errors("retrieve snapshot"):
            response = await retrieve_sandbox_snapshot.asyncio_detailed(
                sandbox_group_id, snapshot_id, client=self.client, owner_id=owner_id
            )
        _handle_snapshot_api_error(response, snapshot_id, "retrieve snapshot")
        if not isinstance(response.parsed, GeneratedSandboxSnapshot):
            raise RenderError("Failed to retrieve snapshot: unexpected response type")
        return _to_snapshot(response.parsed)

    async def list_snapshots(
        self,
        owner_id: str,
        sandbox_group_id: str,
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
    ) -> SnapshotList:
        statuses = _normalize_statuses(status, SandboxSnapshotStatus)
        response = await self._list_snapshots_api_call(
            sandbox_group_id, owner_id, statuses, cursor, limit
        )
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list snapshots: unexpected response type")
        snapshots = [_to_snapshot(item.snapshot) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return SnapshotList(snapshots=snapshots, next_cursor=next_cursor)

    @handle_http_errors("list snapshots")
    async def _list_snapshots_api_call(
        self,
        sandbox_group_id: str,
        owner_id: str,
        statuses: _SandboxSnapshotStatusList,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxSnapshotWithCursorList]:
        return await list_sandbox_snapshots.asyncio_detailed(
            sandbox_group_id,
            client=self.client,
            owner_id=owner_id,
            status=statuses or UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    async def delete_snapshot(
        self, sandbox_group_id: str, snapshot_id: str, owner_id: str | Unset
    ) -> None:
        with request_errors("delete snapshot"):
            response = await delete_sandbox_snapshot.asyncio_detailed(
                sandbox_group_id, snapshot_id, client=self.client, owner_id=owner_id
            )
        _handle_snapshot_api_error(response, snapshot_id, "delete snapshot")

    async def import_image(
        self,
        sandbox_group_id: str,
        name: str,
        source: str,
        registry_credentials: RegistryCredentials | Mapping[str, str] | None,
    ) -> Image:
        body = SandboxBuildPOST(name=name, source_image=source)
        if registry_credentials is not None:
            if isinstance(registry_credentials, Mapping):
                registry_credentials = RegistryCredentials(
                    username=registry_credentials["username"],
                    password=registry_credentials["password"],
                )
            body.registry_credential = SandboxBuildPOSTRegistryCredential(
                username=registry_credentials.username,
                password=registry_credentials.password,
            )
        with request_errors("import image"):
            response = await create_sandbox_build.asyncio_detailed(
                sandbox_group_id, client=self.client, body=body
            )
        _handle_sandbox_api_error(response, "import image")
        if not isinstance(response.parsed, GeneratedSandboxBuild):
            raise RenderError("Failed to import image: unexpected response type")
        return _to_image(response.parsed)

    async def get_image(self, sandbox_group_id: str, image_id: str) -> Image:
        with request_errors("retrieve image"):
            response = await retrieve_sandbox_build.asyncio_detailed(
                sandbox_group_id, image_id, client=self.client
            )
        _handle_image_api_error(response, image_id, "retrieve image")
        if not isinstance(response.parsed, GeneratedSandboxBuild):
            raise RenderError("Failed to retrieve image: unexpected response type")
        return _to_image(response.parsed)

    async def list_images(
        self,
        sandbox_group_id: str,
        name: str | None,
        status: str | Sequence[str] | None,
        cursor: str | None,
        limit: int | None,
    ) -> ImageList:
        statuses = _normalize_statuses(status, SandboxBuildStatus)
        response = await self._list_images_api_call(
            sandbox_group_id, name, statuses, cursor, limit
        )
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list images: unexpected response type")
        images = [_to_image(item.build) for item in parsed]
        next_cursor = parsed[-1].cursor if parsed else None
        return ImageList(images=images, next_cursor=next_cursor)

    @handle_http_errors("list images")
    async def _list_images_api_call(
        self,
        sandbox_group_id: str,
        name: str | None,
        statuses: _SandboxBuildStatusList,
        cursor: str | None,
        limit: int | None,
    ) -> Response[Error | _SandboxBuildWithCursorList]:
        return await list_sandbox_builds.asyncio_detailed(
            sandbox_group_id,
            client=self.client,
            name=name if name is not None else UNSET,
            status=statuses or UNSET,
            cursor=cursor if cursor is not None else UNSET,
            limit=limit if limit is not None else UNSET,
        )

    async def create_credential(
        self,
        sandbox_group_id: str,
        credential_id: str,
        domain: str,
        value: str,
        injection: CredentialInjection,
        enabled: bool | None,
        methods: Sequence[str] | None,
        paths: Sequence[str] | None,
    ) -> Credential:
        body = SandboxCredentialCreate(
            id=credential_id,
            domain=domain,
            value=value,
            injection=_to_credential_injection_body(injection),
        )
        if enabled is not None:
            body.enabled = enabled
        if methods is not None:
            body.methods = _string_list(methods)
        if paths is not None:
            body.paths = _string_list(paths)
        with request_errors("create credential"):
            response = await create_sandbox_group_credential.asyncio_detailed(
                sandbox_group_id, client=self.client, body=body
            )
        _handle_sandbox_api_error(response, "create credential")
        if not isinstance(response.parsed, GeneratedCredential):
            raise RenderError("Failed to create credential: unexpected response type")
        return _to_credential(response.parsed)

    async def get_credential(
        self, sandbox_group_id: str, credential_id: str
    ) -> Credential:
        with request_errors("retrieve credential"):
            response = await retrieve_sandbox_group_credential.asyncio_detailed(
                sandbox_group_id, credential_id, client=self.client
            )
        _handle_credential_api_error(
            response, f"credential {credential_id} not found", "retrieve credential"
        )
        if not isinstance(response.parsed, GeneratedCredential):
            raise RenderError("Failed to retrieve credential: unexpected response type")
        return _to_credential(response.parsed)

    async def list_credentials(self, sandbox_group_id: str) -> _CredentialList:
        with request_errors("list credentials"):
            response = await list_sandbox_group_credentials.asyncio_detailed(
                sandbox_group_id, client=self.client
            )
        _handle_sandbox_api_error(response, "list credentials")
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError("Failed to list credentials: unexpected response type")
        return [_to_credential(item) for item in parsed]

    async def update_credential(
        self,
        sandbox_group_id: str,
        credential_id: str,
        value: str | None,
        domain: str | None,
        enabled: bool | None,
        methods: Sequence[str] | None,
        paths: Sequence[str] | None,
        injection: CredentialInjection | None,
    ) -> Credential:
        body = SandboxCredentialUpdate()
        if value is not None:
            body.value = value
        if domain is not None:
            body.domain = domain
        if enabled is not None:
            body.enabled = enabled
        if methods is not None:
            body.methods = _string_list(methods)
        if paths is not None:
            body.paths = _string_list(paths)
        if injection is not None:
            body.injection = _to_credential_injection_body(injection)
        with request_errors("update credential"):
            response = await update_sandbox_group_credential.asyncio_detailed(
                sandbox_group_id, credential_id, client=self.client, body=body
            )
        _handle_credential_api_error(
            response, f"credential {credential_id} not found", "update credential"
        )
        if not isinstance(response.parsed, GeneratedCredential):
            raise RenderError("Failed to update credential: unexpected response type")
        return _to_credential(response.parsed)

    async def delete_credential(
        self, sandbox_group_id: str, credential_id: str
    ) -> None:
        with request_errors("delete credential"):
            response = await delete_sandbox_group_credential.asyncio_detailed(
                sandbox_group_id, credential_id, client=self.client
            )
        # Deleting a missing credential succeeds, so a 404 is about the group.
        _handle_sandbox_api_error(response, "delete credential")

    async def list_credential_versions(
        self, sandbox_group_id: str, credential_id: str
    ) -> _CredentialVersionList:
        with request_errors("list credential versions"):
            response = await list_sandbox_group_credential_versions.asyncio_detailed(
                sandbox_group_id, credential_id, client=self.client
            )
        _handle_credential_api_error(
            response,
            f"credential {credential_id} not found",
            "list credential versions",
        )
        parsed = response.parsed
        if not isinstance(parsed, list):
            raise RenderError(
                "Failed to list credential versions: unexpected response type"
            )
        return [_to_credential_version(item) for item in parsed]

    async def restore_credential(
        self, sandbox_group_id: str, credential_id: str, version_id: int
    ) -> Credential:
        with request_errors("restore credential"):
            response = await restore_sandbox_group_credential.asyncio_detailed(
                sandbox_group_id,
                credential_id,
                client=self.client,
                body=SandboxCredentialRestore(version_id=version_id),
            )
        _handle_credential_api_error(
            response,
            f"credential {credential_id} or its version {version_id} not found",
            "restore credential",
        )
        if not isinstance(response.parsed, GeneratedCredential):
            raise RenderError("Failed to restore credential: unexpected response type")
        return _to_credential(response.parsed)

    async def _raise_connect_token_error(
        self, sandbox_id: str, owner_id: str, response: httpx.Response, action: str
    ) -> NoReturn:
        # The 409 body doesn't say which way the sandbox ended or when, so look
        # it up to name both.
        if (
            response.status_code == 409
            and _error_body(response.text).code == _SANDBOX_NOT_RUNNING_CODE
        ):
            try:
                sandbox = await self.get(sandbox_id, owner_id)
            except RenderError:
                pass
            else:
                ended_error = _sandbox_ended_error(sandbox, action)
                if ended_error is not None:
                    raise ended_error
        _raise_sandbox_http_error(
            sandbox_id, response.status_code, response.text, action
        )

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
            await self._raise_connect_token_error(
                sandbox_id, owner_id, response, "exec"
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
            await self._raise_connect_token_error(
                sandbox_id, owner_id, response, operation
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
        # instead of turning a trailing slash into a 400.
        remote_path = normalize_remote_path(remote_path)
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


def _load_event(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise SandboxExecError(
            f"failed to parse sandbox exec event data: {data}"
        ) from exc


def _sandbox_ended_error(sandbox: Sandbox, action: str) -> SandboxEndedError | None:
    """Name how and when a sandbox ended, or None if it hasn't."""
    if sandbox.status not in ("terminated", "errored"):
        return None
    ended = "was terminated" if sandbox.status == "terminated" else "errored"
    at = ""
    if sandbox.terminated_at:
        # Match the API's own format, which ends in Z rather than +00:00.
        at = f" at {sandbox.terminated_at.isoformat().replace('+00:00', 'Z')}"
    return SandboxEndedError(
        f"{action} failed: sandbox {sandbox.id} {ended}{at}",
        sandbox_status=sandbox.status,
        code=_SANDBOX_NOT_RUNNING_CODE,
        status_code=409,
    )


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
    _raise_for_error_code(status_code, body, action)
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
