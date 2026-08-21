from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_available_parameter_override import PostgresAvailableParameterOverride


T = TypeVar("T", bound="PostgresAvailableParameterOverridesResult")


@_attrs_define
class PostgresAvailableParameterOverridesResult:
    """
    Attributes:
        available_parameter_overrides (list['PostgresAvailableParameterOverride']):
    """

    available_parameter_overrides: list["PostgresAvailableParameterOverride"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available_parameter_overrides = []
        for available_parameter_overrides_item_data in self.available_parameter_overrides:
            available_parameter_overrides_item = available_parameter_overrides_item_data.to_dict()
            available_parameter_overrides.append(available_parameter_overrides_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "availableParameterOverrides": available_parameter_overrides,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_available_parameter_override import PostgresAvailableParameterOverride

        d = dict(src_dict)
        available_parameter_overrides = []
        _available_parameter_overrides = d.pop("availableParameterOverrides")
        for available_parameter_overrides_item_data in _available_parameter_overrides:
            available_parameter_overrides_item = PostgresAvailableParameterOverride.from_dict(
                available_parameter_overrides_item_data
            )

            available_parameter_overrides.append(available_parameter_overrides_item)

        postgres_available_parameter_overrides_result = cls(
            available_parameter_overrides=available_parameter_overrides,
        )

        postgres_available_parameter_overrides_result.additional_properties = d
        return postgres_available_parameter_overrides_result

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
