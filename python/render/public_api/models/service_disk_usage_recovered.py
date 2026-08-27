from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServiceDiskUsageRecovered")


@_attrs_define
class ServiceDiskUsageRecovered:
    """
    Attributes:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        disk_name (str):
        mount_path (str):
        usage_percent (float):
        threshold_percent (float):
    """

    disk_id: str
    disk_name: str
    mount_path: str
    usage_percent: float
    threshold_percent: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_id = self.disk_id

        disk_name = self.disk_name

        mount_path = self.mount_path

        usage_percent = self.usage_percent

        threshold_percent = self.threshold_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "diskId": disk_id,
                "diskName": disk_name,
                "mountPath": mount_path,
                "usagePercent": usage_percent,
                "thresholdPercent": threshold_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disk_id = d.pop("diskId")

        disk_name = d.pop("diskName")

        mount_path = d.pop("mountPath")

        usage_percent = d.pop("usagePercent")

        threshold_percent = d.pop("thresholdPercent")

        service_disk_usage_recovered = cls(
            disk_id=disk_id,
            disk_name=disk_name,
            mount_path=mount_path,
            usage_percent=usage_percent,
            threshold_percent=threshold_percent,
        )

        service_disk_usage_recovered.additional_properties = d
        return service_disk_usage_recovered

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
