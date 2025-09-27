from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetryConfig")


@_attrs_define
class RetryConfig:
    """
    Attributes:
        max_retries (Union[Unset, int]): Maximum number of retry attempts
        wait_duration_ms (Union[Unset, int]): Initial wait duration between retries (in milliseconds)
        factor (Union[Unset, float]): Backoff factor for exponential retry
    """

    max_retries: Union[Unset, int] = UNSET
    wait_duration_ms: Union[Unset, int] = UNSET
    factor: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_retries = self.max_retries

        wait_duration_ms = self.wait_duration_ms

        factor = self.factor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_retries is not UNSET:
            field_dict["max_retries"] = max_retries
        if wait_duration_ms is not UNSET:
            field_dict["wait_duration_ms"] = wait_duration_ms
        if factor is not UNSET:
            field_dict["factor"] = factor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_retries = d.pop("max_retries", UNSET)

        wait_duration_ms = d.pop("wait_duration_ms", UNSET)

        factor = d.pop("factor", UNSET)

        retry_config = cls(
            max_retries=max_retries,
            wait_duration_ms=wait_duration_ms,
            factor=factor,
        )

        retry_config.additional_properties = d
        return retry_config

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
