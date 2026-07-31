from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sandbox_group import SandboxGroup


T = TypeVar("T", bound="SandboxGroupWithCursor")


@_attrs_define
class SandboxGroupWithCursor:
    """A sandbox group with a cursor

    Attributes:
        sandbox_group (SandboxGroup):
        cursor (str):
    """

    sandbox_group: "SandboxGroup"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sandbox_group = self.sandbox_group.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sandboxGroup": sandbox_group,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_group import SandboxGroup

        d = dict(src_dict)
        sandbox_group = SandboxGroup.from_dict(d.pop("sandboxGroup"))

        cursor = d.pop("cursor")

        sandbox_group_with_cursor = cls(
            sandbox_group=sandbox_group,
            cursor=cursor,
        )

        sandbox_group_with_cursor.additional_properties = d
        return sandbox_group_with_cursor

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
