from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HostedRepoPOSTInput")


@_attrs_define
class HostedRepoPOSTInput:
    """
    Attributes:
        owner_id (str):  Example: tea-cph1rs3idesc73a2b2mg.
        name (str): Up to 100 lowercase letters, digits, `.`, `_` or `-`, starting with a letter or digit and not ending
            in `.git` Example: bookmarks.
        default_branch (str | Unset): The branch a clone checks out. Defaults to `main`. Example: main.
    """

    owner_id: str
    name: str
    default_branch: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        name = self.name

        default_branch = self.default_branch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "name": name,
            }
        )
        if default_branch is not UNSET:
            field_dict["defaultBranch"] = default_branch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        name = d.pop("name")

        default_branch = d.pop("defaultBranch", UNSET)

        hosted_repo_post_input = cls(
            owner_id=owner_id,
            name=name,
            default_branch=default_branch,
        )

        hosted_repo_post_input.additional_properties = d
        return hosted_repo_post_input

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
