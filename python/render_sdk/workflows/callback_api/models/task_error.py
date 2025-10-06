from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskError")


@_attrs_define
class TaskError:
    """
    Attributes:
        details (str):
        stack_trace (Union[Unset, str]):
    """

    details: str
    stack_trace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        details = self.details

        stack_trace = self.stack_trace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "details": details,
            }
        )
        if stack_trace is not UNSET:
            field_dict["stack_trace"] = stack_trace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        details = d.pop("details")

        stack_trace = d.pop("stack_trace", UNSET)

        task_error = cls(
            details=details,
            stack_trace=stack_trace,
        )

        task_error.additional_properties = d
        return task_error

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
