import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.registry_credential_registry import RegistryCredentialRegistry

T = TypeVar("T", bound="RegistryCredential")


@_attrs_define
class RegistryCredential:
    """
    Attributes:
        id (str): Unique identifier for this credential
        name (str): Descriptive name for this credential
        registry (RegistryCredentialRegistry): The registry to use this credential with
        username (str): The username associated with the credential
        updated_at (datetime.datetime): Last updated time for the credential
    """

    id: str
    name: str
    registry: RegistryCredentialRegistry
    username: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        registry = self.registry.value

        username = self.username

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "registry": registry,
                "username": username,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        registry = RegistryCredentialRegistry(d.pop("registry"))

        username = d.pop("username")

        updated_at = isoparse(d.pop("updatedAt"))

        registry_credential = cls(
            id=id,
            name=name,
            registry=registry,
            username=username,
            updated_at=updated_at,
        )

        registry_credential.additional_properties = d
        return registry_credential

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
