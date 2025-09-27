from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_complete import TaskComplete
    from ..models.task_error import TaskError


T = TypeVar("T", bound="CallbackRequest")


@_attrs_define
class CallbackRequest:
    """
    Attributes:
        error (Union[Unset, TaskError]):
        complete (Union[Unset, TaskComplete]):
    """

    error: Union[Unset, "TaskError"] = UNSET
    complete: Union[Unset, "TaskComplete"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        complete: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.complete, Unset):
            complete = self.complete.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if complete is not UNSET:
            field_dict["complete"] = complete

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.task_complete import TaskComplete
        from ..models.task_error import TaskError

        d = dict(src_dict)
        _error = d.pop("error", UNSET)
        error: Union[Unset, TaskError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = TaskError.from_dict(_error)

        _complete = d.pop("complete", UNSET)
        complete: Union[Unset, TaskComplete]
        if isinstance(_complete, Unset):
            complete = UNSET
        else:
            complete = TaskComplete.from_dict(_complete)

        callback_request = cls(
            error=error,
            complete=complete,
        )

        callback_request.additional_properties = d
        return callback_request

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
