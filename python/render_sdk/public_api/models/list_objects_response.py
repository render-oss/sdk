from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.object_with_cursor import ObjectWithCursor


T = TypeVar("T", bound="ListObjectsResponse")


@_attrs_define
class ListObjectsResponse:
    """
    Attributes:
        items (list['ObjectWithCursor']):
        has_next (bool): Whether there are more results after this page.
        next_cursor (Union[Unset, str]): Cursor to fetch the next page. Only present when hasNext is true.
    """

    items: list["ObjectWithCursor"]
    has_next: bool
    next_cursor: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        has_next = self.has_next

        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "hasNext": has_next,
            }
        )
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_with_cursor import ObjectWithCursor

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ObjectWithCursor.from_dict(items_item_data)

            items.append(items_item)

        has_next = d.pop("hasNext")

        next_cursor = d.pop("nextCursor", UNSET)

        list_objects_response = cls(
            items=items,
            has_next=has_next,
            next_cursor=next_cursor,
        )

        list_objects_response.additional_properties = d
        return list_objects_response

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
