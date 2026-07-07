from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.maxmemory_policy import MaxmemoryPolicy
from ..models.persistence_mode import PersistenceMode
from ..models.redis_plan import RedisPlan
from ..models.region import Region
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription


T = TypeVar("T", bound="RedisPOSTInput")


@_attrs_define
class RedisPOSTInput:
    """Input type for creating a Redis instance

    Attributes:
        name (str): The name of the Redis instance
        owner_id (str): The ID of the owner of the Redis instance
        plan (RedisPlan):
        region (Union[Unset, Region]): Defaults to "oregon"
        environment_id (Union[Unset, str]):
        maxmemory_policy (Union[Unset, MaxmemoryPolicy]): The eviction policy for the Key Value instance
        persistence_mode (Union[Unset, PersistenceMode]): The persistence mode for the Key Value instance. The default
            for paid instances is journal_snapshot (both journaling and snapshots). Only turn off persistence if you're
            using this Key Value instance as a cache and are okay with losing data. Free instances do not have persistence.
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    name: str
    owner_id: str
    plan: RedisPlan
    region: Union[Unset, Region] = UNSET
    environment_id: Union[Unset, str] = UNSET
    maxmemory_policy: Union[Unset, MaxmemoryPolicy] = UNSET
    persistence_mode: Union[Unset, PersistenceMode] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        owner_id = self.owner_id

        plan = self.plan.value

        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        environment_id = self.environment_id

        maxmemory_policy: Union[Unset, str] = UNSET
        if not isinstance(self.maxmemory_policy, Unset):
            maxmemory_policy = self.maxmemory_policy.value

        persistence_mode: Union[Unset, str] = UNSET
        if not isinstance(self.persistence_mode, Unset):
            persistence_mode = self.persistence_mode.value

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
                "name": name,
                "ownerId": owner_id,
                "plan": plan,
            }
        )
        if region is not UNSET:
            field_dict["region"] = region
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if maxmemory_policy is not UNSET:
            field_dict["maxmemoryPolicy"] = maxmemory_policy
        if persistence_mode is not UNSET:
            field_dict["persistenceMode"] = persistence_mode
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription

        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        plan = RedisPlan(d.pop("plan"))

        _region = d.pop("region", UNSET)
        region: Union[Unset, Region]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

        environment_id = d.pop("environmentId", UNSET)

        _maxmemory_policy = d.pop("maxmemoryPolicy", UNSET)
        maxmemory_policy: Union[Unset, MaxmemoryPolicy]
        if isinstance(_maxmemory_policy, Unset):
            maxmemory_policy = UNSET
        else:
            maxmemory_policy = MaxmemoryPolicy(_maxmemory_policy)

        _persistence_mode = d.pop("persistenceMode", UNSET)
        persistence_mode: Union[Unset, PersistenceMode]
        if isinstance(_persistence_mode, Unset):
            persistence_mode = UNSET
        else:
            persistence_mode = PersistenceMode(_persistence_mode)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(
                ip_allow_list_item_data
            )

            ip_allow_list.append(ip_allow_list_item)

        redis_post_input = cls(
            name=name,
            owner_id=owner_id,
            plan=plan,
            region=region,
            environment_id=environment_id,
            maxmemory_policy=maxmemory_policy,
            persistence_mode=persistence_mode,
            ip_allow_list=ip_allow_list,
        )

        redis_post_input.additional_properties = d
        return redis_post_input

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
