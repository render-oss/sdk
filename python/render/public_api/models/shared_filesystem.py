import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SharedFilesystem")


@_attrs_define
class SharedFilesystem:
    """
    Attributes:
        id (str):  Example: sfs-cph1rs3idesc73a2b2mg.
        owner_id (str): The ID of the workspace this filesystem belongs to. Example: tea-cph1rs3idesc73a2b2mg.
        name (str): Name of the filesystem, unique in the workspace. Workloads mount
            the filesystem by this name.
             Example: data.
        region (str): Render region the filesystem lives in. Only workloads in this
            region can mount it.
             Example: oregon.
        created_at (datetime.datetime):  Example: 2026-10-22T18:30:00Z.
    """

    id: str
    owner_id: str
    name: str
    region: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        owner_id = self.owner_id

        name = self.name

        region = self.region

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ownerId": owner_id,
                "name": name,
                "region": region,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        owner_id = d.pop("ownerId")

        name = d.pop("name")

        region = d.pop("region")

        created_at = isoparse(d.pop("createdAt"))

        shared_filesystem = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            region=region,
            created_at=created_at,
        )

        shared_filesystem.additional_properties = d
        return shared_filesystem

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
