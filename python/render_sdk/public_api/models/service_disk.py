from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceDisk")


@_attrs_define
class ServiceDisk:
    """
    Attributes:
        name (str):
        mount_path (str):
        size_gb (Union[Unset, int]): Defaults to 1
    """

    name: str
    mount_path: str
    size_gb: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mount_path = self.mount_path

        size_gb = self.size_gb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mountPath": mount_path,
            }
        )
        if size_gb is not UNSET:
            field_dict["sizeGB"] = size_gb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        mount_path = d.pop("mountPath")

        size_gb = d.pop("sizeGB", UNSET)

        service_disk = cls(
            name=name,
            mount_path=mount_path,
            size_gb=size_gb,
        )

        service_disk.additional_properties = d
        return service_disk

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
