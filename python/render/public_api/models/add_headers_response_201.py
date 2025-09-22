from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.header import Header


T = TypeVar("T", bound="AddHeadersResponse201")


@_attrs_define
class AddHeadersResponse201:
    """
    Attributes:
        headers (Union[Unset, Header]):
    """

    headers: Union[Unset, "Header"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.header import Header

        d = dict(src_dict)
        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, Header]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = Header.from_dict(_headers)

        add_headers_response_201 = cls(
            headers=headers,
        )

        add_headers_response_201.additional_properties = d
        return add_headers_response_201

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
