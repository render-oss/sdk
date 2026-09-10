from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.runtime import Runtime
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildConfigUpdate")


@_attrs_define
class BuildConfigUpdate:
    """A partial update to a workflow's build config. Every field is optional; omitted fields are left unchanged.

    Attributes:
        branch (Union[Unset, str]): The branch to use for the build, if applicable.
        build_command (Union[Unset, str]): The command to run to build the workflow. Required for every runtime except
            docker, which builds from its Dockerfile.
        repo (Union[Unset, str]): The repository URL to use for the build. Cannot be blank.
        root_dir (Union[Unset, str]): The root directory of the repository to use for the build, if applicable.
        runtime (Union[Unset, Runtime]): The runtime environment for the workflow (e.g., node, python, etc.).
    """

    branch: Union[Unset, str] = UNSET
    build_command: Union[Unset, str] = UNSET
    repo: Union[Unset, str] = UNSET
    root_dir: Union[Unset, str] = UNSET
    runtime: Union[Unset, Runtime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        branch = self.branch

        build_command = self.build_command

        repo = self.repo

        root_dir = self.root_dir

        runtime: Union[Unset, str] = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if branch is not UNSET:
            field_dict["branch"] = branch
        if build_command is not UNSET:
            field_dict["buildCommand"] = build_command
        if repo is not UNSET:
            field_dict["repo"] = repo
        if root_dir is not UNSET:
            field_dict["rootDir"] = root_dir
        if runtime is not UNSET:
            field_dict["runtime"] = runtime

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        branch = d.pop("branch", UNSET)

        build_command = d.pop("buildCommand", UNSET)

        repo = d.pop("repo", UNSET)

        root_dir = d.pop("rootDir", UNSET)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = Runtime(_runtime)

        build_config_update = cls(
            branch=branch,
            build_command=build_command,
            repo=repo,
            root_dir=root_dir,
            runtime=runtime,
        )

        build_config_update.additional_properties = d
        return build_config_update

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
