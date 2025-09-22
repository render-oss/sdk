from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.protected_status import ProtectedStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription


T = TypeVar("T", bound="Environment")


@_attrs_define
class Environment:
    """
    Attributes:
        id (str):
        name (str):
        project_id (str):
        databases_ids (list[str]):
        redis_ids (list[str]):
        service_ids (list[str]):
        env_group_ids (list[str]):
        protected_status (ProtectedStatus): Indicates whether an environment is `unprotected` or `protected`. Only admin
            users can perform destructive actions in `protected` environments.
        network_isolation_enabled (bool): Indicates whether network connections across environments are allowed.
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    id: str
    name: str
    project_id: str
    databases_ids: list[str]
    redis_ids: list[str]
    service_ids: list[str]
    env_group_ids: list[str]
    protected_status: ProtectedStatus
    network_isolation_enabled: bool
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        project_id = self.project_id

        databases_ids = self.databases_ids

        redis_ids = self.redis_ids

        service_ids = self.service_ids

        env_group_ids = self.env_group_ids

        protected_status = self.protected_status.value

        network_isolation_enabled = self.network_isolation_enabled

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "projectId": project_id,
                "databasesIds": databases_ids,
                "redisIds": redis_ids,
                "serviceIds": service_ids,
                "envGroupIds": env_group_ids,
                "protectedStatus": protected_status,
                "networkIsolationEnabled": network_isolation_enabled,
            }
        )
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        project_id = d.pop("projectId")

        databases_ids = cast(list[str], d.pop("databasesIds"))

        redis_ids = cast(list[str], d.pop("redisIds"))

        service_ids = cast(list[str], d.pop("serviceIds"))

        env_group_ids = cast(list[str], d.pop("envGroupIds"))

        protected_status = ProtectedStatus(d.pop("protectedStatus"))

        network_isolation_enabled = d.pop("networkIsolationEnabled")

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        environment = cls(
            id=id,
            name=name,
            project_id=project_id,
            databases_ids=databases_ids,
            redis_ids=redis_ids,
            service_ids=service_ids,
            env_group_ids=env_group_ids,
            protected_status=protected_status,
            network_isolation_enabled=network_isolation_enabled,
            ip_allow_list=ip_allow_list,
        )

        environment.additional_properties = d
        return environment

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
