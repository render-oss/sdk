from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_parameter_overrides import PostgresParameterOverrides


T = TypeVar("T", bound="PostgresParameterOverridesWrapper")


@_attrs_define
class PostgresParameterOverridesWrapper:
    """
    Attributes:
        parameter_overrides (PostgresParameterOverrides):
    """

    parameter_overrides: "PostgresParameterOverrides"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parameter_overrides = self.parameter_overrides.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameterOverrides": parameter_overrides,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_parameter_overrides import PostgresParameterOverrides

        d = dict(src_dict)
        parameter_overrides = PostgresParameterOverrides.from_dict(d.pop("parameterOverrides"))

        postgres_parameter_overrides_wrapper = cls(
            parameter_overrides=parameter_overrides,
        )

        postgres_parameter_overrides_wrapper.additional_properties = d
        return postgres_parameter_overrides_wrapper

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
