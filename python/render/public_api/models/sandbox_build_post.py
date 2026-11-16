from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_build_post_registry_credential import SandboxBuildPOSTRegistryCredential


T = TypeVar("T", bound="SandboxBuildPOST")


@_attrs_define
class SandboxBuildPOST:
    """The source container image and settings for the sandbox build.

    Attributes:
        name (str): The name used to select this image when creating a sandbox, between 1 and 255 characters. Can't
            start with `sbb-`, the prefix reserved for build IDs. Multiple builds can share a name.
        source_image (str): The container image to convert, specified by tag or digest. Example: python:3.13.
        registry_credential (SandboxBuildPOSTRegistryCredential | Unset): Credentials used to pull `sourceImage` from a
            private registry for this build.
    """

    name: str
    source_image: str
    registry_credential: SandboxBuildPOSTRegistryCredential | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        source_image = self.source_image

        registry_credential: dict[str, Any] | Unset = UNSET
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
        from ..models.sandbox_build_post_registry_credential import SandboxBuildPOSTRegistryCredential  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        source_image = d.pop("sourceImage")

        _registry_credential = d.pop("registryCredential", UNSET)
        registry_credential: SandboxBuildPOSTRegistryCredential | Unset
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
