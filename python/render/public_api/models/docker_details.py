from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.registry_credential import RegistryCredential


T = TypeVar("T", bound="DockerDetails")


@_attrs_define
class DockerDetails:
    """
    Attributes:
        docker_command (str):
        docker_context (str):
        dockerfile_path (str):
        pre_deploy_command (Union[Unset, str]):
        registry_credential (Union[Unset, RegistryCredential]):
    """

    docker_command: str
    docker_context: str
    dockerfile_path: str
    pre_deploy_command: Union[Unset, str] = UNSET
    registry_credential: Union[Unset, "RegistryCredential"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        docker_command = self.docker_command

        docker_context = self.docker_context

        dockerfile_path = self.dockerfile_path

        pre_deploy_command = self.pre_deploy_command

        registry_credential: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.registry_credential, Unset):
            registry_credential = self.registry_credential.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dockerCommand": docker_command,
                "dockerContext": docker_context,
                "dockerfilePath": dockerfile_path,
            }
        )
        if pre_deploy_command is not UNSET:
            field_dict["preDeployCommand"] = pre_deploy_command
        if registry_credential is not UNSET:
            field_dict["registryCredential"] = registry_credential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registry_credential import RegistryCredential

        d = dict(src_dict)
        docker_command = d.pop("dockerCommand")

        docker_context = d.pop("dockerContext")

        dockerfile_path = d.pop("dockerfilePath")

        pre_deploy_command = d.pop("preDeployCommand", UNSET)

        _registry_credential = d.pop("registryCredential", UNSET)
        registry_credential: Union[Unset, RegistryCredential]
        if isinstance(_registry_credential, Unset):
            registry_credential = UNSET
        else:
            registry_credential = RegistryCredential.from_dict(_registry_credential)

        docker_details = cls(
            docker_command=docker_command,
            docker_context=docker_context,
            dockerfile_path=dockerfile_path,
            pre_deploy_command=pre_deploy_command,
            registry_credential=registry_credential,
        )

        docker_details.additional_properties = d
        return docker_details

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
