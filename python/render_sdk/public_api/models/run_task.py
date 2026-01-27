from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.task_data_type_1 import TaskDataType1


T = TypeVar("T", bound="RunTask")


@_attrs_define
class RunTask:
    """
    Attributes:
        task (str): Either a task ID or a workflow slug with task name and optional version name. If a version is not
            provided, the latest version of the task will be used. Example: tsk-1234, my-workflow-slug/my-task, my-workflow-
            slug/my-task:SHA123.
        input_ (Union['TaskDataType1', list[Any]]): Input data for a task. Can be either an array (for positional
            arguments) or an object (for named parameters).
    """

    task: str
    input_: Union["TaskDataType1", list[Any]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        input_: Union[dict[str, Any], list[Any]]
        if isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_.to_dict()

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
        from ..models.task_data_type_1 import TaskDataType1

        d = dict(src_dict)
        task = d.pop("task")

        def _parse_input_(data: object) -> Union["TaskDataType1", list[Any]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_task_data_type_0 = cast(list[Any], data)

                return componentsschemas_task_data_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_task_data_type_1 = TaskDataType1.from_dict(data)

            return componentsschemas_task_data_type_1

        input_ = _parse_input_(d.pop("input"))

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
