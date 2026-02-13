from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.object_metadata import ObjectMetadata


T = TypeVar("T", bound="ObjectWithCursor")


@_attrs_define
class ObjectWithCursor:
    """
    Attributes:
        cursor (str):
        object_ (ObjectMetadata):
    """

    cursor: str
    object_: "ObjectMetadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cursor = self.cursor

        object_ = self.object_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cursor": cursor,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_metadata import ObjectMetadata

        d = dict(src_dict)
        cursor = d.pop("cursor")

        object_ = ObjectMetadata.from_dict(d.pop("object"))

        object_with_cursor = cls(
            cursor=cursor,
            object_=object_,
        )

        object_with_cursor.additional_properties = d
        return object_with_cursor

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
