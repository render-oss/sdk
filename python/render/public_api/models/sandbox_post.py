from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_plan import SandboxPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_policy_post import SandboxNetworkPolicyPOST
    from ..models.sandbox_post_env import SandboxPOSTEnv


T = TypeVar("T", bound="SandboxPOST")


@_attrs_define
class SandboxPOST:
    """
    Attributes:
        owner_id (str): The ID of the workspace the sandbox belongs to.
        network_policy (Union[Unset, SandboxNetworkPolicyPOST]): Set either `type` or its deprecated alias `default`.
            Sending both is
            only accepted when they name the same policy.
        plan (Union[SandboxPlan, Unset, str]): Compute plan. See `sandboxPlan` for known values.
        timeout_seconds (Union[Unset, int]): Maximum sandbox lifetime in seconds. Sandbox is terminated when reached.
            Default: 86400.
        idle_timeout_seconds (Union[Unset, int]): Seconds of inactivity before the sandbox is suspended. Use 0 to
            disable automatic idle suspension. Positive values must be at least 300. Default: 900.
        region (Union[Unset, str]): Render region. Defaults to the workspace default.
        env (Union[Unset, SandboxPOSTEnv]): Inline environment variables injected into the sandbox at creation.
        snapshot_id (Union[Unset, str]):  Example: snp-cph1rs3idesc73a2b2mg.
        snapshot_name (Union[Unset, str]): Case sensitive. Scoped to the sandbox group. Must not start with `snp-`
            so clients can tell a name from a snapshot ID. Several snapshots may
            share a name; the most recently available one is the one the name
            resolves to.
             Example: gold.
    """

    owner_id: str
    network_policy: Union[Unset, "SandboxNetworkPolicyPOST"] = UNSET
    plan: Union[SandboxPlan, Unset, str] = UNSET
    timeout_seconds: Union[Unset, int] = 86400
    idle_timeout_seconds: Union[Unset, int] = 900
    region: Union[Unset, str] = UNSET
    env: Union[Unset, "SandboxPOSTEnv"] = UNSET
    snapshot_id: Union[Unset, str] = UNSET
    snapshot_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        network_policy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        plan: Union[Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, SandboxPlan):
            plan = self.plan.value
        else:
            plan = self.plan

        timeout_seconds = self.timeout_seconds

        idle_timeout_seconds = self.idle_timeout_seconds

        region = self.region

        env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        snapshot_id = self.snapshot_id

        snapshot_name = self.snapshot_name

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
        if idle_timeout_seconds is not UNSET:
            field_dict["idleTimeoutSeconds"] = idle_timeout_seconds
        if region is not UNSET:
            field_dict["region"] = region
        if env is not UNSET:
            field_dict["env"] = env
        if snapshot_id is not UNSET:
            field_dict["snapshotId"] = snapshot_id
        if snapshot_name is not UNSET:
            field_dict["snapshotName"] = snapshot_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_policy_post import SandboxNetworkPolicyPOST
        from ..models.sandbox_post_env import SandboxPOSTEnv

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        _network_policy = d.pop("networkPolicy", UNSET)
        network_policy: Union[Unset, SandboxNetworkPolicyPOST]
        if isinstance(_network_policy, Unset):
            network_policy = UNSET
        else:
            network_policy = SandboxNetworkPolicyPOST.from_dict(_network_policy)

        def _parse_plan(data: object) -> Union[SandboxPlan, Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = SandboxPlan(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[SandboxPlan, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        idle_timeout_seconds = d.pop("idleTimeoutSeconds", UNSET)

        region = d.pop("region", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, SandboxPOSTEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = SandboxPOSTEnv.from_dict(_env)

        snapshot_id = d.pop("snapshotId", UNSET)

        snapshot_name = d.pop("snapshotName", UNSET)

        sandbox_post = cls(
            owner_id=owner_id,
            network_policy=network_policy,
            plan=plan,
            timeout_seconds=timeout_seconds,
            idle_timeout_seconds=idle_timeout_seconds,
            region=region,
            env=env,
            snapshot_id=snapshot_id,
            snapshot_name=snapshot_name,
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
