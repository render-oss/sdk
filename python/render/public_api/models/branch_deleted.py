from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BranchDeleted")


@_attrs_define
class BranchDeleted:
    """
    Attributes:
        deleted_branch (str):
        new_branch (str):
    """

    deleted_branch: str
    new_branch: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_branch = self.deleted_branch

        new_branch = self.new_branch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deletedBranch": deleted_branch,
                "newBranch": new_branch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deleted_branch = d.pop("deletedBranch")

        new_branch = d.pop("newBranch")

        branch_deleted = cls(
            deleted_branch=deleted_branch,
            new_branch=new_branch,
        )

        branch_deleted.additional_properties = d
        return branch_deleted

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
