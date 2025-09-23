import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.owner import Owner


T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """A project is a collection of environments

    Attributes:
        id (str): The ID of the project
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str): The name of the project
        owner (Owner):
        environment_ids (list[str]): The environments associated with the project
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    owner: "Owner"
    environment_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        owner = self.owner.to_dict()

        environment_ids = self.environment_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "name": name,
                "owner": owner,
                "environmentIds": environment_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.owner import Owner

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        name = d.pop("name")

        owner = Owner.from_dict(d.pop("owner"))

        environment_ids = cast(list[str], d.pop("environmentIds"))

        project = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            owner=owner,
            environment_ids=environment_ids,
        )

        project.additional_properties = d
        return project

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
