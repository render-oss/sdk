from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.registry_credential_registry import RegistryCredentialRegistry

T = TypeVar("T", bound="CreateRegistryCredentialBody")


@_attrs_define
class CreateRegistryCredentialBody:
    """
    Attributes:
        registry (RegistryCredentialRegistry): The registry to use this credential with
        name (str):
        username (str):
        auth_token (str):
        owner_id (str):
    """

    registry: RegistryCredentialRegistry
    name: str
    username: str
    auth_token: str
    owner_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        registry = self.registry.value

        name = self.name

        username = self.username

        auth_token = self.auth_token

        owner_id = self.owner_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "registry": registry,
                "name": name,
                "username": username,
                "authToken": auth_token,
                "ownerId": owner_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        registry = RegistryCredentialRegistry(d.pop("registry"))

        name = d.pop("name")

        username = d.pop("username")

        auth_token = d.pop("authToken")

        owner_id = d.pop("ownerId")

        create_registry_credential_body = cls(
            registry=registry,
            name=name,
            username=username,
            auth_token=auth_token,
            owner_id=owner_id,
        )

        create_registry_credential_body.additional_properties = d
        return create_registry_credential_body

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
