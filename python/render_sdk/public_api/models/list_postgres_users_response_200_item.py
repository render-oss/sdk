from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListPostgresUsersResponse200Item")


@_attrs_define
class ListPostgresUsersResponse200Item:
    """
    Attributes:
        username (Union[Unset, str]):
        default (Union[Unset, bool]):
        created_at (Union[Unset, str]):
        open_connections (Union[Unset, int]):
    """

    username: Union[Unset, str] = UNSET
    default: Union[Unset, bool] = UNSET
    created_at: Union[Unset, str] = UNSET
    open_connections: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        default = self.default

        created_at = self.created_at

        open_connections = self.open_connections

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if default is not UNSET:
            field_dict["default"] = default
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if open_connections is not UNSET:
            field_dict["openConnections"] = open_connections

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username", UNSET)

        default = d.pop("default", UNSET)

        created_at = d.pop("createdAt", UNSET)

        open_connections = d.pop("openConnections", UNSET)

        list_postgres_users_response_200_item = cls(
            username=username,
            default=default,
            created_at=created_at,
            open_connections=open_connections,
        )

        list_postgres_users_response_200_item.additional_properties = d
        return list_postgres_users_response_200_item

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
