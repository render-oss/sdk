from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.owner_type import OwnerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription


T = TypeVar("T", bound="Owner")


@_attrs_define
class Owner:
    """
    Attributes:
        id (str):
        name (str):
        email (str):
        type_ (OwnerType):
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
        two_factor_auth_enabled (bool | Unset): Whether two-factor authentication is enabled for the owner. Only present
            if `type` is `user`.
    """

    id: str
    name: str
    email: str
    type_: OwnerType
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    two_factor_auth_enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        email = self.email

        type_ = self.type_.value

        ip_allow_list: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        two_factor_auth_enabled = self.two_factor_auth_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "email": email,
                "type": type_,
            }
        )
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list
        if two_factor_auth_enabled is not UNSET:
            field_dict["twoFactorAuthEnabled"] = two_factor_auth_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        email = d.pop("email")

        type_ = OwnerType(d.pop("type"))

        _ip_allow_list = d.pop("ipAllowList", UNSET)
        ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
        if _ip_allow_list is not UNSET:
            ip_allow_list = []
            for ip_allow_list_item_data in _ip_allow_list:
                ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

                ip_allow_list.append(ip_allow_list_item)

        two_factor_auth_enabled = d.pop("twoFactorAuthEnabled", UNSET)

        owner = cls(
            id=id,
            name=name,
            email=email,
            type_=type_,
            ip_allow_list=ip_allow_list,
            two_factor_auth_enabled=two_factor_auth_enabled,
        )

        owner.additional_properties = d
        return owner

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
