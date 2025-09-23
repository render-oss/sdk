from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.custom_domain import CustomDomain


T = TypeVar("T", bound="CustomDomainWithCursor")


@_attrs_define
class CustomDomainWithCursor:
    """
    Attributes:
        custom_domain (CustomDomain):
        cursor (str):
    """

    custom_domain: "CustomDomain"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        custom_domain = self.custom_domain.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customDomain": custom_domain,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_domain import CustomDomain

        d = dict(src_dict)
        custom_domain = CustomDomain.from_dict(d.pop("customDomain"))

        cursor = d.pop("cursor")

        custom_domain_with_cursor = cls(
            custom_domain=custom_domain,
            cursor=cursor,
        )

        custom_domain_with_cursor.additional_properties = d
        return custom_domain_with_cursor

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
