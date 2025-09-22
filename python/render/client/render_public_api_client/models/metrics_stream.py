from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.otel_provider_type import OtelProviderType

T = TypeVar("T", bound="MetricsStream")


@_attrs_define
class MetricsStream:
    """
    Attributes:
        owner_id (str): The ID of the owner
        provider (OtelProviderType): Provider to send metrics to
        url (str): The endpoint URL to stream metrics to
    """

    owner_id: str
    provider: OtelProviderType
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        provider = self.provider.value

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "provider": provider,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        provider = OtelProviderType(d.pop("provider"))

        url = d.pop("url")

        metrics_stream = cls(
            owner_id=owner_id,
            provider=provider,
            url=url,
        )

        metrics_stream.additional_properties = d
        return metrics_stream

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
