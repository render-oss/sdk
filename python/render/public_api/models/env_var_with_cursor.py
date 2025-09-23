from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.env_var import EnvVar


T = TypeVar("T", bound="EnvVarWithCursor")


@_attrs_define
class EnvVarWithCursor:
    """
    Attributes:
        env_var (EnvVar):
        cursor (str):
    """

    env_var: "EnvVar"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        env_var = self.env_var.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "envVar": env_var,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.env_var import EnvVar

        d = dict(src_dict)
        env_var = EnvVar.from_dict(d.pop("envVar"))

        cursor = d.pop("cursor")

        env_var_with_cursor = cls(
            env_var=env_var,
            cursor=cursor,
        )

        env_var_with_cursor.additional_properties = d
        return env_var_with_cursor

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
