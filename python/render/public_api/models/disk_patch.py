from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskPATCH")


@_attrs_define
class DiskPATCH:
    """
    Attributes:
        name (Union[Unset, str]):
        size_gb (Union[Unset, int]):
        mount_path (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    size_gb: Union[Unset, int] = UNSET
    mount_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        size_gb = self.size_gb

        mount_path = self.mount_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if size_gb is not UNSET:
            field_dict["sizeGB"] = size_gb
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        size_gb = d.pop("sizeGB", UNSET)

        mount_path = d.pop("mountPath", UNSET)

        disk_patch = cls(
            name=name,
            size_gb=size_gb,
            mount_path=mount_path,
        )

        disk_patch.additional_properties = d
        return disk_patch

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
