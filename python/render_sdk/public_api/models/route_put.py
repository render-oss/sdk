from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.route_type import RouteType

T = TypeVar("T", bound="RoutePut")


@_attrs_define
class RoutePut:
    """
    Attributes:
        type_ (RouteType):
        source (str):  Example: /:bar/foo.
        destination (str):  Example: /foo/:bar.
    """

    type_: RouteType
    source: str
    destination: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        source = self.source

        destination = self.destination

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "source": source,
                "destination": destination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = RouteType(d.pop("type"))

        source = d.pop("source")

        destination = d.pop("destination")

        route_put = cls(
            type_=type_,
            source=source,
            destination=destination,
        )

        route_put.additional_properties = d
        return route_put

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
