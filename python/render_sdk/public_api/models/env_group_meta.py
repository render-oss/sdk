import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env_group_link import EnvGroupLink


T = TypeVar("T", bound="EnvGroupMeta")


@_attrs_define
class EnvGroupMeta:
    """
    Attributes:
        id (str):
        name (str):
        owner_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        service_links (list['EnvGroupLink']): List of serviceIds linked to the envGroup
        environment_id (Union[Unset, str]):
    """

    id: str
    name: str
    owner_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    service_links: list["EnvGroupLink"]
    environment_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        owner_id = self.owner_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        service_links = []
        for service_links_item_data in self.service_links:
            service_links_item = service_links_item_data.to_dict()
            service_links.append(service_links_item)

        environment_id = self.environment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ownerId": owner_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "serviceLinks": service_links,
            }
        )
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.env_group_link import EnvGroupLink

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        service_links = []
        _service_links = d.pop("serviceLinks")
        for service_links_item_data in _service_links:
            service_links_item = EnvGroupLink.from_dict(service_links_item_data)

            service_links.append(service_links_item)

        environment_id = d.pop("environmentId", UNSET)

        env_group_meta = cls(
            id=id,
            name=name,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            service_links=service_links,
            environment_id=environment_id,
        )

        env_group_meta.additional_properties = d
        return env_group_meta

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
