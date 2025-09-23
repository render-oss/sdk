from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Image")


@_attrs_define
class Image:
    """
    Attributes:
        owner_id (str): The ID of the owner for this image. This should match the owner of the service as well as the
            owner of any specified registry credential.
        image_path (str): Path to the image used for this server (e.g docker.io/library/nginx:latest).
        registry_credential_id (Union[Unset, str]): Optional reference to the registry credential passed to the image
            repository to retrieve this image.
    """

    owner_id: str
    image_path: str
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        image_path = self.image_path

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "imagePath": image_path,
            }
        )
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        image_path = d.pop("imagePath")

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        image = cls(
            owner_id=owner_id,
            image_path=image_path,
            registry_credential_id=registry_credential_id,
        )

        image.additional_properties = d
        return image

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
