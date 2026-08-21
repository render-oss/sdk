from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationPlanSummary")


@_attrs_define
class ValidationPlanSummary:
    """
    Attributes:
        services (Union[Unset, list[str]]): The names of services that would be created as part of the Blueprint.
        databases (Union[Unset, list[str]]): The names of Render Postgres databases that would be created as part of the
            Blueprint.
        key_value (Union[Unset, list[str]]): The names of Render Key Value instances that would be created as part of
            the Blueprint.
        env_groups (Union[Unset, list[str]]): The names of environment groups that would be created as part of the
            Blueprint.
        total_actions (Union[Unset, int]): The total number of actions that would be performed by the Blueprint. In
            addition to created resources, this includes modifications to individual configuration fields.
    """

    services: Union[Unset, list[str]] = UNSET
    databases: Union[Unset, list[str]] = UNSET
    key_value: Union[Unset, list[str]] = UNSET
    env_groups: Union[Unset, list[str]] = UNSET
    total_actions: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        services: Union[Unset, list[str]] = UNSET
        if not isinstance(self.services, Unset):
            services = self.services

        databases: Union[Unset, list[str]] = UNSET
        if not isinstance(self.databases, Unset):
            databases = self.databases

        key_value: Union[Unset, list[str]] = UNSET
        if not isinstance(self.key_value, Unset):
            key_value = self.key_value

        env_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.env_groups, Unset):
            env_groups = self.env_groups

        total_actions = self.total_actions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if services is not UNSET:
            field_dict["services"] = services
        if databases is not UNSET:
            field_dict["databases"] = databases
        if key_value is not UNSET:
            field_dict["keyValue"] = key_value
        if env_groups is not UNSET:
            field_dict["envGroups"] = env_groups
        if total_actions is not UNSET:
            field_dict["totalActions"] = total_actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        services = cast(list[str], d.pop("services", UNSET))

        databases = cast(list[str], d.pop("databases", UNSET))

        key_value = cast(list[str], d.pop("keyValue", UNSET))

        env_groups = cast(list[str], d.pop("envGroups", UNSET))

        total_actions = d.pop("totalActions", UNSET)

        validation_plan_summary = cls(
            services=services,
            databases=databases,
            key_value=key_value,
            env_groups=env_groups,
            total_actions=total_actions,
        )

        validation_plan_summary.additional_properties = d
        return validation_plan_summary

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
