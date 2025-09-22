from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.route_type import RouteType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RoutePost")


@_attrs_define
class RoutePost:
    """
    Attributes:
        type_ (RouteType):
        source (str):  Example: /:bar/foo.
        destination (str):  Example: /foo/:bar.
        priority (Union[Unset, int]): Redirect and Rewrite Rules are applied in priority order starting at 0. Defaults
            to last in the priority list.
    """

    type_: RouteType
    source: str
    destination: str
    priority: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        source = self.source

        destination = self.destination

        priority = self.priority

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "source": source,
                "destination": destination,
            }
        )
        if priority is not UNSET:
            field_dict["priority"] = priority

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = RouteType(d.pop("type"))

        source = d.pop("source")

        destination = d.pop("destination")

        priority = d.pop("priority", UNSET)

        route_post = cls(
            type_=type_,
            source=source,
            destination=destination,
            priority=priority,
        )

        route_post.additional_properties = d
        return route_post

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
