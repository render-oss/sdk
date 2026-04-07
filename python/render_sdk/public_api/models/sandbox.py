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
    from ..models.sandbox_env import SandboxEnv
    from ..models.sandbox_error import SandboxError
    from ..models.sandbox_network_policy import SandboxNetworkPolicy
    from ..models.sandbox_tags import SandboxTags


T = TypeVar("T", bound="Sandbox")


@_attrs_define
class Sandbox:
    """
    Attributes:
        id (str):  Example: sb-cph1rs3idesc73a2b2mg.
        status (SandboxStatus):
        plan (SandboxPlan): Compute plan.
        network_policy (SandboxNetworkPolicy):
        env (SandboxEnv): Inline environment variables. Secret values are redacted.
        tags (SandboxTags): Key-value metadata for filtering and cost tracking.
        region (str): Region the sandbox is running in. Example: oregon.
        timeout (int): Maximum sandbox lifetime in seconds. Example: 7200.
        idle_timeout (int): Seconds of inactivity before automatic lifecycle action. Example: 900.
        created_at (datetime.datetime):  Example: 2026-04-01T18:30:00Z.
        base (Union[None, Unset, str]): Render base image used, or null if a custom image is specified. Example:
            render/sandbox-node.
        image (Union[None, Unset, str]): OCI image reference, or null if using a Render base image.
        env_group (Union[None, Unset, str]): Attached environment group name or ID, or null.
        terminated_at (Union[None, Unset, datetime.datetime]): When the sandbox was terminated, or null.
        error (Union[Unset, SandboxError]):
    """

    id: str
    status: SandboxStatus
    plan: SandboxPlan
    network_policy: "SandboxNetworkPolicy"
    env: "SandboxEnv"
    tags: "SandboxTags"
    region: str
    timeout: int
    idle_timeout: int
    created_at: datetime.datetime
    base: Union[None, Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    env_group: Union[None, Unset, str] = UNSET
    terminated_at: Union[None, Unset, datetime.datetime] = UNSET
    error: Union[Unset, "SandboxError"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        plan = self.plan.value

        network_policy = self.network_policy.to_dict()

        env = self.env.to_dict()

        tags = self.tags.to_dict()

        region = self.region

        timeout = self.timeout

        idle_timeout = self.idle_timeout

        created_at = self.created_at.isoformat()

        base: Union[None, Unset, str]
        if isinstance(self.base, Unset):
            base = UNSET
        else:
            base = self.base

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        env_group: Union[None, Unset, str]
        if isinstance(self.env_group, Unset):
            env_group = UNSET
        else:
            env_group = self.env_group

        terminated_at: Union[None, Unset, str]
        if isinstance(self.terminated_at, Unset):
            terminated_at = UNSET
        elif isinstance(self.terminated_at, datetime.datetime):
            terminated_at = self.terminated_at.isoformat()
        else:
            terminated_at = self.terminated_at

        error: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "plan": plan,
                "networkPolicy": network_policy,
                "env": env,
                "tags": tags,
                "region": region,
                "timeout": timeout,
                "idleTimeout": idle_timeout,
                "createdAt": created_at,
            }
        )
        if base is not UNSET:
            field_dict["base"] = base
        if image is not UNSET:
            field_dict["image"] = image
        if env_group is not UNSET:
            field_dict["envGroup"] = env_group
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_env import SandboxEnv
        from ..models.sandbox_error import SandboxError
        from ..models.sandbox_network_policy import SandboxNetworkPolicy
        from ..models.sandbox_tags import SandboxTags

        d = dict(src_dict)
        id = d.pop("id")

        status = SandboxStatus(d.pop("status"))

        plan = SandboxPlan(d.pop("plan"))

        network_policy = SandboxNetworkPolicy.from_dict(d.pop("networkPolicy"))

        env = SandboxEnv.from_dict(d.pop("env"))

        tags = SandboxTags.from_dict(d.pop("tags"))

        region = d.pop("region")

        timeout = d.pop("timeout")

        idle_timeout = d.pop("idleTimeout")

        created_at = isoparse(d.pop("createdAt"))

        def _parse_base(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        base = _parse_base(d.pop("base", UNSET))

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_env_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        env_group = _parse_env_group(d.pop("envGroup", UNSET))

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

        _error = d.pop("error", UNSET)
        error: Union[Unset, SandboxError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = SandboxError.from_dict(_error)

        sandbox = cls(
            id=id,
            status=status,
            plan=plan,
            network_policy=network_policy,
            env=env,
            tags=tags,
            region=region,
            timeout=timeout,
            idle_timeout=idle_timeout,
            created_at=created_at,
            base=base,
            image=image,
            env_group=env_group,
            terminated_at=terminated_at,
            error=error,
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
