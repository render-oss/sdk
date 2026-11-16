from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        plan (SandboxPlan | str): The source sandbox's compute plan when the snapshot was captured. See `sandboxPlan`
            for known values.
        requested_at (datetime.datetime): The timestamp when the snapshot was requested, in ISO 8601 format.
        expires_at (datetime.datetime): The timestamp after which the snapshot can no longer be retrieved or restored,
            in ISO 8601 format. Each time you create a sandbox from this snapshot, Render resets its expiration to
            `ttlSeconds` seconds after that use. For snapshots with no expiration (`ttlSeconds: 0`), this is
            `9999-12-31T23:59:59Z`.
        name (None | str | Unset): The name assigned when the snapshot was created. Cannot be changed. Null if no name
            was provided.
        captured_at (datetime.datetime | None | Unset): The timestamp when capture completed, in ISO 8601 format. Null
            until the snapshot is `available`.
        ttl_seconds (int | Unset): The snapshot's lifetime after its last use, in seconds. A value of 0 means the
            snapshot does not expire. If omitted, Render's default snapshot lifetime applies.
        size_bytes (int | None | Unset): The size of the snapshot, in bytes. Null until the snapshot is `available`.
        error (None | str | Unset): The reason the snapshot failed. Null unless its status is `failed`.
    """

    id: str
    sandbox_group_id: str
    source_sandbox_id: str
    kind: SandboxSnapshotKind
    status: SandboxSnapshotStatus
    plan: SandboxPlan | str
    requested_at: datetime.datetime
    expires_at: datetime.datetime
    name: None | str | Unset = UNSET
    captured_at: datetime.datetime | None | Unset = UNSET
    ttl_seconds: int | Unset = UNSET
    size_bytes: int | None | Unset = UNSET
    error: None | str | Unset = UNSET
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

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        captured_at: None | str | Unset
        if isinstance(self.captured_at, Unset):
            captured_at = UNSET
        elif isinstance(self.captured_at, datetime.datetime):
            captured_at = self.captured_at.isoformat()
        else:
            captured_at = self.captured_at

        ttl_seconds = self.ttl_seconds

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        error: None | str | Unset
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

        def _parse_plan(data: object) -> SandboxPlan | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = SandboxPlan(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(SandboxPlan | str, data)

        plan = _parse_plan(d.pop("plan"))

        requested_at = datetime.datetime.fromisoformat(d.pop("requestedAt"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_captured_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                captured_at_type_0 = datetime.datetime.fromisoformat(data)

                return captured_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        captured_at = _parse_captured_at(d.pop("capturedAt", UNSET))

        ttl_seconds = d.pop("ttlSeconds", UNSET)

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("sizeBytes", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

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
