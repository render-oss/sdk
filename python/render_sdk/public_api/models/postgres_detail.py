import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.database_role import DatabaseRole
from ..models.database_status import DatabaseStatus
from ..models.postgres_detail_suspended import PostgresDetailSuspended
from ..models.postgres_plans import PostgresPlans
from ..models.postgres_version import PostgresVersion
from ..models.region import Region
from ..models.suspender_type import SuspenderType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.maintenance_run import MaintenanceRun
    from ..models.owner import Owner
    from ..models.read_replica import ReadReplica


T = TypeVar("T", bound="PostgresDetail")


@_attrs_define
class PostgresDetail:
    """
    Attributes:
        id (str):
        ip_allow_list (list['CidrBlockAndDescription']):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        dashboard_url (str): The URL to view the Postgres instance in the Render Dashboard
        database_name (str):
        database_user (str):
        high_availability_enabled (bool):
        name (str):
        owner (Owner):
        plan (PostgresPlans):
        region (Region): Defaults to "oregon"
        read_replicas (list['ReadReplica']):
        role (DatabaseRole):
        status (DatabaseStatus):
        version (PostgresVersion): The PostgreSQL version
        suspended (PostgresDetailSuspended):
        suspenders (list[SuspenderType]):
        expires_at (Union[Unset, datetime.datetime]): The time at which the database will be expire. Applies to free
            tier databases only.
        environment_id (Union[Unset, str]):
        maintenance (Union[Unset, MaintenanceRun]):
        disk_size_gb (Union[Unset, int]):
        primary_postgres_id (Union[Unset, str]):
    """

    id: str
    ip_allow_list: list["CidrBlockAndDescription"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    dashboard_url: str
    database_name: str
    database_user: str
    high_availability_enabled: bool
    name: str
    owner: "Owner"
    plan: PostgresPlans
    region: Region
    read_replicas: list["ReadReplica"]
    role: DatabaseRole
    status: DatabaseStatus
    version: PostgresVersion
    suspended: PostgresDetailSuspended
    suspenders: list[SuspenderType]
    expires_at: Union[Unset, datetime.datetime] = UNSET
    environment_id: Union[Unset, str] = UNSET
    maintenance: Union[Unset, "MaintenanceRun"] = UNSET
    disk_size_gb: Union[Unset, int] = UNSET
    primary_postgres_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ip_allow_list = []
        for ip_allow_list_item_data in self.ip_allow_list:
            ip_allow_list_item = ip_allow_list_item_data.to_dict()
            ip_allow_list.append(ip_allow_list_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        dashboard_url = self.dashboard_url

        database_name = self.database_name

        database_user = self.database_user

        high_availability_enabled = self.high_availability_enabled

        name = self.name

        owner = self.owner.to_dict()

        plan = self.plan.value

        region = self.region.value

        read_replicas = []
        for componentsschemasread_replicas_item_data in self.read_replicas:
            componentsschemasread_replicas_item = componentsschemasread_replicas_item_data.to_dict()
            read_replicas.append(componentsschemasread_replicas_item)

        role = self.role.value

        status = self.status.value

        version = self.version.value

        suspended = self.suspended.value

        suspenders = []
        for suspenders_item_data in self.suspenders:
            suspenders_item = suspenders_item_data.value
            suspenders.append(suspenders_item)

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        environment_id = self.environment_id

        maintenance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maintenance, Unset):
            maintenance = self.maintenance.to_dict()

        disk_size_gb = self.disk_size_gb

        primary_postgres_id = self.primary_postgres_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ipAllowList": ip_allow_list,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "dashboardUrl": dashboard_url,
                "databaseName": database_name,
                "databaseUser": database_user,
                "highAvailabilityEnabled": high_availability_enabled,
                "name": name,
                "owner": owner,
                "plan": plan,
                "region": region,
                "readReplicas": read_replicas,
                "role": role,
                "status": status,
                "version": version,
                "suspended": suspended,
                "suspenders": suspenders,
            }
        )
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if maintenance is not UNSET:
            field_dict["maintenance"] = maintenance
        if disk_size_gb is not UNSET:
            field_dict["diskSizeGB"] = disk_size_gb
        if primary_postgres_id is not UNSET:
            field_dict["primaryPostgresID"] = primary_postgres_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.maintenance_run import MaintenanceRun
        from ..models.owner import Owner
        from ..models.read_replica import ReadReplica

        d = dict(src_dict)
        id = d.pop("id")

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList")
        for ip_allow_list_item_data in _ip_allow_list:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        dashboard_url = d.pop("dashboardUrl")

        database_name = d.pop("databaseName")

        database_user = d.pop("databaseUser")

        high_availability_enabled = d.pop("highAvailabilityEnabled")

        name = d.pop("name")

        owner = Owner.from_dict(d.pop("owner"))

        plan = PostgresPlans(d.pop("plan"))

        region = Region(d.pop("region"))

        read_replicas = []
        _read_replicas = d.pop("readReplicas")
        for componentsschemasread_replicas_item_data in _read_replicas:
            componentsschemasread_replicas_item = ReadReplica.from_dict(componentsschemasread_replicas_item_data)

            read_replicas.append(componentsschemasread_replicas_item)

        role = DatabaseRole(d.pop("role"))

        status = DatabaseStatus(d.pop("status"))

        version = PostgresVersion(d.pop("version"))

        suspended = PostgresDetailSuspended(d.pop("suspended"))

        suspenders = []
        _suspenders = d.pop("suspenders")
        for suspenders_item_data in _suspenders:
            suspenders_item = SuspenderType(suspenders_item_data)

            suspenders.append(suspenders_item)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        environment_id = d.pop("environmentId", UNSET)

        _maintenance = d.pop("maintenance", UNSET)
        maintenance: Union[Unset, MaintenanceRun]
        if isinstance(_maintenance, Unset):
            maintenance = UNSET
        else:
            maintenance = MaintenanceRun.from_dict(_maintenance)

        disk_size_gb = d.pop("diskSizeGB", UNSET)

        primary_postgres_id = d.pop("primaryPostgresID", UNSET)

        postgres_detail = cls(
            id=id,
            ip_allow_list=ip_allow_list,
            created_at=created_at,
            updated_at=updated_at,
            dashboard_url=dashboard_url,
            database_name=database_name,
            database_user=database_user,
            high_availability_enabled=high_availability_enabled,
            name=name,
            owner=owner,
            plan=plan,
            region=region,
            read_replicas=read_replicas,
            role=role,
            status=status,
            version=version,
            suspended=suspended,
            suspenders=suspenders,
            expires_at=expires_at,
            environment_id=environment_id,
            maintenance=maintenance,
            disk_size_gb=disk_size_gb,
            primary_postgres_id=primary_postgres_id,
        )

        postgres_detail.additional_properties = d
        return postgres_detail

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
