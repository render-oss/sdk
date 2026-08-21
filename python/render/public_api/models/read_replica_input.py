from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.postgres_parameter_overrides import PostgresParameterOverrides


T = TypeVar("T", bound="ReadReplicaInput")


@_attrs_define
class ReadReplicaInput:
    """
    Attributes:
        name (str): The display name of the replica instance.
        parameter_overrides (Union[Unset, PostgresParameterOverrides]):
    """

    name: str
    parameter_overrides: Union[Unset, "PostgresParameterOverrides"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        parameter_overrides: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameter_overrides, Unset):
            parameter_overrides = self.parameter_overrides.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if parameter_overrides is not UNSET:
            field_dict["parameterOverrides"] = parameter_overrides

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_parameter_overrides import PostgresParameterOverrides

        d = dict(src_dict)
        name = d.pop("name")

        _parameter_overrides = d.pop("parameterOverrides", UNSET)
        parameter_overrides: Union[Unset, PostgresParameterOverrides]
        if isinstance(_parameter_overrides, Unset):
            parameter_overrides = UNSET
        else:
            parameter_overrides = PostgresParameterOverrides.from_dict(_parameter_overrides)

        read_replica_input = cls(
            name=name,
            parameter_overrides=parameter_overrides,
        )

        read_replica_input.additional_properties = d
        return read_replica_input

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
