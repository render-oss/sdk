from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostgresUpgradeSucceeded")


@_attrs_define
class PostgresUpgradeSucceeded:
    """
    Attributes:
        from_version (str):
        to_version (str):
    """

    from_version: str
    to_version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_version = self.from_version

        to_version = self.to_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromVersion": from_version,
                "toVersion": to_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_version = d.pop("fromVersion")

        to_version = d.pop("toVersion")

        postgres_upgrade_succeeded = cls(
            from_version=from_version,
            to_version=to_version,
        )

        postgres_upgrade_succeeded.additional_properties = d
        return postgres_upgrade_succeeded

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
