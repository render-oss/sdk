from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DiskPOST")


@_attrs_define
class DiskPOST:
    """
    Attributes:
        name (str):
        size_gb (int):
        mount_path (str):
        service_id (str):
    """

    name: str
    size_gb: int
    mount_path: str
    service_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        size_gb = self.size_gb

        mount_path = self.mount_path

        service_id = self.service_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "sizeGB": size_gb,
                "mountPath": mount_path,
                "serviceId": service_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        size_gb = d.pop("sizeGB")

        mount_path = d.pop("mountPath")

        service_id = d.pop("serviceId")

        disk_post = cls(
            name=name,
            size_gb=size_gb,
            mount_path=mount_path,
            service_id=service_id,
        )

        disk_post.additional_properties = d
        return disk_post

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
