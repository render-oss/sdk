from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_build_post_registry_credential import SandboxBuildPOSTRegistryCredential


T = TypeVar("T", bound="SandboxBuildPOST")


@_attrs_define
class SandboxBuildPOST:
    """
    Attributes:
        name (str): Names the image. Every build of an image shares it.
        source_image (str): The image to convert, by tag or digest. Example: python:3.13.
        registry_credential (Union[Unset, SandboxBuildPOSTRegistryCredential]): Pulls `sourceImage` from a private
            registry. Used for this build only and never stored.
    """

    name: str
    source_image: str
    registry_credential: Union[Unset, "SandboxBuildPOSTRegistryCredential"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        source_image = self.source_image

        registry_credential: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.registry_credential, Unset):
            registry_credential = self.registry_credential.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "sourceImage": source_image,
            }
        )
        if registry_credential is not UNSET:
            field_dict["registryCredential"] = registry_credential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_build_post_registry_credential import SandboxBuildPOSTRegistryCredential

        d = dict(src_dict)
        name = d.pop("name")

        source_image = d.pop("sourceImage")

        _registry_credential = d.pop("registryCredential", UNSET)
        registry_credential: Union[Unset, SandboxBuildPOSTRegistryCredential]
        if isinstance(_registry_credential, Unset):
            registry_credential = UNSET
        else:
            registry_credential = SandboxBuildPOSTRegistryCredential.from_dict(_registry_credential)

        sandbox_build_post = cls(
            name=name,
            source_image=source_image,
            registry_credential=registry_credential,
        )

        sandbox_build_post.additional_properties = d
        return sandbox_build_post

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
