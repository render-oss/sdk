from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postgres_plans import PostgresPlans
from ..models.postgres_version import PostgresVersion
from ..models.region import Region
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.postgres_parameter_overrides import PostgresParameterOverrides
    from ..models.read_replica_input import ReadReplicaInput


T = TypeVar("T", bound="PostgresPOSTInput")


@_attrs_define
class PostgresPOSTInput:
    """Input for creating a database

    Attributes:
        name (str): The name of the database as it will appear in the Render Dashboard
        owner_id (str): The ID of the workspace to create the database for
        plan (PostgresPlans):
        version (PostgresVersion): The PostgreSQL version
        database_name (str | Unset):  Default: 'randomly generated'.
        database_user (str | Unset):  Default: 'randomly generated'.
        datadog_api_key (str | Unset): The Datadog API key for the Datadog agent to monitor the new database.
        datadog_site (str | Unset): Datadog region to use for monitoring the new database. Defaults to 'US1'. Example:
            US1.
        enable_high_availability (bool | Unset):  Default: False.
        environment_id (str | Unset):
        disk_size_gb (int | Unset): The number of gigabytes of disk space to allocate for the database
        enable_disk_autoscaling (bool | Unset):  Default: False.
        connection_pool (str | Unset): What connection pool to use (if any) out of 'pgbouncer' and 'none' Default:
            'none'.
        region (Region | Unset): Defaults to "oregon"
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
        parameter_overrides (PostgresParameterOverrides | Unset):
        read_replicas (list[ReadReplicaInput] | Unset):
    """

    name: str
    owner_id: str
    plan: PostgresPlans
    version: PostgresVersion
    database_name: str | Unset = "randomly generated"
    database_user: str | Unset = "randomly generated"
    datadog_api_key: str | Unset = UNSET
    datadog_site: str | Unset = UNSET
    enable_high_availability: bool | Unset = False
    environment_id: str | Unset = UNSET
    disk_size_gb: int | Unset = UNSET
    enable_disk_autoscaling: bool | Unset = False
    connection_pool: str | Unset = "none"
    region: Region | Unset = UNSET
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    parameter_overrides: PostgresParameterOverrides | Unset = UNSET
    read_replicas: list[ReadReplicaInput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        owner_id = self.owner_id

        plan = self.plan.value

        version = self.version.value

        database_name = self.database_name

        database_user = self.database_user

        datadog_api_key = self.datadog_api_key

        datadog_site = self.datadog_site

        enable_high_availability = self.enable_high_availability

        environment_id = self.environment_id

        disk_size_gb = self.disk_size_gb

        enable_disk_autoscaling = self.enable_disk_autoscaling

        connection_pool = self.connection_pool

        region: str | Unset = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

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
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "plan": plan,
                "version": version,
            }
        )
        if database_name is not UNSET:
            field_dict["databaseName"] = database_name
        if database_user is not UNSET:
            field_dict["databaseUser"] = database_user
        if datadog_api_key is not UNSET:
            field_dict["datadogAPIKey"] = datadog_api_key
        if datadog_site is not UNSET:
            field_dict["datadogSite"] = datadog_site
        if enable_high_availability is not UNSET:
            field_dict["enableHighAvailability"] = enable_high_availability
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if disk_size_gb is not UNSET:
            field_dict["diskSizeGB"] = disk_size_gb
        if enable_disk_autoscaling is not UNSET:
            field_dict["enableDiskAutoscaling"] = enable_disk_autoscaling
        if connection_pool is not UNSET:
            field_dict["connectionPool"] = connection_pool
        if region is not UNSET:
            field_dict["region"] = region
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
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        plan = PostgresPlans(d.pop("plan"))

        version = PostgresVersion(d.pop("version"))

        database_name = d.pop("databaseName", UNSET)

        database_user = d.pop("databaseUser", UNSET)

        datadog_api_key = d.pop("datadogAPIKey", UNSET)

        datadog_site = d.pop("datadogSite", UNSET)

        enable_high_availability = d.pop("enableHighAvailability", UNSET)

        environment_id = d.pop("environmentId", UNSET)

        disk_size_gb = d.pop("diskSizeGB", UNSET)

        enable_disk_autoscaling = d.pop("enableDiskAutoscaling", UNSET)

        connection_pool = d.pop("connectionPool", UNSET)

        _region = d.pop("region", UNSET)
        region: Region | Unset
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

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

        postgres_post_input = cls(
            name=name,
            owner_id=owner_id,
            plan=plan,
            version=version,
            database_name=database_name,
            database_user=database_user,
            datadog_api_key=datadog_api_key,
            datadog_site=datadog_site,
            enable_high_availability=enable_high_availability,
            environment_id=environment_id,
            disk_size_gb=disk_size_gb,
            enable_disk_autoscaling=enable_disk_autoscaling,
            connection_pool=connection_pool,
            region=region,
            ip_allow_list=ip_allow_list,
            parameter_overrides=parameter_overrides,
            read_replicas=read_replicas,
        )

        postgres_post_input.additional_properties = d
        return postgres_post_input

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
