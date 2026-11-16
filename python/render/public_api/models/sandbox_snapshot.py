import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sandbox_plan import SandboxPlan
from ..models.sandbox_snapshot_kind import SandboxSnapshotKind
from ..models.sandbox_snapshot_status import SandboxSnapshotStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxSnapshot")


@_attrs_define
class SandboxSnapshot:
    """A saved filesystem or runtime state that can be used to create another sandbox.

    Attributes:
        id (str): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        source_sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        kind (SandboxSnapshotKind): The state to capture. A `filesystem` snapshot captures the writable filesystem and
            can be restored to any plan. A `runtime` snapshot also captures memory and CPU state and must be restored to the
            source sandbox plan.
        status (SandboxSnapshotStatus): The snapshot's current status.
        plan (Union[SandboxPlan, str]): The source sandbox's compute plan when the snapshot was captured. See
            `sandboxPlan` for known values.
        requested_at (datetime.datetime): The timestamp when the snapshot was requested, in ISO 8601 format.
        expires_at (datetime.datetime): The timestamp after which the snapshot can no longer be retrieved or restored,
            in ISO 8601 format. Each time you create a sandbox from this snapshot, Render resets its expiration to
            `ttlSeconds` seconds after that use. For snapshots with no expiration (`ttlSeconds: 0`), this is
            `9999-12-31T23:59:59Z`.
        name (Union[None, Unset, str]): The name assigned when the snapshot was created. Cannot be changed. Null if no
            name was provided.
        captured_at (Union[None, Unset, datetime.datetime]): The timestamp when capture completed, in ISO 8601 format.
            Null until the snapshot is `available`.
        ttl_seconds (Union[Unset, int]): The snapshot's lifetime after its last use, in seconds. A value of 0 means the
            snapshot does not expire. If omitted, Render's default snapshot lifetime applies.
        size_bytes (Union[None, Unset, int]): The size of the snapshot, in bytes. Null until the snapshot is
            `available`.
        error (Union[None, Unset, str]): The reason the snapshot failed. Null unless its status is `failed`.
    """

    id: str
    sandbox_group_id: str
    source_sandbox_id: str
    kind: SandboxSnapshotKind
    status: SandboxSnapshotStatus
    plan: Union[SandboxPlan, str]
    requested_at: datetime.datetime
    expires_at: datetime.datetime
    name: Union[None, Unset, str] = UNSET
    captured_at: Union[None, Unset, datetime.datetime] = UNSET
    ttl_seconds: Union[Unset, int] = UNSET
    size_bytes: Union[None, Unset, int] = UNSET
    error: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sandbox_group_id = self.sandbox_group_id

        source_sandbox_id = self.source_sandbox_id

        kind = self.kind.value

        status = self.status.value

        plan: str
        if isinstance(self.plan, SandboxPlan):
            plan = self.plan.value
        else:
            plan = self.plan

        requested_at = self.requested_at.isoformat()

        expires_at = self.expires_at.isoformat()

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        captured_at: Union[None, Unset, str]
        if isinstance(self.captured_at, Unset):
            captured_at = UNSET
        elif isinstance(self.captured_at, datetime.datetime):
            captured_at = self.captured_at.isoformat()
        else:
            captured_at = self.captured_at

        ttl_seconds = self.ttl_seconds

        size_bytes: Union[None, Unset, int]
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sandboxGroupId": sandbox_group_id,
                "sourceSandboxId": source_sandbox_id,
                "kind": kind,
                "status": status,
                "plan": plan,
                "requestedAt": requested_at,
                "expiresAt": expires_at,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if captured_at is not UNSET:
            field_dict["capturedAt"] = captured_at
        if ttl_seconds is not UNSET:
            field_dict["ttlSeconds"] = ttl_seconds
        if size_bytes is not UNSET:
            field_dict["sizeBytes"] = size_bytes
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        sandbox_group_id = d.pop("sandboxGroupId")

        source_sandbox_id = d.pop("sourceSandboxId")

        kind = SandboxSnapshotKind(d.pop("kind"))

        status = SandboxSnapshotStatus(d.pop("status"))

        def _parse_plan(data: object) -> Union[SandboxPlan, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = SandboxPlan(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[SandboxPlan, str], data)

        plan = _parse_plan(d.pop("plan"))

        requested_at = isoparse(d.pop("requestedAt"))

        expires_at = isoparse(d.pop("expiresAt"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_captured_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                captured_at_type_0 = isoparse(data)

                return captured_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        captured_at = _parse_captured_at(d.pop("capturedAt", UNSET))

        ttl_seconds = d.pop("ttlSeconds", UNSET)

        def _parse_size_bytes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        sandbox_snapshot = cls(
            id=id,
            sandbox_group_id=sandbox_group_id,
            source_sandbox_id=source_sandbox_id,
            kind=kind,
            status=status,
            plan=plan,
            requested_at=requested_at,
            expires_at=expires_at,
            name=name,
            captured_at=captured_at,
            ttl_seconds=ttl_seconds,
            size_bytes=size_bytes,
            error=error,
        )

        sandbox_snapshot.additional_properties = d
        return sandbox_snapshot

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
