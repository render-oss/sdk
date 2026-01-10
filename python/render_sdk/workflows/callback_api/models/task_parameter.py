from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskParameter")


@_attrs_define
class TaskParameter:
    """Information about a task parameter extracted from function signature

    Attributes:
        name (str): Parameter name
        has_default (bool): Whether the parameter has a default value
        type_ (Union[Unset, str]): String representation of the parameter type hint
        default_value (Union[Unset, str]): JSON-encoded default value (if has_default is true)
    """

    name: str
    has_default: bool
    type_: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        has_default = self.has_default

        type_ = self.type_

        default_value = self.default_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "has_default": has_default,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if default_value is not UNSET:
            field_dict["default_value"] = default_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        has_default = d.pop("has_default")

        type_ = d.pop("type", UNSET)

        default_value = d.pop("default_value", UNSET)

        task_parameter = cls(
            name=name,
            has_default=has_default,
            type_=type_,
            default_value=default_value,
        )

        task_parameter.additional_properties = d
        return task_parameter

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
