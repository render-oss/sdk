from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.webhook_event import WebhookEvent


T = TypeVar("T", bound="WebhookEventWithCursor")


@_attrs_define
class WebhookEventWithCursor:
    """
    Attributes:
        webhook_event (WebhookEvent):
        cursor (str):
    """

    webhook_event: "WebhookEvent"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        webhook_event = self.webhook_event.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "webhookEvent": webhook_event,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook_event import WebhookEvent

        d = dict(src_dict)
        webhook_event = WebhookEvent.from_dict(d.pop("webhookEvent"))

        cursor = d.pop("cursor")

        webhook_event_with_cursor = cls(
            webhook_event=webhook_event,
            cursor=cursor,
        )

        webhook_event_with_cursor.additional_properties = d
        return webhook_event_with_cursor

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
