import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.database_status import DatabaseStatus
from ..models.redis_plan import RedisPlan
from ..models.region import Region
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.maintenance_run import MaintenanceRun
    from ..models.owner import Owner
    from ..models.redis_options import RedisOptions


T = TypeVar("T", bound="RedisDetail")


@_attrs_define
class RedisDetail:
    """A Redis instance

    Attributes:
        id (str): The ID of the Redis instance
        created_at (datetime.datetime): The creation time of the Redis instance
        updated_at (datetime.datetime): The last updated time of the Redis instance
        status (DatabaseStatus):
        region (Region): Defaults to "oregon"
        plan (RedisPlan):
        name (str): The name of the Redis instance
        owner (Owner):
        options (RedisOptions): Options for a Redis instance
        ip_allow_list (list['CidrBlockAndDescription']): The IP allow list for the Redis instance
        version (str): The version of Redis
        environment_id (Union[Unset, str]): The ID of the environment the Redis instance is associated with
        maintenance (Union[Unset, MaintenanceRun]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: DatabaseStatus
    region: Region
    plan: RedisPlan
    name: str
    owner: "Owner"
    options: "RedisOptions"
    ip_allow_list: list["CidrBlockAndDescription"]
    version: str
    environment_id: Union[Unset, str] = UNSET
    maintenance: Union[Unset, "MaintenanceRun"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status = self.status.value

        region = self.region.value

        plan = self.plan.value

        name = self.name

        owner = self.owner.to_dict()

        options = self.options.to_dict()

        ip_allow_list = []
        for ip_allow_list_item_data in self.ip_allow_list:
            ip_allow_list_item = ip_allow_list_item_data.to_dict()
            ip_allow_list.append(ip_allow_list_item)

        version = self.version

        environment_id = self.environment_id

        maintenance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maintenance, Unset):
            maintenance = self.maintenance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "status": status,
                "region": region,
                "plan": plan,
                "name": name,
                "owner": owner,
                "options": options,
                "ipAllowList": ip_allow_list,
                "version": version,
            }
        )
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if maintenance is not UNSET:
            field_dict["maintenance"] = maintenance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.maintenance_run import MaintenanceRun
        from ..models.owner import Owner
        from ..models.redis_options import RedisOptions

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        status = DatabaseStatus(d.pop("status"))

        region = Region(d.pop("region"))

        plan = RedisPlan(d.pop("plan"))

        name = d.pop("name")

        owner = Owner.from_dict(d.pop("owner"))

        options = RedisOptions.from_dict(d.pop("options"))

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList")
        for ip_allow_list_item_data in _ip_allow_list:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        version = d.pop("version")

        environment_id = d.pop("environmentId", UNSET)

        _maintenance = d.pop("maintenance", UNSET)
        maintenance: Union[Unset, MaintenanceRun]
        if isinstance(_maintenance, Unset):
            maintenance = UNSET
        else:
            maintenance = MaintenanceRun.from_dict(_maintenance)

        redis_detail = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            region=region,
            plan=plan,
            name=name,
            owner=owner,
            options=options,
            ip_allow_list=ip_allow_list,
            version=version,
            environment_id=environment_id,
            maintenance=maintenance,
        )

        redis_detail.additional_properties = d
        return redis_detail

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
