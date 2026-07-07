from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.region import Region
from ..types import UNSET, Unset

T = TypeVar("T", bound="DedicatedIPPOST")


@_attrs_define
class DedicatedIPPOST:
    """Input for creating a dedicated IP set.

    Attributes:
        name (str): Name for the dedicated IP set.
        owner_id (str): The ID of the workspace that will own this dedicated IP set.
        region (Region): Defaults to "oregon"
        description (Union[Unset, str]): Free-form description for the dedicated IP set.
        environment_ids (Union[Unset, list[str]]): Environments to scope the dedicated IP set to. If omitted or empty,
            it applies to all services in the workspace within its region.
    """

    name: str
    owner_id: str
    region: Region
    description: Union[Unset, str] = UNSET
    environment_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        owner_id = self.owner_id

        region = self.region.value

        description = self.description

        environment_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.environment_ids, Unset):
            environment_ids = self.environment_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "region": region,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if environment_ids is not UNSET:
            field_dict["environmentIds"] = environment_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        region = Region(d.pop("region"))

        description = d.pop("description", UNSET)

        environment_ids = cast(list[str], d.pop("environmentIds", UNSET))

        dedicated_ippost = cls(
            name=name,
            owner_id=owner_id,
            region=region,
            description=description,
            environment_ids=environment_ids,
        )

        dedicated_ippost.additional_properties = d
        return dedicated_ippost

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
