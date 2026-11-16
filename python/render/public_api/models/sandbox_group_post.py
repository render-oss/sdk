from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxGroupPOST")


@_attrs_define
class SandboxGroupPOST:
    """The sandbox group to create.

    Attributes:
        owner_id (str): The ID of the workspace to create the sandbox group in. Example: tea-cph1rs3idesc73a2b2mg.
        name (str): The sandbox group's name. Must be unique within the workspace. Example: CI agents.
        region (str | Unset): The Render region where the group's sandboxes run. Defaults to `oregon`. Default:
            'oregon'. Example: oregon.
    """

    owner_id: str
    name: str
    region: str | Unset = "oregon"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        name = self.name

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "name": name,
            }
        )
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        name = d.pop("name")

        region = d.pop("region", UNSET)

        sandbox_group_post = cls(
            owner_id=owner_id,
            name=name,
            region=region,
        )

        sandbox_group_post.additional_properties = d
        return sandbox_group_post

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
