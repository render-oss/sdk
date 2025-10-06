from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SnapshotRestorePOST")


@_attrs_define
class SnapshotRestorePOST:
    """
    Attributes:
        snapshot_key (str):
        instance_id (Union[Unset, str]): When a service with a disk is scaled, the instanceId is used to identify the
            instance that the disk is attached to. Each instance's disks get their own snapshots, and can be restored
            separately.
    """

    snapshot_key: str
    instance_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        snapshot_key = self.snapshot_key

        instance_id = self.instance_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "snapshotKey": snapshot_key,
            }
        )
        if instance_id is not UNSET:
            field_dict["instanceId"] = instance_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        snapshot_key = d.pop("snapshotKey")

        instance_id = d.pop("instanceId", UNSET)

        snapshot_restore_post = cls(
            snapshot_key=snapshot_key,
            instance_id=instance_id,
        )

        snapshot_restore_post.additional_properties = d
        return snapshot_restore_post

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
