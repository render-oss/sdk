from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_snapshot_kind import SandboxSnapshotKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxSnapshotPOST")


@_attrs_define
class SandboxSnapshotPOST:
    """The settings for the sandbox snapshot to capture.

    Attributes:
        kind (SandboxSnapshotKind | Unset): The state to capture. A `filesystem` snapshot captures the writable
            filesystem and can be restored to any plan. A `runtime` snapshot also captures memory and CPU state and must be
            restored to the source sandbox plan.
             Default: SandboxSnapshotKind.RUNTIME.
        name (str | Unset): A case-sensitive name for snapshots in a sandbox group, up to 64 characters. Must not start
            with `snp-`. Multiple snapshots can share a name. When creating a sandbox by snapshot name, Render uses the most
            recently created snapshot with that name that is `available` and unexpired.
             Example: gold.
        ttl_seconds (int | Unset): The snapshot's lifetime after its last use, in seconds. Creating a sandbox from this
            snapshot resets its remaining lifetime to this duration. Use 0 to keep the snapshot until you delete it.
            Defaults to Render's snapshot lifetime. Cannot be combined with `expiresAt`.
        expires_at (datetime.datetime | Unset): The expiration timestamp, in ISO 8601 format. Deprecated; use
            `ttlSeconds` instead. Must be in the future. Render sets the snapshot lifetime to the duration between the
            request and this timestamp.
    """

    kind: SandboxSnapshotKind | Unset = SandboxSnapshotKind.RUNTIME
    name: str | Unset = UNSET
    ttl_seconds: int | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        name = self.name

        ttl_seconds = self.ttl_seconds

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name
        if ttl_seconds is not UNSET:
            field_dict["ttlSeconds"] = ttl_seconds
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: SandboxSnapshotKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = SandboxSnapshotKind(_kind)

        name = d.pop("name", UNSET)

        ttl_seconds = d.pop("ttlSeconds", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)

        sandbox_snapshot_post = cls(
            kind=kind,
            name=name,
            ttl_seconds=ttl_seconds,
            expires_at=expires_at,
        )

        sandbox_snapshot_post.additional_properties = d
        return sandbox_snapshot_post

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
