from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_table_scan import PostgresTableScan


T = TypeVar("T", bound="PostgresTableScansResult")


@_attrs_define
class PostgresTableScansResult:
    """
    Attributes:
        table_scans (list['PostgresTableScan']):
    """

    table_scans: list["PostgresTableScan"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_scans = []
        for table_scans_item_data in self.table_scans:
            table_scans_item = table_scans_item_data.to_dict()
            table_scans.append(table_scans_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tableScans": table_scans,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_table_scan import PostgresTableScan

        d = dict(src_dict)
        table_scans = []
        _table_scans = d.pop("tableScans")
        for table_scans_item_data in _table_scans:
            table_scans_item = PostgresTableScan.from_dict(table_scans_item_data)

            table_scans.append(table_scans_item)

        postgres_table_scans_result = cls(
            table_scans=table_scans,
        )

        postgres_table_scans_result.additional_properties = d
        return postgres_table_scans_result

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
