from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sandbox import Sandbox


T = TypeVar("T", bound="SandboxWithCursor")


@_attrs_define
class SandboxWithCursor:
    """A sandbox with a cursor

    Attributes:
        sandbox (Sandbox):
        cursor (str):
    """

    sandbox: "Sandbox"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sandbox = self.sandbox.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sandbox": sandbox,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox import Sandbox

        d = dict(src_dict)
        sandbox = Sandbox.from_dict(d.pop("sandbox"))

        cursor = d.pop("cursor")

        sandbox_with_cursor = cls(
            sandbox=sandbox,
            cursor=cursor,
        )

        sandbox_with_cursor.additional_properties = d
        return sandbox_with_cursor

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
