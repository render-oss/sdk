from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_options import TaskOptions
    from ..models.task_parameter import TaskParameter


T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """
    Attributes:
        name (str):
        options (Union[Unset, TaskOptions]):
        parameters (Union[Unset, list['TaskParameter']]): Parameter schema extracted from the task function signature
    """

    name: str
    options: Union[Unset, "TaskOptions"] = UNSET
    parameters: Union[Unset, list["TaskParameter"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        parameters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.task_options import TaskOptions
        from ..models.task_parameter import TaskParameter

        d = dict(src_dict)
        name = d.pop("name")

        _options = d.pop("options", UNSET)
        options: Union[Unset, TaskOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = TaskOptions.from_dict(_options)

        parameters = []
        _parameters = d.pop("parameters", UNSET)
        for parameters_item_data in _parameters or []:
            parameters_item = TaskParameter.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        task = cls(
            name=name,
            options=options,
            parameters=parameters,
        )

        task.additional_properties = d
        return task

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
