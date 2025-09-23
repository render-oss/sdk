from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.maxmemory_policy import MaxmemoryPolicy
from ..models.redis_plan import RedisPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription


T = TypeVar("T", bound="RedisPATCHInput")


@_attrs_define
class RedisPATCHInput:
    """Input type for updating a Redis instance

    Attributes:
        name (Union[Unset, str]): The name of the Redis instance
        plan (Union[Unset, RedisPlan]):
        maxmemory_policy (Union[Unset, MaxmemoryPolicy]): The eviction policy for the Key Value instance
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    name: Union[Unset, str] = UNSET
    plan: Union[Unset, RedisPlan] = UNSET
    maxmemory_policy: Union[Unset, MaxmemoryPolicy] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        maxmemory_policy: Union[Unset, str] = UNSET
        if not isinstance(self.maxmemory_policy, Unset):
            maxmemory_policy = self.maxmemory_policy.value

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
        if plan is not UNSET:
            field_dict["plan"] = plan
        if maxmemory_policy is not UNSET:
            field_dict["maxmemoryPolicy"] = maxmemory_policy
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, RedisPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = RedisPlan(_plan)

        _maxmemory_policy = d.pop("maxmemoryPolicy", UNSET)
        maxmemory_policy: Union[Unset, MaxmemoryPolicy]
        if isinstance(_maxmemory_policy, Unset):
            maxmemory_policy = UNSET
        else:
            maxmemory_policy = MaxmemoryPolicy(_maxmemory_policy)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        redis_patch_input = cls(
            name=name,
            plan=plan,
            maxmemory_policy=maxmemory_policy,
            ip_allow_list=ip_allow_list,
        )

        redis_patch_input.additional_properties = d
        return redis_patch_input

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
