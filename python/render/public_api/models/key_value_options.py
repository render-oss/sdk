from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="KeyValueOptions")


@_attrs_define
class KeyValueOptions:
    """Options for a Key Value instance

    Attributes:
        maxmemory_policy (Union[Unset, str]):
    """

    maxmemory_policy: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        maxmemory_policy = self.maxmemory_policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if maxmemory_policy is not UNSET:
            field_dict["maxmemoryPolicy"] = maxmemory_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        maxmemory_policy = d.pop("maxmemoryPolicy", UNSET)

        key_value_options = cls(
            maxmemory_policy=maxmemory_policy,
        )

        key_value_options.additional_properties = d
        return key_value_options

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
