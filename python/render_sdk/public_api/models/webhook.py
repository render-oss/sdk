from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_type import EventType

T = TypeVar("T", bound="Webhook")


@_attrs_define
class Webhook:
    """
    Attributes:
        id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        url (str):
        name (str):
        secret (str):
        enabled (bool):
        event_filter (list[EventType]): The event types that will trigger the webhook. An empty list means all event
            types will trigger the webhook.
    """

    id: str
    url: str
    name: str
    secret: str
    enabled: bool
    event_filter: list[EventType]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        url = self.url

        name = self.name

        secret = self.secret

        enabled = self.enabled

        event_filter = []
        for componentsschemasevent_filter_item_data in self.event_filter:
            componentsschemasevent_filter_item = componentsschemasevent_filter_item_data.value
            event_filter.append(componentsschemasevent_filter_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "url": url,
                "name": name,
                "secret": secret,
                "enabled": enabled,
                "eventFilter": event_filter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        url = d.pop("url")

        name = d.pop("name")

        secret = d.pop("secret")

        enabled = d.pop("enabled")

        event_filter = []
        _event_filter = d.pop("eventFilter")
        for componentsschemasevent_filter_item_data in _event_filter:
            componentsschemasevent_filter_item = EventType(componentsschemasevent_filter_item_data)

            event_filter.append(componentsschemasevent_filter_item)

        webhook = cls(
            id=id,
            url=url,
            name=name,
            secret=secret,
            enabled=enabled,
            event_filter=event_filter,
        )

        webhook.additional_properties = d
        return webhook

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
