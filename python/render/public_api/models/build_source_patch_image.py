from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildSourcePATCHImage")


@_attrs_define
class BuildSourcePATCHImage:
    """Patch shape for a build source's image identity. Unset fields are left unchanged on the underlying image reference.
    ownerId is intentionally omitted — a build source's owner is fixed at creation, and changing the image's owner would
    amount to a different identity.

        Attributes:
            image_url (Union[Unset, str]):
            registry_credential_id (Union[Unset, str]): Optional reference to the registry credential passed to the image
                repository to retrieve this image. Omit the field to leave the stored credential unchanged; send an empty string
                to clear it.
    """

    image_url: Union[Unset, str] = UNSET
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_url = self.image_url

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_url = d.pop("imageUrl", UNSET)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        build_source_patch_image = cls(
            image_url=image_url,
            registry_credential_id=registry_credential_id,
        )

        build_source_patch_image.additional_properties = d
        return build_source_patch_image

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
