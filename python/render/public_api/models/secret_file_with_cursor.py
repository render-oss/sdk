from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.secret_file import SecretFile


T = TypeVar("T", bound="SecretFileWithCursor")


@_attrs_define
class SecretFileWithCursor:
    """
    Attributes:
        secret_file (SecretFile):
        cursor (str):
    """

    secret_file: "SecretFile"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secret_file = self.secret_file.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secretFile": secret_file,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.secret_file import SecretFile

        d = dict(src_dict)
        secret_file = SecretFile.from_dict(d.pop("secretFile"))

        cursor = d.pop("cursor")

        secret_file_with_cursor = cls(
            secret_file=secret_file,
            cursor=cursor,
        )

        secret_file_with_cursor.additional_properties = d
        return secret_file_with_cursor

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
