from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresAvailableParameterOverride")


@_attrs_define
class PostgresAvailableParameterOverride:
    """
    Attributes:
        name (str):
        description (str):
        requires_restart (bool): Whether setting this parameter requires a restart to take effect.
        examples (Union[Unset, list[str]]):
        min_value (Union[Unset, float]): The minimum value allowed for numeric parameters.
        max_value (Union[Unset, float]): The maximum value allowed for numeric parameters.
    """

    name: str
    description: str
    requires_restart: bool
    examples: Union[Unset, list[str]] = UNSET
    min_value: Union[Unset, float] = UNSET
    max_value: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        requires_restart = self.requires_restart

        examples: Union[Unset, list[str]] = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        min_value = self.min_value

        max_value = self.max_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "requiresRestart": requires_restart,
            }
        )
        if examples is not UNSET:
            field_dict["examples"] = examples
        if min_value is not UNSET:
            field_dict["minValue"] = min_value
        if max_value is not UNSET:
            field_dict["maxValue"] = max_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        requires_restart = d.pop("requiresRestart")

        examples = cast(list[str], d.pop("examples", UNSET))

        min_value = d.pop("minValue", UNSET)

        max_value = d.pop("maxValue", UNSET)

        postgres_available_parameter_override = cls(
            name=name,
            description=description,
            requires_restart=requires_restart,
            examples=examples,
            min_value=min_value,
            max_value=max_value,
        )

        postgres_available_parameter_override.additional_properties = d
        return postgres_available_parameter_override

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
