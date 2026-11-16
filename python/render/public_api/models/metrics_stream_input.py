from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.otel_provider_type import OtelProviderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricsStreamInput")


@_attrs_define
class MetricsStreamInput:
    """Input for creating or updating a metrics stream

    Attributes:
        provider (OtelProviderType | Unset): Provider to send metrics to
        url (str | Unset): The endpoint URL to stream metrics to
        token (str | Unset): Authentication token for the metrics stream
    """

    provider: OtelProviderType | Unset = UNSET
    url: str | Unset = UNSET
    token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider: str | Unset = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        url = self.url

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider is not UNSET:
            field_dict["provider"] = provider
        if url is not UNSET:
            field_dict["url"] = url
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _provider = d.pop("provider", UNSET)
        provider: OtelProviderType | Unset
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = OtelProviderType(_provider)

        url = d.pop("url", UNSET)

        token = d.pop("token", UNSET)

        metrics_stream_input = cls(
            provider=provider,
            url=url,
            token=token,
        )

        metrics_stream_input.additional_properties = d
        return metrics_stream_input

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
