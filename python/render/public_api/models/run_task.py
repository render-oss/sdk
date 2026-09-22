from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_data_type_1 import TaskDataType1


T = TypeVar("T", bound="RunTask")


@_attrs_define
class RunTask:
    """
    Attributes:
        task (str): A task slug in the format workflow-slug/task-name. An optional version can be appended (workflow-
            slug/task-name:version). If no version is provided, the latest version is used. Cannot be blank. Example: my-
            workflow-slug/my-task, my-workflow-slug/my-task:SHA123.
        input_ (Union['TaskDataType1', list[Any]]): Input data for a task. Can be either an array (for positional
            arguments) or an object (for named parameters).
        idempotency_key (Union[Unset, str]): A client-generated key that makes starting a task run safe to retry.
            Repeating a request with the same key within 24 hours returns the task run that the first request started
            instead of starting another one; the repeated request's input is ignored. Keys are scoped to a single workflow
            version, so the same key used against a different version starts a separate run. Omit the key to always start a
            new run. Example: 6b2f1f7a-6a0e-4f6f-9d1a-2b1d0d5f6c11.
    """

    task: str
    input_: Union["TaskDataType1", list[Any]]
    idempotency_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        input_: Union[dict[str, Any], list[Any]]
        if isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_.to_dict()

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task": task,
                "input": input_,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotencyKey"] = idempotency_key

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

        idempotency_key = d.pop("idempotencyKey", UNSET)

        run_task = cls(
            task=task,
            input_=input_,
            idempotency_key=idempotency_key,
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
