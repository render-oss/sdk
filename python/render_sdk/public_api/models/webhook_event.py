import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.event_type import EventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEvent")


@_attrs_define
class WebhookEvent:
    """
    Attributes:
        id (str): the id of the webhook event
        event_id (str): the id of the event that triggered the webhook
        event_type (EventType):
        sent_at (datetime.datetime):
        status_code (Union[Unset, int]):
        response_body (Union[Unset, str]):
        error (Union[Unset, str]): error is populated when an error occurs without a response such as a timeout
    """

    id: str
    event_id: str
    event_type: EventType
    sent_at: datetime.datetime
    status_code: Union[Unset, int] = UNSET
    response_body: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        event_type = self.event_type.value

        sent_at = self.sent_at.isoformat()

        status_code = self.status_code

        response_body = self.response_body

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "eventId": event_id,
                "eventType": event_type,
                "sentAt": sent_at,
            }
        )
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if response_body is not UNSET:
            field_dict["responseBody"] = response_body
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("eventId")

        event_type = EventType(d.pop("eventType"))

        sent_at = isoparse(d.pop("sentAt"))

        status_code = d.pop("statusCode", UNSET)

        response_body = d.pop("responseBody", UNSET)

        error = d.pop("error", UNSET)

        webhook_event = cls(
            id=id,
            event_id=event_id,
            event_type=event_type,
            sent_at=sent_at,
            status_code=status_code,
            response_body=response_body,
            error=error,
        )

        webhook_event.additional_properties = d
        return webhook_event

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
