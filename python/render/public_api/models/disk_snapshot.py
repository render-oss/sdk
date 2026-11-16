from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskSnapshot")


@_attrs_define
class DiskSnapshot:
    """
    Attributes:
        created_at (datetime.datetime | Unset):
        snapshot_key (str | Unset):
        instance_id (str | Unset): When a service with a disk is scaled, the instanceId is used to identify the instance
            that the disk is attached to. Each instance's disks get their own snapshots, and can be restored separately.
    """

    created_at: datetime.datetime | Unset = UNSET
    snapshot_key: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        snapshot_key = self.snapshot_key

        instance_id = self.instance_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if snapshot_key is not UNSET:
            field_dict["snapshotKey"] = snapshot_key
        if instance_id is not UNSET:
            field_dict["instanceId"] = instance_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _created_at = d.pop("createdAt", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        snapshot_key = d.pop("snapshotKey", UNSET)

        instance_id = d.pop("instanceId", UNSET)

        disk_snapshot = cls(
            created_at=created_at,
            snapshot_key=snapshot_key,
            instance_id=instance_id,
        )

        disk_snapshot.additional_properties = d
        return disk_snapshot

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
