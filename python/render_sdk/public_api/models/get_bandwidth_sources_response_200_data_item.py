from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_bandwidth_sources_response_200_data_item_labels import (
        GetBandwidthSourcesResponse200DataItemLabels,
    )
    from ..models.get_bandwidth_sources_response_200_data_item_values_item import (
        GetBandwidthSourcesResponse200DataItemValuesItem,
    )


T = TypeVar("T", bound="GetBandwidthSourcesResponse200DataItem")


@_attrs_define
class GetBandwidthSourcesResponse200DataItem:
    """
    Attributes:
        labels (Union[Unset, GetBandwidthSourcesResponse200DataItemLabels]):
        values (Union[Unset, list['GetBandwidthSourcesResponse200DataItemValuesItem']]):
    """

    labels: Union[Unset, "GetBandwidthSourcesResponse200DataItemLabels"] = UNSET
    values: Union[Unset, list["GetBandwidthSourcesResponse200DataItemValuesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        labels: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        values: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item = values_item_data.to_dict()
                values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if labels is not UNSET:
            field_dict["labels"] = labels
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_bandwidth_sources_response_200_data_item_labels import (
            GetBandwidthSourcesResponse200DataItemLabels,
        )
        from ..models.get_bandwidth_sources_response_200_data_item_values_item import (
            GetBandwidthSourcesResponse200DataItemValuesItem,
        )

        d = dict(src_dict)
        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, GetBandwidthSourcesResponse200DataItemLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = GetBandwidthSourcesResponse200DataItemLabels.from_dict(_labels)

        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:
            values_item = GetBandwidthSourcesResponse200DataItemValuesItem.from_dict(values_item_data)

            values.append(values_item)

        get_bandwidth_sources_response_200_data_item = cls(
            labels=labels,
            values=values,
        )

        get_bandwidth_sources_response_200_data_item.additional_properties = d
        return get_bandwidth_sources_response_200_data_item

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
