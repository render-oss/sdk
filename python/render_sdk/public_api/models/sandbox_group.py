import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxGroup")


@_attrs_define
class SandboxGroup:
    """
    Attributes:
        id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        owner_id (str): The ID of the workspace this group belongs to. Example: tea-cph1rs3idesc73a2b2mg.
        name (str): Human-friendly name for the group. Example: Default.
        region (str): Render region the group operates in. Example: oregon.
        is_default (bool): Whether this is the workspace's default group. Exactly one group per workspace is the
            default.
        created_at (datetime.datetime):  Example: 2026-07-02T18:30:00Z.
        updated_at (datetime.datetime):  Example: 2026-07-02T18:30:00Z.
        environment_id (Union[None, Unset, str]): Environment this group is bound to.
    """

    id: str
    owner_id: str
    name: str
    region: str
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    environment_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        owner_id = self.owner_id

        name = self.name

        region = self.region

        is_default = self.is_default

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        environment_id: Union[None, Unset, str]
        if isinstance(self.environment_id, Unset):
            environment_id = UNSET
        else:
            environment_id = self.environment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ownerId": owner_id,
                "name": name,
                "region": region,
                "isDefault": is_default,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        owner_id = d.pop("ownerId")

        name = d.pop("name")

        region = d.pop("region")

        is_default = d.pop("isDefault")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_environment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        environment_id = _parse_environment_id(d.pop("environmentId", UNSET))

        sandbox_group = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            region=region,
            is_default=is_default,
            created_at=created_at,
            updated_at=updated_at,
            environment_id=environment_id,
        )

        sandbox_group.additional_properties = d
        return sandbox_group

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
