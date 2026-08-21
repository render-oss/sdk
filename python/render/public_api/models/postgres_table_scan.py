from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresTableScan")


@_attrs_define
class PostgresTableScan:
    """The number of sequential scans performed against a table.

    Attributes:
        database (Union[Unset, str]):
        schema (Union[Unset, str]):
        table (Union[Unset, str]):
        scans (Union[Unset, int]):
    """

    database: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    table: Union[Unset, str] = UNSET
    scans: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        database = self.database

        schema = self.schema

        table = self.table

        scans = self.scans

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if database is not UNSET:
            field_dict["Database"] = database
        if schema is not UNSET:
            field_dict["Schema"] = schema
        if table is not UNSET:
            field_dict["Table"] = table
        if scans is not UNSET:
            field_dict["Scans"] = scans

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        database = d.pop("Database", UNSET)

        schema = d.pop("Schema", UNSET)

        table = d.pop("Table", UNSET)

        scans = d.pop("Scans", UNSET)

        postgres_table_scan = cls(
            database=database,
            schema=schema,
            table=table,
            scans=scans,
        )

        postgres_table_scan.additional_properties = d
        return postgres_table_scan

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
