from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_parameter_overrides import PostgresParameterOverrides


T = TypeVar("T", bound="PostgresPutParameterOverridesResult")


@_attrs_define
class PostgresPutParameterOverridesResult:
    """
    Attributes:
        affected_databases (list[str]): IDs of databases affected by this update (the primary and any read replicas).
        applied_overrides (PostgresParameterOverrides):
        requires_restart (bool): Whether the affected databases must be restarted for the applied overrides to take
            effect.
    """

    affected_databases: list[str]
    applied_overrides: "PostgresParameterOverrides"
    requires_restart: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affected_databases = self.affected_databases

        applied_overrides = self.applied_overrides.to_dict()

        requires_restart = self.requires_restart

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "affectedDatabases": affected_databases,
                "appliedOverrides": applied_overrides,
                "requiresRestart": requires_restart,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_parameter_overrides import PostgresParameterOverrides

        d = dict(src_dict)
        affected_databases = cast(list[str], d.pop("affectedDatabases"))

        applied_overrides = PostgresParameterOverrides.from_dict(d.pop("appliedOverrides"))

        requires_restart = d.pop("requiresRestart")

        postgres_put_parameter_overrides_result = cls(
            affected_databases=affected_databases,
            applied_overrides=applied_overrides,
            requires_restart=requires_restart,
        )

        postgres_put_parameter_overrides_result.additional_properties = d
        return postgres_put_parameter_overrides_result

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
