from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="EdgeCacheTrigger")


@_attrs_define
class EdgeCacheTrigger:
    """
    Attributes:
        manual (bool): Edge Cache change was triggered manually from the dashboard
        system (bool): Edge Cache Change was triggered by Render
        user (SchemasUser | Unset): User who triggered the action
    """

    manual: bool
    system: bool
    user: SchemasUser | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        manual = self.manual

        system = self.system

        user: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "manual": manual,
                "system": system,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_user import SchemasUser  # noqa: PLC0415

        d = dict(src_dict)
        manual = d.pop("manual")

        system = d.pop("system")

        _user = d.pop("user", UNSET)
        user: SchemasUser | Unset
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = SchemasUser.from_dict(_user)

        edge_cache_trigger = cls(
            manual=manual,
            system=system,
            user=user,
        )

        edge_cache_trigger.additional_properties = d
        return edge_cache_trigger

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
