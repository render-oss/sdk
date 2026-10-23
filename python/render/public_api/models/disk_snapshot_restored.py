import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskSnapshotRestored")


@_attrs_define
class DiskSnapshotRestored:
    """
    Attributes:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        triggered_by_user (Union[None, str]):
        instance_id (Union[Unset, str]): The instance whose disk was restored, when the restore named one. A service
            instance ID, or the service ID for an older single disk.
        snapshot_created_at (Union[Unset, datetime.datetime]): When the restored snapshot was taken
    """

    disk_id: str
    triggered_by_user: Union[None, str]
    instance_id: Union[Unset, str] = UNSET
    snapshot_created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_id = self.disk_id

        triggered_by_user: Union[None, str]
        triggered_by_user = self.triggered_by_user

        instance_id = self.instance_id

        snapshot_created_at: Union[Unset, str] = UNSET
        if not isinstance(self.snapshot_created_at, Unset):
            snapshot_created_at = self.snapshot_created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "diskId": disk_id,
                "triggeredByUser": triggered_by_user,
            }
        )
        if instance_id is not UNSET:
            field_dict["instanceId"] = instance_id
        if snapshot_created_at is not UNSET:
            field_dict["snapshotCreatedAt"] = snapshot_created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disk_id = d.pop("diskId")

        def _parse_triggered_by_user(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        triggered_by_user = _parse_triggered_by_user(d.pop("triggeredByUser"))

        instance_id = d.pop("instanceId", UNSET)

        _snapshot_created_at = d.pop("snapshotCreatedAt", UNSET)
        snapshot_created_at: Union[Unset, datetime.datetime]
        if isinstance(_snapshot_created_at, Unset):
            snapshot_created_at = UNSET
        else:
            snapshot_created_at = isoparse(_snapshot_created_at)

        disk_snapshot_restored = cls(
            disk_id=disk_id,
            triggered_by_user=triggered_by_user,
            instance_id=instance_id,
            snapshot_created_at=snapshot_created_at,
        )

        disk_snapshot_restored.additional_properties = d
        return disk_snapshot_restored

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
