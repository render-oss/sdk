from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageVersion")


@_attrs_define
class ImageVersion:
    """
    Attributes:
        image_path (str): Path to the image used for this server (e.g docker.io/library/nginx:latest).
        sha (str): SHA that the image reference was resolved to when creating the workflow version.
        registry_credential_id (Union[Unset, str]): Optional reference to the registry credential passed to the image
            repository to retrieve this image.
    """

    image_path: str
    sha: str
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_path = self.image_path

        sha = self.sha

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imagePath": image_path,
                "sha": sha,
            }
        )
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_path = d.pop("imagePath")

        sha = d.pop("sha")

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        image_version = cls(
            image_path=image_path,
            sha=sha,
            registry_credential_id=registry_credential_id,
        )

        image_version.additional_properties = d
        return image_version

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
