from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.runtime import Runtime
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildConfig")


@_attrs_define
class BuildConfig:
    """
    Attributes:
        build_command (str): The command to run to build the workflow.
        repo (str): The repository URL to use for the build.
        runtime (Runtime): The runtime environment for the workflow (e.g., node, python, etc.).
        branch (Union[Unset, str]): The branch to use for the build, if applicable.
        root_dir (Union[Unset, str]): The root directory of the repository to use for the build, if applicable.
    """

    build_command: str
    repo: str
    runtime: Runtime
    branch: Union[Unset, str] = UNSET
    root_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        repo = self.repo

        runtime = self.runtime.value

        branch = self.branch

        root_dir = self.root_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buildCommand": build_command,
                "repo": repo,
                "runtime": runtime,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch
        if root_dir is not UNSET:
            field_dict["rootDir"] = root_dir

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        build_command = d.pop("buildCommand")

        repo = d.pop("repo")

        runtime = Runtime(d.pop("runtime"))

        branch = d.pop("branch", UNSET)

        root_dir = d.pop("rootDir", UNSET)

        build_config = cls(
            build_command=build_command,
            repo=repo,
            runtime=runtime,
            branch=branch,
            root_dir=root_dir,
        )

        build_config.additional_properties = d
        return build_config

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
