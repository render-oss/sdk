from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactSourceImage")


@_attrs_define
class ArtifactSourceImage:
    """
    Attributes:
        owner_id (str):
        image_url (str):
        registry_credential_id (Union[Unset, str]):
    """

    owner_id: str
    image_url: str
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        image_url = self.image_url

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "imageUrl": image_url,
            }
        )
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        image_url = d.pop("imageUrl")

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        artifact_source_image = cls(
            owner_id=owner_id,
            image_url=image_url,
            registry_credential_id=registry_credential_id,
        )

        artifact_source_image.additional_properties = d
        return artifact_source_image

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
