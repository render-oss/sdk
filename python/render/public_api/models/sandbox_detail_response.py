from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_plan import SandboxPlan
from ..models.sandbox_status import SandboxStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_exposed_port import SandboxExposedPort
    from ..models.sandbox_network_policy import SandboxNetworkPolicy
    from ..models.sandbox_shared_filesystem import SandboxSharedFilesystem


T = TypeVar("T", bound="SandboxDetailResponse")


@_attrs_define
class SandboxDetailResponse:
    """
    Attributes:
        id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        status (SandboxStatus): The sandbox's current status.
        plan (SandboxPlan | str): The sandbox's compute plan. See `sandboxPlan` for known values.
        network_policy (SandboxNetworkPolicy): The policy that controls outbound traffic from the sandbox.
        region (str): The Render region where the sandbox runs. Example: oregon.
        timeout_seconds (int): The maximum time the sandbox can run continuously, in seconds. The sandbox terminates
            when this time elapses. If the sandbox is suspended and later resumed, this timeout restarts. A value of 0
            disables the runtime timeout.
             Example: 86400.
        idle_timeout_seconds (int): The number of seconds of inactivity before Render suspends the sandbox. A value of 0
            disables automatic idle suspension. Example: 900.
        created_at (datetime.datetime): The timestamp when the sandbox was created, in ISO 8601 format. Example:
            2026-04-01T18:30:00Z.
        name (None | str | Unset): The label set when the sandbox was created.
        sandbox_group_id (str | Unset): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        terminated_at (datetime.datetime | None | Unset): The timestamp when the sandbox was terminated, in ISO 8601
            format. Null if the sandbox has not been terminated.
        shared_filesystems (list[SandboxSharedFilesystem] | Unset): Shared filesystems mounted in the sandbox. Absent
            when there are none.
        exposed_ports (list[SandboxExposedPort] | Unset):
    """

    id: str
    status: SandboxStatus
    plan: SandboxPlan | str
    network_policy: SandboxNetworkPolicy
    region: str
    timeout_seconds: int
    idle_timeout_seconds: int
    created_at: datetime.datetime
    name: None | str | Unset = UNSET
    sandbox_group_id: str | Unset = UNSET
    terminated_at: datetime.datetime | None | Unset = UNSET
    shared_filesystems: list[SandboxSharedFilesystem] | Unset = UNSET
    exposed_ports: list[SandboxExposedPort] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        plan: str
        if isinstance(self.plan, SandboxPlan):
            plan = self.plan.value
        else:
            plan = self.plan

        network_policy = self.network_policy.to_dict()

        region = self.region

        timeout_seconds = self.timeout_seconds

        idle_timeout_seconds = self.idle_timeout_seconds

        created_at = self.created_at.isoformat()

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        sandbox_group_id = self.sandbox_group_id

        terminated_at: None | str | Unset
        if isinstance(self.terminated_at, Unset):
            terminated_at = UNSET
        elif isinstance(self.terminated_at, datetime.datetime):
            terminated_at = self.terminated_at.isoformat()
        else:
            terminated_at = self.terminated_at

        shared_filesystems: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.shared_filesystems, Unset):
            shared_filesystems = []
            for shared_filesystems_item_data in self.shared_filesystems:
                shared_filesystems_item = shared_filesystems_item_data.to_dict()
                shared_filesystems.append(shared_filesystems_item)

        exposed_ports: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.exposed_ports, Unset):
            exposed_ports = []
            for componentsschemassandbox_exposed_ports_item_data in self.exposed_ports:
                componentsschemassandbox_exposed_ports_item = componentsschemassandbox_exposed_ports_item_data.to_dict()
                exposed_ports.append(componentsschemassandbox_exposed_ports_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "plan": plan,
                "networkPolicy": network_policy,
                "region": region,
                "timeoutSeconds": timeout_seconds,
                "idleTimeoutSeconds": idle_timeout_seconds,
                "createdAt": created_at,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if sandbox_group_id is not UNSET:
            field_dict["sandboxGroupId"] = sandbox_group_id
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at
        if shared_filesystems is not UNSET:
            field_dict["sharedFilesystems"] = shared_filesystems
        if exposed_ports is not UNSET:
            field_dict["exposed_ports"] = exposed_ports

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_exposed_port import SandboxExposedPort  # noqa: PLC0415
        from ..models.sandbox_network_policy import SandboxNetworkPolicy  # noqa: PLC0415
        from ..models.sandbox_shared_filesystem import SandboxSharedFilesystem  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        status = SandboxStatus(d.pop("status"))

        def _parse_plan(data: object) -> SandboxPlan | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = SandboxPlan(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(SandboxPlan | str, data)

        plan = _parse_plan(d.pop("plan"))

        network_policy = SandboxNetworkPolicy.from_dict(d.pop("networkPolicy"))

        region = d.pop("region")

        timeout_seconds = d.pop("timeoutSeconds")

        idle_timeout_seconds = d.pop("idleTimeoutSeconds")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        sandbox_group_id = d.pop("sandboxGroupId", UNSET)

        def _parse_terminated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                terminated_at_type_0 = datetime.datetime.fromisoformat(data)

                return terminated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        terminated_at = _parse_terminated_at(d.pop("terminatedAt", UNSET))

        _shared_filesystems = d.pop("sharedFilesystems", UNSET)
        shared_filesystems: list[SandboxSharedFilesystem] | Unset = UNSET
        if _shared_filesystems is not UNSET:
            shared_filesystems = []
            for shared_filesystems_item_data in _shared_filesystems:
                shared_filesystems_item = SandboxSharedFilesystem.from_dict(shared_filesystems_item_data)

                shared_filesystems.append(shared_filesystems_item)

        _exposed_ports = d.pop("exposed_ports", UNSET)
        exposed_ports: list[SandboxExposedPort] | Unset = UNSET
        if _exposed_ports is not UNSET:
            exposed_ports = []
            for componentsschemassandbox_exposed_ports_item_data in _exposed_ports:
                componentsschemassandbox_exposed_ports_item = SandboxExposedPort.from_dict(
                    componentsschemassandbox_exposed_ports_item_data
                )

                exposed_ports.append(componentsschemassandbox_exposed_ports_item)

        sandbox_detail_response = cls(
            id=id,
            status=status,
            plan=plan,
            network_policy=network_policy,
            region=region,
            timeout_seconds=timeout_seconds,
            idle_timeout_seconds=idle_timeout_seconds,
            created_at=created_at,
            name=name,
            sandbox_group_id=sandbox_group_id,
            terminated_at=terminated_at,
            shared_filesystems=shared_filesystems,
            exposed_ports=exposed_ports,
        )

        sandbox_detail_response.additional_properties = d
        return sandbox_detail_response

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
