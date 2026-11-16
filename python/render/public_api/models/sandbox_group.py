from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxGroup")


@_attrs_define
class SandboxGroup:
    """A group of sandboxes in a workspace that share a region, concurrency limit, and credentials.

    Attributes:
        id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        owner_id (str): The ID of the workspace this group belongs to. Example: tea-cph1rs3idesc73a2b2mg.
        name (str): The sandbox group's name. Example: Default.
        region (str): The Render region where the group's sandboxes run. Example: oregon.
        is_default (bool): Whether this is the workspace's default sandbox group. Create requests that omit
            `sandboxGroupId` use this group.
        concurrency_limit (int): The maximum number of active sandboxes allowed in this group, capped by Render's limit
            for the workspace.
        created_at (datetime.datetime): The timestamp when the sandbox group was created, in ISO 8601 format. Example:
            2026-07-02T18:30:00Z.
        updated_at (datetime.datetime): The timestamp when the sandbox group was last updated, in ISO 8601 format.
            Example: 2026-07-02T18:30:00Z.
        environment_id (None | str | Unset): The ID of the environment this sandbox group belongs to, if any.
    """

    id: str
    owner_id: str
    name: str
    region: str
    is_default: bool
    concurrency_limit: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    environment_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        owner_id = self.owner_id

        name = self.name

        region = self.region

        is_default = self.is_default

        concurrency_limit = self.concurrency_limit

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        environment_id: None | str | Unset
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
                "concurrencyLimit": concurrency_limit,
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

        concurrency_limit = d.pop("concurrencyLimit")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        def _parse_environment_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment_id = _parse_environment_id(d.pop("environmentId", UNSET))

        sandbox_group = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            region=region,
            is_default=is_default,
            concurrency_limit=concurrency_limit,
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
