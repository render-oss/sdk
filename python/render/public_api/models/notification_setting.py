from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notify_setting_v2 import NotifySettingV2

T = TypeVar("T", bound="NotificationSetting")


@_attrs_define
class NotificationSetting:
    """
    Attributes:
        owner_id (str):
        slack_enabled (bool):
        email_enabled (bool):
        preview_notifications_enabled (bool):
        notifications_to_send (NotifySettingV2):
    """

    owner_id: str
    slack_enabled: bool
    email_enabled: bool
    preview_notifications_enabled: bool
    notifications_to_send: NotifySettingV2
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        slack_enabled = self.slack_enabled

        email_enabled = self.email_enabled

        preview_notifications_enabled = self.preview_notifications_enabled

        notifications_to_send = self.notifications_to_send.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "slackEnabled": slack_enabled,
                "emailEnabled": email_enabled,
                "previewNotificationsEnabled": preview_notifications_enabled,
                "notificationsToSend": notifications_to_send,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        slack_enabled = d.pop("slackEnabled")

        email_enabled = d.pop("emailEnabled")

        preview_notifications_enabled = d.pop("previewNotificationsEnabled")

        notifications_to_send = NotifySettingV2(d.pop("notificationsToSend"))

        notification_setting = cls(
            owner_id=owner_id,
            slack_enabled=slack_enabled,
            email_enabled=email_enabled,
            preview_notifications_enabled=preview_notifications_enabled,
            notifications_to_send=notifications_to_send,
        )

        notification_setting.additional_properties = d
        return notification_setting

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
