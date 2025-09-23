from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_type import EventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookPATCHInput")


@_attrs_define
class WebhookPATCHInput:
    """
    Attributes:
        name (Union[Unset, str]):
        url (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        event_filter (Union[Unset, list[EventType]]): The event types that will trigger the webhook. An empty list means
            all event types will trigger the webhook.
    """

    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    event_filter: Union[Unset, list[EventType]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        url = self.url

        enabled = self.enabled

        event_filter: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_filter, Unset):
            event_filter = []
            for componentsschemasevent_filter_item_data in self.event_filter:
                componentsschemasevent_filter_item = componentsschemasevent_filter_item_data.value
                event_filter.append(componentsschemasevent_filter_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if event_filter is not UNSET:
            field_dict["eventFilter"] = event_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        enabled = d.pop("enabled", UNSET)

        event_filter = []
        _event_filter = d.pop("eventFilter", UNSET)
        for componentsschemasevent_filter_item_data in _event_filter or []:
            componentsschemasevent_filter_item = EventType(componentsschemasevent_filter_item_data)

            event_filter.append(componentsschemasevent_filter_item)

        webhook_patch_input = cls(
            name=name,
            url=url,
            enabled=enabled,
            event_filter=event_filter,
        )

        webhook_patch_input.additional_properties = d
        return webhook_patch_input

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
