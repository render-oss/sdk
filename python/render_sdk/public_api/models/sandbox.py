import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sandbox_plan import SandboxPlan
from ..models.sandbox_status import SandboxStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_policy import SandboxNetworkPolicy


T = TypeVar("T", bound="Sandbox")


@_attrs_define
class Sandbox:
    """
    Attributes:
        id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        status (SandboxStatus):
        plan (SandboxPlan): Compute plan. Sizing matches Workflow plans of the same name.
        network_policy (SandboxNetworkPolicy):
        region (str): Region the sandbox is running in. Example: oregon.
        timeout_seconds (int): Maximum sandbox lifetime in seconds. Example: 7200.
        created_at (datetime.datetime):  Example: 2026-04-01T18:30:00Z.
        terminated_at (Union[None, Unset, datetime.datetime]): When the sandbox was terminated, or null.
    """

    id: str
    status: SandboxStatus
    plan: SandboxPlan
    network_policy: "SandboxNetworkPolicy"
    region: str
    timeout_seconds: int
    created_at: datetime.datetime
    terminated_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        plan = self.plan.value

        network_policy = self.network_policy.to_dict()

        region = self.region

        timeout_seconds = self.timeout_seconds

        created_at = self.created_at.isoformat()

        terminated_at: Union[None, Unset, str]
        if isinstance(self.terminated_at, Unset):
            terminated_at = UNSET
        elif isinstance(self.terminated_at, datetime.datetime):
            terminated_at = self.terminated_at.isoformat()
        else:
            terminated_at = self.terminated_at

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
                "createdAt": created_at,
            }
        )
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_policy import SandboxNetworkPolicy

        d = dict(src_dict)
        id = d.pop("id")

        status = SandboxStatus(d.pop("status"))

        plan = SandboxPlan(d.pop("plan"))

        network_policy = SandboxNetworkPolicy.from_dict(d.pop("networkPolicy"))

        region = d.pop("region")

        timeout_seconds = d.pop("timeoutSeconds")

        created_at = isoparse(d.pop("createdAt"))

        def _parse_terminated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                terminated_at_type_0 = isoparse(data)

                return terminated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        terminated_at = _parse_terminated_at(d.pop("terminatedAt", UNSET))

        sandbox = cls(
            id=id,
            status=status,
            plan=plan,
            network_policy=network_policy,
            region=region,
            timeout_seconds=timeout_seconds,
            created_at=created_at,
            terminated_at=terminated_at,
        )

        sandbox.additional_properties = d
        return sandbox

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
