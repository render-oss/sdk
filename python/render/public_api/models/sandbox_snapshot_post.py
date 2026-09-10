import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sandbox_snapshot_kind import SandboxSnapshotKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxSnapshotPOST")


@_attrs_define
class SandboxSnapshotPOST:
    """
    Attributes:
        kind (Union[Unset, SandboxSnapshotKind]): `filesystem` captures the writable filesystem and restores onto any
            plan.
            `runtime` also captures memory and CPU state and restores only onto the
            plan of the source sandbox.
             Default: SandboxSnapshotKind.FILESYSTEM.
        expires_at (Union[Unset, datetime.datetime]): The time after which the snapshot can no longer be retrieved or
            restored.
            Must be in the future. Omit to use Render's default snapshot lifetime.
    """

    kind: Union[Unset, SandboxSnapshotKind] = SandboxSnapshotKind.FILESYSTEM
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, SandboxSnapshotKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = SandboxSnapshotKind(_kind)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        sandbox_snapshot_post = cls(
            kind=kind,
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
