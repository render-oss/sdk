from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.key_value import KeyValue


T = TypeVar("T", bound="KeyValueWithCursor")


@_attrs_define
class KeyValueWithCursor:
    """
    Attributes:
        key_value (KeyValue): A Key Value instance
        cursor (str):
    """

    key_value: "KeyValue"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_value = self.key_value.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keyValue": key_value,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.key_value import KeyValue

        d = dict(src_dict)
        key_value = KeyValue.from_dict(d.pop("keyValue"))

        cursor = d.pop("cursor")

        key_value_with_cursor = cls(
            key_value=key_value,
            cursor=cursor,
        )

        key_value_with_cursor.additional_properties = d
        return key_value_with_cursor

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
