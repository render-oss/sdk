from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_plan import SandboxPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_policy_post import SandboxNetworkPolicyPOST
    from ..models.sandbox_port import SandboxPort
    from ..models.sandbox_post_env import SandboxPOSTEnv
    from ..models.sandbox_shared_filesystem import SandboxSharedFilesystem


T = TypeVar("T", bound="SandboxPOST")


@_attrs_define
class SandboxPOST:
    """The sandbox to create, including its compute plan, network policy, and optional source build or snapshot.

    Attributes:
        owner_id (str): The ID of the workspace the sandbox belongs to.
        sandbox_group_id (str | Unset): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        name (str | Unset): A label for the sandbox, such as `my-agent`, up to 64 characters. Names do not have to be
            unique; use the sandbox ID to identify a specific sandbox. Must not start with `sbx-`.
        network_policy (SandboxNetworkPolicyPOST | Unset): The outbound traffic policy to apply to the sandbox. Provide
            `type` or its deprecated alias `default`. If both are provided, they must match.
        exposed_ports (list[SandboxPort] | Unset): Ports exposed through public HTTP/WebSocket ingress, not arbitrary
            TCP forwarding. Each port may appear once, and at most 10 ports may be exposed.
        plan (SandboxPlan | str | Unset): The compute plan for the sandbox. See `sandboxPlan` for known values.
        timeout_seconds (int | Unset): The maximum time the sandbox can run continuously, in seconds. The sandbox
            terminates when this time elapses. If the sandbox is suspended and later resumed, this timeout restarts.

            Use 0 to disable the runtime timeout. Positive values must be between 60 and 2592000 (30 days). Defaults to
            86400, or to the source sandbox's runtime timeout when creating a sandbox from a snapshot.
        idle_timeout_seconds (int | Unset): The number of seconds of inactivity before Render suspends the sandbox. Use
            0 to disable automatic idle suspension. Positive values must be between 300 and 86400. Defaults to 900, or to
            the source sandbox's idle timeout when creating a sandbox from a snapshot.
        env (SandboxPOSTEnv | Unset): The environment variables to set when creating the sandbox.
        snapshot_id (str | Unset): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        snapshot_name (str | Unset): A case-sensitive name for snapshots in a sandbox group, up to 64 characters. Must
            not start with `snp-`. Multiple snapshots can share a name. When creating a sandbox by snapshot name, Render
            uses the most recently created snapshot with that name that is `available` and unexpired.
             Example: gold.
        build_id (str | Unset): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.
        build_name (str | Unset): The name of the build to create the sandbox from instead of the base image. Uses the
            newest successful build with this name in the sandbox group. Cannot be combined with `buildId`, `snapshotId`, or
            `snapshotName`.
        shared_filesystems (list[SandboxSharedFilesystem] | Unset): Shared filesystems to mount in the sandbox. At most
            one is supported.
    """

    owner_id: str
    sandbox_group_id: str | Unset = UNSET
    name: str | Unset = UNSET
    network_policy: SandboxNetworkPolicyPOST | Unset = UNSET
    exposed_ports: list[SandboxPort] | Unset = UNSET
    plan: SandboxPlan | str | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    idle_timeout_seconds: int | Unset = UNSET
    env: SandboxPOSTEnv | Unset = UNSET
    snapshot_id: str | Unset = UNSET
    snapshot_name: str | Unset = UNSET
    build_id: str | Unset = UNSET
    build_name: str | Unset = UNSET
    shared_filesystems: list[SandboxSharedFilesystem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        sandbox_group_id = self.sandbox_group_id

        name = self.name

        network_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        exposed_ports: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.exposed_ports, Unset):
            exposed_ports = []
            for componentsschemassandbox_ports_item_data in self.exposed_ports:
                componentsschemassandbox_ports_item = componentsschemassandbox_ports_item_data.to_dict()
                exposed_ports.append(componentsschemassandbox_ports_item)

        plan: str | Unset
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, SandboxPlan):
            plan = self.plan.value
        else:
            plan = self.plan

        timeout_seconds = self.timeout_seconds

        idle_timeout_seconds = self.idle_timeout_seconds

        env: dict[str, Any] | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        snapshot_id = self.snapshot_id

        snapshot_name = self.snapshot_name

        build_id = self.build_id

        build_name = self.build_name

        shared_filesystems: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.shared_filesystems, Unset):
            shared_filesystems = []
            for shared_filesystems_item_data in self.shared_filesystems:
                shared_filesystems_item = shared_filesystems_item_data.to_dict()
                shared_filesystems.append(shared_filesystems_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
            }
        )
        if sandbox_group_id is not UNSET:
            field_dict["sandboxGroupId"] = sandbox_group_id
        if name is not UNSET:
            field_dict["name"] = name
        if network_policy is not UNSET:
            field_dict["networkPolicy"] = network_policy
        if exposed_ports is not UNSET:
            field_dict["exposed_ports"] = exposed_ports
        if plan is not UNSET:
            field_dict["plan"] = plan
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if idle_timeout_seconds is not UNSET:
            field_dict["idleTimeoutSeconds"] = idle_timeout_seconds
        if env is not UNSET:
            field_dict["env"] = env
        if snapshot_id is not UNSET:
            field_dict["snapshotId"] = snapshot_id
        if snapshot_name is not UNSET:
            field_dict["snapshotName"] = snapshot_name
        if build_id is not UNSET:
            field_dict["buildId"] = build_id
        if build_name is not UNSET:
            field_dict["buildName"] = build_name
        if shared_filesystems is not UNSET:
            field_dict["sharedFilesystems"] = shared_filesystems

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_policy_post import SandboxNetworkPolicyPOST  # noqa: PLC0415
        from ..models.sandbox_port import SandboxPort  # noqa: PLC0415
        from ..models.sandbox_post_env import SandboxPOSTEnv  # noqa: PLC0415
        from ..models.sandbox_shared_filesystem import SandboxSharedFilesystem  # noqa: PLC0415

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        sandbox_group_id = d.pop("sandboxGroupId", UNSET)

        name = d.pop("name", UNSET)

        _network_policy = d.pop("networkPolicy", UNSET)
        network_policy: SandboxNetworkPolicyPOST | Unset
        if isinstance(_network_policy, Unset):
            network_policy = UNSET
        else:
            network_policy = SandboxNetworkPolicyPOST.from_dict(_network_policy)

        _exposed_ports = d.pop("exposed_ports", UNSET)
        exposed_ports: list[SandboxPort] | Unset = UNSET
        if _exposed_ports is not UNSET:
            exposed_ports = []
            for componentsschemassandbox_ports_item_data in _exposed_ports:
                componentsschemassandbox_ports_item = SandboxPort.from_dict(componentsschemassandbox_ports_item_data)

                exposed_ports.append(componentsschemassandbox_ports_item)

        def _parse_plan(data: object) -> SandboxPlan | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = SandboxPlan(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(SandboxPlan | str | Unset, data)

        plan = _parse_plan(d.pop("plan", UNSET))

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        idle_timeout_seconds = d.pop("idleTimeoutSeconds", UNSET)

        _env = d.pop("env", UNSET)
        env: SandboxPOSTEnv | Unset
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = SandboxPOSTEnv.from_dict(_env)

        snapshot_id = d.pop("snapshotId", UNSET)

        snapshot_name = d.pop("snapshotName", UNSET)

        build_id = d.pop("buildId", UNSET)

        build_name = d.pop("buildName", UNSET)

        _shared_filesystems = d.pop("sharedFilesystems", UNSET)
        shared_filesystems: list[SandboxSharedFilesystem] | Unset = UNSET
        if _shared_filesystems is not UNSET:
            shared_filesystems = []
            for shared_filesystems_item_data in _shared_filesystems:
                shared_filesystems_item = SandboxSharedFilesystem.from_dict(shared_filesystems_item_data)

                shared_filesystems.append(shared_filesystems_item)

        sandbox_post = cls(
            owner_id=owner_id,
            sandbox_group_id=sandbox_group_id,
            name=name,
            network_policy=network_policy,
            exposed_ports=exposed_ports,
            plan=plan,
            timeout_seconds=timeout_seconds,
            idle_timeout_seconds=idle_timeout_seconds,
            env=env,
            snapshot_id=snapshot_id,
            snapshot_name=snapshot_name,
            build_id=build_id,
            build_name=build_name,
            shared_filesystems=shared_filesystems,
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
