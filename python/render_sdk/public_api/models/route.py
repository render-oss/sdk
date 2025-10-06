from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.route_type import RouteType

T = TypeVar("T", bound="Route")


@_attrs_define
class Route:
    """
    Attributes:
        id (str):
        type_ (RouteType):
        source (str):
        destination (str):
        priority (int): Redirect and Rewrite Rules are applied in priority order starting at 0
    """

    id: str
    type_: RouteType
    source: str
    destination: str
    priority: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_.value

        source = self.source

        destination = self.destination

        priority = self.priority

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "source": source,
                "destination": destination,
                "priority": priority,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = RouteType(d.pop("type"))

        source = d.pop("source")

        destination = d.pop("destination")

        priority = d.pop("priority")

        route = cls(
            id=id,
            type_=type_,
            source=source,
            destination=destination,
            priority=priority,
        )

        route.additional_properties = d
        return route

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
