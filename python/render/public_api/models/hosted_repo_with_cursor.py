from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.hosted_repo import HostedRepo


T = TypeVar("T", bound="HostedRepoWithCursor")


@_attrs_define
class HostedRepoWithCursor:
    """
    Attributes:
        cursor (str):
        hosted_repo (HostedRepo):
    """

    cursor: str
    hosted_repo: HostedRepo
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cursor = self.cursor

        hosted_repo = self.hosted_repo.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cursor": cursor,
                "hostedRepo": hosted_repo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hosted_repo import HostedRepo  # noqa: PLC0415

        d = dict(src_dict)
        cursor = d.pop("cursor")

        hosted_repo = HostedRepo.from_dict(d.pop("hostedRepo"))

        hosted_repo_with_cursor = cls(
            cursor=cursor,
            hosted_repo=hosted_repo,
        )

        hosted_repo_with_cursor.additional_properties = d
        return hosted_repo_with_cursor

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
