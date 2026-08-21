from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationError")


@_attrs_define
class ValidationError:
    """
    Attributes:
        error (str): The error message
        path (Union[Unset, str]): The path to the field with the error (e.g., `services[0].plan`)
        line (Union[Unset, int]): The line number in the YAML file (1-indexed)
        column (Union[Unset, int]): The column number in the YAML file (1-indexed)
    """

    error: str
    path: Union[Unset, str] = UNSET
    line: Union[Unset, int] = UNSET
    column: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        path = self.path

        line = self.line

        column = self.column

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if line is not UNSET:
            field_dict["line"] = line
        if column is not UNSET:
            field_dict["column"] = column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        path = d.pop("path", UNSET)

        line = d.pop("line", UNSET)

        column = d.pop("column", UNSET)

        validation_error = cls(
            error=error,
            path=path,
            line=line,
            column=column,
        )

        validation_error.additional_properties = d
        return validation_error

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
