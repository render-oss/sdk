from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresReplicationSetupInput")


@_attrs_define
class PostgresReplicationSetupInput:
    """
    Attributes:
        schema_name (str): Schema to replicate.
        database_name (str): Database to replicate.
        all_tables_publication_name (Union[Unset, str]): Publication name to create.
        replication_slot_name (Union[Unset, str]): Replication slot name to create.
        restart_now (Union[Unset, bool]): Immediately enqueue a restart to apply.
    """

    schema_name: str
    database_name: str
    all_tables_publication_name: Union[Unset, str] = UNSET
    replication_slot_name: Union[Unset, str] = UNSET
    restart_now: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_name = self.schema_name

        database_name = self.database_name

        all_tables_publication_name = self.all_tables_publication_name

        replication_slot_name = self.replication_slot_name

        restart_now = self.restart_now

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schemaName": schema_name,
                "databaseName": database_name,
            }
        )
        if all_tables_publication_name is not UNSET:
            field_dict["allTablesPublicationName"] = all_tables_publication_name
        if replication_slot_name is not UNSET:
            field_dict["replicationSlotName"] = replication_slot_name
        if restart_now is not UNSET:
            field_dict["restartNow"] = restart_now

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_name = d.pop("schemaName")

        database_name = d.pop("databaseName")

        all_tables_publication_name = d.pop("allTablesPublicationName", UNSET)

        replication_slot_name = d.pop("replicationSlotName", UNSET)

        restart_now = d.pop("restartNow", UNSET)

        postgres_replication_setup_input = cls(
            schema_name=schema_name,
            database_name=database_name,
            all_tables_publication_name=all_tables_publication_name,
            replication_slot_name=replication_slot_name,
            restart_now=restart_now,
        )

        postgres_replication_setup_input.additional_properties = d
        return postgres_replication_setup_input

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
