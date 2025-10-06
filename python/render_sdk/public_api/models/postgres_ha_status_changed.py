from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostgresHAStatusChanged")


@_attrs_define
class PostgresHAStatusChanged:
    """
    Attributes:
        from_status (str):
        to_status (str):
    """

    from_status: str
    to_status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_status = self.from_status

        to_status = self.to_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromStatus": from_status,
                "toStatus": to_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_status = d.pop("fromStatus")

        to_status = d.pop("toStatus")

        postgres_ha_status_changed = cls(
            from_status=from_status,
            to_status=to_status,
        )

        postgres_ha_status_changed.additional_properties = d
        return postgres_ha_status_changed

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
