from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deploy import Deploy


T = TypeVar("T", bound="DeployWithCursor")


@_attrs_define
class DeployWithCursor:
    """
    Attributes:
        deploy (Deploy | Unset):
        cursor (str | Unset):
    """

    deploy: Deploy | Unset = UNSET
    cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deploy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deploy, Unset):
            deploy = self.deploy.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deploy is not UNSET:
            field_dict["deploy"] = deploy
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deploy import Deploy  # noqa: PLC0415

        d = dict(src_dict)
        _deploy = d.pop("deploy", UNSET)
        deploy: Deploy | Unset
        if isinstance(_deploy, Unset):
            deploy = UNSET
        else:
            deploy = Deploy.from_dict(_deploy)

        cursor = d.pop("cursor", UNSET)

        deploy_with_cursor = cls(
            deploy=deploy,
            cursor=cursor,
        )

        deploy_with_cursor.additional_properties = d
        return deploy_with_cursor

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
