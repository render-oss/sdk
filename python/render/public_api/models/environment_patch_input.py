from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.protected_status import ProtectedStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription


T = TypeVar("T", bound="EnvironmentPATCHInput")


@_attrs_define
class EnvironmentPATCHInput:
    """
    Attributes:
        name (Union[Unset, str]):
        network_isolation_enabled (Union[Unset, bool]): Indicates whether network connections across environments are
            allowed.
        protected_status (Union[Unset, ProtectedStatus]): Indicates whether an environment is `unprotected` or
            `protected`. Only admin users can perform destructive actions in `protected` environments.
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    name: Union[Unset, str] = UNSET
    network_isolation_enabled: Union[Unset, bool] = UNSET
    protected_status: Union[Unset, ProtectedStatus] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        network_isolation_enabled = self.network_isolation_enabled

        protected_status: Union[Unset, str] = UNSET
        if not isinstance(self.protected_status, Unset):
            protected_status = self.protected_status.value

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if network_isolation_enabled is not UNSET:
            field_dict["networkIsolationEnabled"] = network_isolation_enabled
        if protected_status is not UNSET:
            field_dict["protectedStatus"] = protected_status
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        network_isolation_enabled = d.pop("networkIsolationEnabled", UNSET)

        _protected_status = d.pop("protectedStatus", UNSET)
        protected_status: Union[Unset, ProtectedStatus]
        if isinstance(_protected_status, Unset):
            protected_status = UNSET
        else:
            protected_status = ProtectedStatus(_protected_status)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        environment_patch_input = cls(
            name=name,
            network_isolation_enabled=network_isolation_enabled,
            protected_status=protected_status,
            ip_allow_list=ip_allow_list,
        )

        environment_patch_input.additional_properties = d
        return environment_patch_input

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
