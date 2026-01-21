from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.task_options_plan import TaskOptionsPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.retry_config import RetryConfig


T = TypeVar("T", bound="TaskOptions")


@_attrs_define
class TaskOptions:
    """
    Attributes:
        retry (Union[Unset, RetryConfig]):
        timeout_seconds (Union[Unset, int]): Task execution timeout in seconds (30-86400)
        plan (Union[Unset, TaskOptionsPlan]): Resource plan for task execution
    """

    retry: Union[Unset, "RetryConfig"] = UNSET
    timeout_seconds: Union[Unset, int] = UNSET
    plan: Union[Unset, TaskOptionsPlan] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        retry: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        timeout_seconds = self.timeout_seconds

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if retry is not UNSET:
            field_dict["retry"] = retry
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.retry_config import RetryConfig

        d = dict(src_dict)
        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, RetryConfig]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = RetryConfig.from_dict(_retry)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, TaskOptionsPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = TaskOptionsPlan(_plan)

        task_options = cls(
            retry=retry,
            timeout_seconds=timeout_seconds,
            plan=plan,
        )

        task_options.additional_properties = d
        return task_options

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
