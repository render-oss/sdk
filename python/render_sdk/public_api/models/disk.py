from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Disk")


@_attrs_define
class Disk:
    """
    Attributes:
        id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        name (str):
        size_gb (int):
        mount_path (str):
    """

    id: str
    name: str
    size_gb: int
    mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size_gb = self.size_gb

        mount_path = self.mount_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "sizeGB": size_gb,
                "mountPath": mount_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size_gb = d.pop("sizeGB")

        mount_path = d.pop("mountPath")

        disk = cls(
            id=id,
            name=name,
            size_gb=size_gb,
            mount_path=mount_path,
        )

        disk.additional_properties = d
        return disk

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
