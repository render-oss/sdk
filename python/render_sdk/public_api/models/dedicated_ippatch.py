from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DedicatedIPPATCH")


@_attrs_define
class DedicatedIPPATCH:
    """Input for updating a dedicated IP set. All fields are optional. Omitted fields are left unchanged. Provide
    `environmentIds: []` to switch from environment-scoped to workspace-scoped.

        Attributes:
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            environment_ids (Union[Unset, list[str]]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    environment_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        environment_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.environment_ids, Unset):
            environment_ids = self.environment_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if environment_ids is not UNSET:
            field_dict["environmentIds"] = environment_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        environment_ids = cast(list[str], d.pop("environmentIds", UNSET))

        dedicated_ippatch = cls(
            name=name,
            description=description,
            environment_ids=environment_ids,
        )

        dedicated_ippatch.additional_properties = d
        return dedicated_ippatch

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
