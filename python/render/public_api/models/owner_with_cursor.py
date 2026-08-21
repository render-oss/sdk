from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.owner import Owner


T = TypeVar("T", bound="OwnerWithCursor")


@_attrs_define
class OwnerWithCursor:
    """
    Attributes:
        owner (Union[Unset, Owner]):
        cursor (Union[Unset, str]):
    """

    owner: Union[Unset, "Owner"] = UNSET
    cursor: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if owner is not UNSET:
            field_dict["owner"] = owner
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.owner import Owner

        d = dict(src_dict)
        _owner = d.pop("owner", UNSET)
        owner: Union[Unset, Owner]
        if isinstance(_owner, Unset):
            owner = UNSET
        else:
            owner = Owner.from_dict(_owner)

        cursor = d.pop("cursor", UNSET)

        owner_with_cursor = cls(
            owner=owner,
            cursor=cursor,
        )

        owner_with_cursor.additional_properties = d
        return owner_with_cursor

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
