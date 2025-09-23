from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DockerDetailsPOST")


@_attrs_define
class DockerDetailsPOST:
    """
    Attributes:
        docker_command (Union[Unset, str]):
        docker_context (Union[Unset, str]):
        dockerfile_path (Union[Unset, str]): Defaults to "./Dockerfile"
        registry_credential_id (Union[Unset, str]):
    """

    docker_command: Union[Unset, str] = UNSET
    docker_context: Union[Unset, str] = UNSET
    dockerfile_path: Union[Unset, str] = UNSET
    registry_credential_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        docker_command = self.docker_command

        docker_context = self.docker_context

        dockerfile_path = self.dockerfile_path

        registry_credential_id = self.registry_credential_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if docker_command is not UNSET:
            field_dict["dockerCommand"] = docker_command
        if docker_context is not UNSET:
            field_dict["dockerContext"] = docker_context
        if dockerfile_path is not UNSET:
            field_dict["dockerfilePath"] = dockerfile_path
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        docker_command = d.pop("dockerCommand", UNSET)

        docker_context = d.pop("dockerContext", UNSET)

        dockerfile_path = d.pop("dockerfilePath", UNSET)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        docker_details_post = cls(
            docker_command=docker_command,
            docker_context=docker_context,
            dockerfile_path=dockerfile_path,
            registry_credential_id=registry_credential_id,
        )

        docker_details_post.additional_properties = d
        return docker_details_post

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
