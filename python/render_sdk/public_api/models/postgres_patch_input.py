from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postgres_plans import PostgresPlans
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.read_replica_input import ReadReplicaInput


T = TypeVar("T", bound="PostgresPATCHInput")


@_attrs_define
class PostgresPATCHInput:
    """
    Attributes:
        name (Union[Unset, str]):
        plan (Union[Unset, PostgresPlans]):
        disk_size_gb (Union[Unset, int]): The number of gigabytes of disk space to allocate for the database
        enable_high_availability (Union[Unset, bool]):
        datadog_api_key (Union[Unset, str]): The Datadog API key for the Datadog agent to monitor the database. Pass
            empty string to remove. Restarts Postgres on change.
        datadog_site (Union[Unset, str]): Datadog region to use for monitoring the new database. Defaults to 'US1'.
            Example: US1.
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
        read_replicas (Union[Unset, list['ReadReplicaInput']]):
    """

    name: Union[Unset, str] = UNSET
    plan: Union[Unset, PostgresPlans] = UNSET
    disk_size_gb: Union[Unset, int] = UNSET
    enable_high_availability: Union[Unset, bool] = UNSET
    datadog_api_key: Union[Unset, str] = UNSET
    datadog_site: Union[Unset, str] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    read_replicas: Union[Unset, list["ReadReplicaInput"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        disk_size_gb = self.disk_size_gb

        enable_high_availability = self.enable_high_availability

        datadog_api_key = self.datadog_api_key

        datadog_site = self.datadog_site

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        read_replicas: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.read_replicas, Unset):
            read_replicas = []
            for componentsschemasread_replicas_input_item_data in self.read_replicas:
                componentsschemasread_replicas_input_item = componentsschemasread_replicas_input_item_data.to_dict()
                read_replicas.append(componentsschemasread_replicas_input_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if plan is not UNSET:
            field_dict["plan"] = plan
        if disk_size_gb is not UNSET:
            field_dict["diskSizeGB"] = disk_size_gb
        if enable_high_availability is not UNSET:
            field_dict["enableHighAvailability"] = enable_high_availability
        if datadog_api_key is not UNSET:
            field_dict["datadogAPIKey"] = datadog_api_key
        if datadog_site is not UNSET:
            field_dict["datadogSite"] = datadog_site
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list
        if read_replicas is not UNSET:
            field_dict["readReplicas"] = read_replicas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.read_replica_input import ReadReplicaInput

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, PostgresPlans]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PostgresPlans(_plan)

        disk_size_gb = d.pop("diskSizeGB", UNSET)

        enable_high_availability = d.pop("enableHighAvailability", UNSET)

        datadog_api_key = d.pop("datadogAPIKey", UNSET)

        datadog_site = d.pop("datadogSite", UNSET)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        read_replicas = []
        _read_replicas = d.pop("readReplicas", UNSET)
        for componentsschemasread_replicas_input_item_data in _read_replicas or []:
            componentsschemasread_replicas_input_item = ReadReplicaInput.from_dict(
                componentsschemasread_replicas_input_item_data
            )

            read_replicas.append(componentsschemasread_replicas_input_item)

        postgres_patch_input = cls(
            name=name,
            plan=plan,
            disk_size_gb=disk_size_gb,
            enable_high_availability=enable_high_availability,
            datadog_api_key=datadog_api_key,
            datadog_site=datadog_site,
            ip_allow_list=ip_allow_list,
            read_replicas=read_replicas,
        )

        postgres_patch_input.additional_properties = d
        return postgres_patch_input

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
