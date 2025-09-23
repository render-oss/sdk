from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_type import EventType

T = TypeVar("T", bound="WebhookPOSTInput")


@_attrs_define
class WebhookPOSTInput:
    """
    Attributes:
        owner_id (str): The ID of the owner (team or personal user) whose resources should be returned
        url (str):
        name (str):
        enabled (bool):
        event_filter (list[EventType]): The event types that will trigger the webhook. An empty list means all event
            types will trigger the webhook.
    """

    owner_id: str
    url: str
    name: str
    enabled: bool
    event_filter: list[EventType]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        url = self.url

        name = self.name

        enabled = self.enabled

        event_filter = []
        for componentsschemasevent_filter_item_data in self.event_filter:
            componentsschemasevent_filter_item = componentsschemasevent_filter_item_data.value
            event_filter.append(componentsschemasevent_filter_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "url": url,
                "name": name,
                "enabled": enabled,
                "eventFilter": event_filter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        url = d.pop("url")

        name = d.pop("name")

        enabled = d.pop("enabled")

        event_filter = []
        _event_filter = d.pop("eventFilter")
        for componentsschemasevent_filter_item_data in _event_filter:
            componentsschemasevent_filter_item = EventType(componentsschemasevent_filter_item_data)

            event_filter.append(componentsschemasevent_filter_item)

        webhook_post_input = cls(
            owner_id=owner_id,
            url=url,
            name=name,
            enabled=enabled,
            event_filter=event_filter,
        )

        webhook_post_input.additional_properties = d
        return webhook_post_input

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
