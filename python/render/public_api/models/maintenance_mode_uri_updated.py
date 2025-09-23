from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceModeURIUpdated")


@_attrs_define
class MaintenanceModeURIUpdated:
    """
    Attributes:
        from_uri (str):
        to_uri (str):
    """

    from_uri: str
    to_uri: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_uri = self.from_uri

        to_uri = self.to_uri

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromURI": from_uri,
                "toURI": to_uri,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_uri = d.pop("fromURI")

        to_uri = d.pop("toURI")

        maintenance_mode_uri_updated = cls(
            from_uri=from_uri,
            to_uri=to_uri,
        )

        maintenance_mode_uri_updated.additional_properties = d
        return maintenance_mode_uri_updated

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
