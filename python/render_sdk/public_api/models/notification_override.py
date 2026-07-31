from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notify_override import NotifyOverride
from ..models.notify_preview_override import NotifyPreviewOverride

T = TypeVar("T", bound="NotificationOverride")


@_attrs_define
class NotificationOverride:
    """
    Attributes:
        service_id (str):
        preview_notifications_enabled (NotifyPreviewOverride):
        notifications_to_send (NotifyOverride):
    """

    service_id: str
    preview_notifications_enabled: NotifyPreviewOverride
    notifications_to_send: NotifyOverride
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        preview_notifications_enabled = self.preview_notifications_enabled.value

        notifications_to_send = self.notifications_to_send.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serviceId": service_id,
                "previewNotificationsEnabled": preview_notifications_enabled,
                "notificationsToSend": notifications_to_send,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("serviceId")

        preview_notifications_enabled = NotifyPreviewOverride(d.pop("previewNotificationsEnabled"))

        notifications_to_send = NotifyOverride(d.pop("notificationsToSend"))

        notification_override = cls(
            service_id=service_id,
            preview_notifications_enabled=preview_notifications_enabled,
            notifications_to_send=notifications_to_send,
        )

        notification_override.additional_properties = d
        return notification_override

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
