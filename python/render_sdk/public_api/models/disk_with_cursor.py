from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.disk_details import DiskDetails


T = TypeVar("T", bound="DiskWithCursor")


@_attrs_define
class DiskWithCursor:
    """
    Attributes:
        disk (DiskDetails):
        cursor (str):
    """

    disk: "DiskDetails"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disk = self.disk.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disk": disk,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.disk_details import DiskDetails

        d = dict(src_dict)
        disk = DiskDetails.from_dict(d.pop("disk"))

        cursor = d.pop("cursor")

        disk_with_cursor = cls(
            disk=disk,
            cursor=cursor,
        )

        disk_with_cursor.additional_properties = d
        return disk_with_cursor

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
