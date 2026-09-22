from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlueprintSource")


@_attrs_define
class BlueprintSource:
    """
    Attributes:
        repo (str): URL of the connected Git repository. Example: https://github.com/my-username/my-repository.
        branch (Union[Unset, str]): Branch to read. Defaults to the repository default branch.
        path (Union[Unset, str]): Path to the Blueprint file in the repository. Default: 'render.yaml'.
    """

    repo: str
    branch: Union[Unset, str] = UNSET
    path: Union[Unset, str] = "render.yaml"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repo = self.repo

        branch = self.branch

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repo": repo,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo = d.pop("repo")

        branch = d.pop("branch", UNSET)

        path = d.pop("path", UNSET)

        blueprint_source = cls(
            repo=repo,
            branch=branch,
            path=path,
        )

        blueprint_source.additional_properties = d
        return blueprint_source

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
