from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresSize")


@_attrs_define
class PostgresSize:
    """The size of an index, table, or database.

    Attributes:
        database (Union[Unset, str]):
        schema (Union[Unset, str]):
        table (Union[Unset, str]):
        index (Union[Unset, str]):
        bytes_ (Union[Unset, int]):
    """

    database: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    table: Union[Unset, str] = UNSET
    index: Union[Unset, str] = UNSET
    bytes_: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        database = self.database

        schema = self.schema

        table = self.table

        index = self.index

        bytes_ = self.bytes_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if database is not UNSET:
            field_dict["Database"] = database
        if schema is not UNSET:
            field_dict["Schema"] = schema
        if table is not UNSET:
            field_dict["Table"] = table
        if index is not UNSET:
            field_dict["Index"] = index
        if bytes_ is not UNSET:
            field_dict["Bytes"] = bytes_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        database = d.pop("Database", UNSET)

        schema = d.pop("Schema", UNSET)

        table = d.pop("Table", UNSET)

        index = d.pop("Index", UNSET)

        bytes_ = d.pop("Bytes", UNSET)

        postgres_size = cls(
            database=database,
            schema=schema,
            table=table,
            index=index,
            bytes_=bytes_,
        )

        postgres_size.additional_properties = d
        return postgres_size

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
