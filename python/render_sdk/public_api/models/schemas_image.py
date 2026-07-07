from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemasImage")


@_attrs_define
class SchemasImage:
    """Present when the artifact source is currently image-based. Mutually exclusive with `build`.

    Attributes:
        image_version_id (Union[Unset, str]):
        sha (Union[Unset, str]):
        ref (Union[Unset, str]):
        image_url (Union[Unset, str]):
        registry_credential_id (Union[Unset, str]):
    """

    image_version_id: Union[Unset, str] = UNSET
    sha: Union[Unset, str] = UNSET
    ref: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_version_id = self.image_version_id

        sha = self.sha

        ref = self.ref

        image_url = self.image_url

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if image_version_id is not UNSET:
            field_dict["imageVersionId"] = image_version_id
        if sha is not UNSET:
            field_dict["SHA"] = sha
        if ref is not UNSET:
            field_dict["ref"] = ref
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_version_id = d.pop("imageVersionId", UNSET)

        sha = d.pop("SHA", UNSET)

        ref = d.pop("ref", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        schemas_image = cls(
            image_version_id=image_version_id,
            sha=sha,
            ref=ref,
            image_url=image_url,
            registry_credential_id=registry_credential_id,
        )

        schemas_image.additional_properties = d
        return schemas_image

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
