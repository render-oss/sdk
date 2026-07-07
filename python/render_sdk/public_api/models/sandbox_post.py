from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_plan import SandboxPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_policy import SandboxNetworkPolicy


T = TypeVar("T", bound="SandboxPOST")


@_attrs_define
class SandboxPOST:
    """
    Attributes:
        owner_id (str): The ID of the workspace the sandbox belongs to.
        network_policy (Union[Unset, SandboxNetworkPolicy]):
        plan (Union[Unset, SandboxPlan]): Compute plan. Sizing matches Workflow plans of the same name. Default:
            SandboxPlan.STARTER.
        timeout_seconds (Union[Unset, int]): Maximum sandbox lifetime in seconds. Sandbox is terminated when reached.
            Default: 7200.
        region (Union[Unset, str]): Render region. Defaults to the workspace default.
    """

    owner_id: str
    network_policy: Union[Unset, "SandboxNetworkPolicy"] = UNSET
    plan: Union[Unset, SandboxPlan] = SandboxPlan.STARTER
    timeout_seconds: Union[Unset, int] = 7200
    region: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        network_policy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        timeout_seconds = self.timeout_seconds

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
            }
        )
        if network_policy is not UNSET:
            field_dict["networkPolicy"] = network_policy
        if plan is not UNSET:
            field_dict["plan"] = plan
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_policy import SandboxNetworkPolicy

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        _network_policy = d.pop("networkPolicy", UNSET)
        network_policy: Union[Unset, SandboxNetworkPolicy]
        if isinstance(_network_policy, Unset):
            network_policy = UNSET
        else:
            network_policy = SandboxNetworkPolicy.from_dict(_network_policy)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, SandboxPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = SandboxPlan(_plan)

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        region = d.pop("region", UNSET)

        sandbox_post = cls(
            owner_id=owner_id,
            network_policy=network_policy,
            plan=plan,
            timeout_seconds=timeout_seconds,
            region=region,
        )

        sandbox_post.additional_properties = d
        return sandbox_post

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
