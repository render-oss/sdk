from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_bandwidth_sources_response_200_data_item_labels_traffic_source import (
    GetBandwidthSourcesResponse200DataItemLabelsTrafficSource,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBandwidthSourcesResponse200DataItemLabels")


@_attrs_define
class GetBandwidthSourcesResponse200DataItemLabels:
    """
    Attributes:
        resource (Union[Unset, str]):  Example: srv-abc123.
        traffic_source (Union[Unset, GetBandwidthSourcesResponse200DataItemLabelsTrafficSource]):  Example: http.
    """

    resource: Union[Unset, str] = UNSET
    traffic_source: Union[Unset, GetBandwidthSourcesResponse200DataItemLabelsTrafficSource] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource

        traffic_source: Union[Unset, str] = UNSET
        if not isinstance(self.traffic_source, Unset):
            traffic_source = self.traffic_source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource is not UNSET:
            field_dict["resource"] = resource
        if traffic_source is not UNSET:
            field_dict["trafficSource"] = traffic_source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource = d.pop("resource", UNSET)

        _traffic_source = d.pop("trafficSource", UNSET)
        traffic_source: Union[Unset, GetBandwidthSourcesResponse200DataItemLabelsTrafficSource]
        if isinstance(_traffic_source, Unset):
            traffic_source = UNSET
        else:
            traffic_source = GetBandwidthSourcesResponse200DataItemLabelsTrafficSource(_traffic_source)

        get_bandwidth_sources_response_200_data_item_labels = cls(
            resource=resource,
            traffic_source=traffic_source,
        )

        get_bandwidth_sources_response_200_data_item_labels.additional_properties = d
        return get_bandwidth_sources_response_200_data_item_labels

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
