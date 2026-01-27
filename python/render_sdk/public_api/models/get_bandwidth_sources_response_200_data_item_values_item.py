from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBandwidthSourcesResponse200DataItemValuesItem")


@_attrs_define
class GetBandwidthSourcesResponse200DataItemValuesItem:
    """
    Attributes:
        timestamp (Union[Unset, int]):  Example: 1709856000.
        value (Union[Unset, float]):  Example: 100.
    """

    timestamp: Union[Unset, int] = UNSET
    value: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp", UNSET)

        value = d.pop("value", UNSET)

        get_bandwidth_sources_response_200_data_item_values_item = cls(
            timestamp=timestamp,
            value=value,
        )

        get_bandwidth_sources_response_200_data_item_values_item.additional_properties = d
        return get_bandwidth_sources_response_200_data_item_values_item

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
