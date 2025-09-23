from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.service_event import ServiceEvent


T = TypeVar("T", bound="ServiceEventWithCursor")


@_attrs_define
class ServiceEventWithCursor:
    """A service event with a cursor

    Attributes:
        event (ServiceEvent):
    """

    event: "ServiceEvent"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event = self.event.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event": event,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_event import ServiceEvent

        d = dict(src_dict)
        event = ServiceEvent.from_dict(d.pop("event"))

        service_event_with_cursor = cls(
            event=event,
        )

        service_event_with_cursor.additional_properties = d
        return service_event_with_cursor

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
