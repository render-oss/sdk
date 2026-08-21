from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DiskUpdated")


@_attrs_define
class DiskUpdated:
    """
    Attributes:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        from_size_gb (int):
        to_size_gb (int):
    """

    disk_id: str
    from_size_gb: int
    to_size_gb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk_id = self.disk_id

        from_size_gb = self.from_size_gb

        to_size_gb = self.to_size_gb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "diskId": disk_id,
                "fromSizeGB": from_size_gb,
                "toSizeGB": to_size_gb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disk_id = d.pop("diskId")

        from_size_gb = d.pop("fromSizeGB")

        to_size_gb = d.pop("toSizeGB")

        disk_updated = cls(
            disk_id=disk_id,
            from_size_gb=from_size_gb,
            to_size_gb=to_size_gb,
        )

        disk_updated.additional_properties = d
        return disk_updated

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
