from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunTask")


@_attrs_define
class RunTask:
    """
    Attributes:
        task (str): Either a task ID or a workflow slug with task name and optional version. If a version is not
            provided, the latest version of the task will be used.
        input_ (list[Any]):
    """

    task: str
    input_: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        input_ = self.input_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task": task,
                "input": input_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        task = d.pop("task")

        input_ = cast(list[Any], d.pop("input"))

        run_task = cls(
            task=task,
            input_=input_,
        )

        run_task.additional_properties = d
        return run_task

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
