from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.retry_config import RetryConfig


T = TypeVar("T", bound="TaskOptions")


@_attrs_define
class TaskOptions:
    """
    Attributes:
        retry (Union[Unset, RetryConfig]):
    """

    retry: Union[Unset, "RetryConfig"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        retry: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if retry is not UNSET:
            field_dict["retry"] = retry

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

        task_options = cls(
            retry=retry,
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
