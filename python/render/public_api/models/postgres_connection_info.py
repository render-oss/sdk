from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostgresConnectionInfo")


@_attrs_define
class PostgresConnectionInfo:
    """
    Attributes:
        password (str):
        internal_connection_string (str):
        external_connection_string (str):
        psql_command (str):
    """

    password: str
    internal_connection_string: str
    external_connection_string: str
    psql_command: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password

        internal_connection_string = self.internal_connection_string

        external_connection_string = self.external_connection_string

        psql_command = self.psql_command

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "password": password,
                "internalConnectionString": internal_connection_string,
                "externalConnectionString": external_connection_string,
                "psqlCommand": psql_command,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password = d.pop("password")

        internal_connection_string = d.pop("internalConnectionString")

        external_connection_string = d.pop("externalConnectionString")

        psql_command = d.pop("psqlCommand")

        postgres_connection_info = cls(
            password=password,
            internal_connection_string=internal_connection_string,
            external_connection_string=external_connection_string,
            psql_command=psql_command,
        )

        postgres_connection_info.additional_properties = d
        return postgres_connection_info

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
