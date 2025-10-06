from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployImage")


@_attrs_define
class DeployImage:
    """Image information used when creating the deploy. Not present for Git-backed deploys

    Attributes:
        ref (Union[Unset, str]): Image reference used when creating the deploy
        sha (Union[Unset, str]): SHA that the image reference was resolved to when creating the deploy
        registry_credential (Union[Unset, str]): Name of credential used to pull the image, if provided
    """

    ref: Union[Unset, str] = UNSET
    sha: Union[Unset, str] = UNSET
    registry_credential: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ref = self.ref

        sha = self.sha

        registry_credential = self.registry_credential

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ref is not UNSET:
            field_dict["ref"] = ref
        if sha is not UNSET:
            field_dict["sha"] = sha
        if registry_credential is not UNSET:
            field_dict["registryCredential"] = registry_credential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ref = d.pop("ref", UNSET)

        sha = d.pop("sha", UNSET)

        registry_credential = d.pop("registryCredential", UNSET)

        deploy_image = cls(
            ref=ref,
            sha=sha,
            registry_credential=registry_credential,
        )

        deploy_image.additional_properties = d
        return deploy_image

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
