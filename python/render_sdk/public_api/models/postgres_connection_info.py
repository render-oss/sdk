from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresConnectionInfo")


@_attrs_define
class PostgresConnectionInfo:
    """
    Attributes:
        password (str):
        internal_connection_string (str):
        external_connection_string (str):
        psql_command (str):
        internal_connection_pool_string (Union[Unset, str]):
        external_connection_pool_string (Union[Unset, str]):
    """

    password: str
    internal_connection_string: str
    external_connection_string: str
    psql_command: str
    internal_connection_pool_string: Union[Unset, str] = UNSET
    external_connection_pool_string: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password

        internal_connection_string = self.internal_connection_string

        external_connection_string = self.external_connection_string

        psql_command = self.psql_command

        internal_connection_pool_string = self.internal_connection_pool_string

        external_connection_pool_string = self.external_connection_pool_string

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
        if internal_connection_pool_string is not UNSET:
            field_dict["internalConnectionPoolString"] = internal_connection_pool_string
        if external_connection_pool_string is not UNSET:
            field_dict["externalConnectionPoolString"] = external_connection_pool_string

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password = d.pop("password")

        internal_connection_string = d.pop("internalConnectionString")

        external_connection_string = d.pop("externalConnectionString")

        psql_command = d.pop("psqlCommand")

        internal_connection_pool_string = d.pop("internalConnectionPoolString", UNSET)

        external_connection_pool_string = d.pop("externalConnectionPoolString", UNSET)

        postgres_connection_info = cls(
            password=password,
            internal_connection_string=internal_connection_string,
            external_connection_string=external_connection_string,
            psql_command=psql_command,
            internal_connection_pool_string=internal_connection_pool_string,
            external_connection_pool_string=external_connection_pool_string,
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
