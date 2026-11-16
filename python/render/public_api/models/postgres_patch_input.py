from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postgres_plans import PostgresPlans
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.postgres_parameter_overrides import PostgresParameterOverrides
    from ..models.read_replica_input import ReadReplicaInput


T = TypeVar("T", bound="PostgresPATCHInput")


@_attrs_define
class PostgresPATCHInput:
    """
    Attributes:
        name (str | Unset):
        plan (PostgresPlans | Unset):
        disk_size_gb (int | Unset): The number of gigabytes of disk space to allocate for the database
        enable_disk_autoscaling (bool | Unset):
        connection_pool (str | Unset): What connection pool to use (if any) out of 'pgbouncer' and 'none' Default:
            'none'.
        enable_high_availability (bool | Unset):
        datadog_api_key (str | Unset): The Datadog API key for the Datadog agent to monitor the database. Pass empty
            string to remove. Restarts Postgres on change.
        datadog_site (str | Unset): Datadog region to use for monitoring the new database. Defaults to 'US1'. Example:
            US1.
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
        parameter_overrides (PostgresParameterOverrides | Unset):
        read_replicas (list[ReadReplicaInput] | Unset):
    """

    name: str | Unset = UNSET
    plan: PostgresPlans | Unset = UNSET
    disk_size_gb: int | Unset = UNSET
    enable_disk_autoscaling: bool | Unset = UNSET
    connection_pool: str | Unset = "none"
    enable_high_availability: bool | Unset = UNSET
    datadog_api_key: str | Unset = UNSET
    datadog_site: str | Unset = UNSET
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    parameter_overrides: PostgresParameterOverrides | Unset = UNSET
    read_replicas: list[ReadReplicaInput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        plan: str | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        disk_size_gb = self.disk_size_gb

        enable_disk_autoscaling = self.enable_disk_autoscaling

        connection_pool = self.connection_pool

        enable_high_availability = self.enable_high_availability

        datadog_api_key = self.datadog_api_key

        datadog_site = self.datadog_site

        ip_allow_list: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        parameter_overrides: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameter_overrides, Unset):
            parameter_overrides = self.parameter_overrides.to_dict()

        read_replicas: list[dict[str, Any]] | Unset = UNSET
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
        if enable_disk_autoscaling is not UNSET:
            field_dict["enableDiskAutoscaling"] = enable_disk_autoscaling
        if connection_pool is not UNSET:
            field_dict["connectionPool"] = connection_pool
        if enable_high_availability is not UNSET:
            field_dict["enableHighAvailability"] = enable_high_availability
        if datadog_api_key is not UNSET:
            field_dict["datadogAPIKey"] = datadog_api_key
        if datadog_site is not UNSET:
            field_dict["datadogSite"] = datadog_site
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list
        if parameter_overrides is not UNSET:
            field_dict["parameterOverrides"] = parameter_overrides
        if read_replicas is not UNSET:
            field_dict["readReplicas"] = read_replicas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription  # noqa: PLC0415
        from ..models.postgres_parameter_overrides import PostgresParameterOverrides  # noqa: PLC0415
        from ..models.read_replica_input import ReadReplicaInput  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: PostgresPlans | Unset
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PostgresPlans(_plan)

        disk_size_gb = d.pop("diskSizeGB", UNSET)

        enable_disk_autoscaling = d.pop("enableDiskAutoscaling", UNSET)

        connection_pool = d.pop("connectionPool", UNSET)

        enable_high_availability = d.pop("enableHighAvailability", UNSET)

        datadog_api_key = d.pop("datadogAPIKey", UNSET)

        datadog_site = d.pop("datadogSite", UNSET)

        _ip_allow_list = d.pop("ipAllowList", UNSET)
        ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
        if _ip_allow_list is not UNSET:
            ip_allow_list = []
            for ip_allow_list_item_data in _ip_allow_list:
                ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

                ip_allow_list.append(ip_allow_list_item)

        _parameter_overrides = d.pop("parameterOverrides", UNSET)
        parameter_overrides: PostgresParameterOverrides | Unset
        if isinstance(_parameter_overrides, Unset):
            parameter_overrides = UNSET
        else:
            parameter_overrides = PostgresParameterOverrides.from_dict(_parameter_overrides)

        _read_replicas = d.pop("readReplicas", UNSET)
        read_replicas: list[ReadReplicaInput] | Unset = UNSET
        if _read_replicas is not UNSET:
            read_replicas = []
            for componentsschemasread_replicas_input_item_data in _read_replicas:
                componentsschemasread_replicas_input_item = ReadReplicaInput.from_dict(
                    componentsschemasread_replicas_input_item_data
                )

                read_replicas.append(componentsschemasread_replicas_input_item)

        postgres_patch_input = cls(
            name=name,
            plan=plan,
            disk_size_gb=disk_size_gb,
            enable_disk_autoscaling=enable_disk_autoscaling,
            connection_pool=connection_pool,
            enable_high_availability=enable_high_availability,
            datadog_api_key=datadog_api_key,
            datadog_site=datadog_site,
            ip_allow_list=ip_allow_list,
            parameter_overrides=parameter_overrides,
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
