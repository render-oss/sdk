from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.paid_plan import PaidPlan
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docker_details_patch import DockerDetailsPATCH
    from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH


T = TypeVar("T", bound="CronJobDetailsPATCH")


@_attrs_define
class CronJobDetailsPATCH:
    """
    Attributes:
        env_specific_details (DockerDetailsPATCH | NativeEnvironmentDetailsPATCH | Unset):
        plan (PaidPlan | Unset): Defaults to `0.5c-512mb` when creating a new service.
        schedule (str | Unset):
        runtime (ServiceRuntime | Unset): Runtime
    """

    env_specific_details: DockerDetailsPATCH | NativeEnvironmentDetailsPATCH | Unset = UNSET
    plan: PaidPlan | Unset = UNSET
    schedule: str | Unset = UNSET
    runtime: ServiceRuntime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details_patch import DockerDetailsPATCH  # noqa: PLC0415

        env_specific_details: dict[str, Any] | Unset
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetailsPATCH):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        plan: str | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        schedule = self.schedule

        runtime: str | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if plan is not UNSET:
            field_dict["plan"] = plan
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if runtime is not UNSET:
            field_dict["runtime"] = runtime

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_details_patch import DockerDetailsPATCH  # noqa: PLC0415
        from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_env_specific_details(data: object) -> DockerDetailsPATCH | NativeEnvironmentDetailsPATCH | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_patch_type_0 = DockerDetailsPATCH.from_dict(data)

                return componentsschemasenv_specific_details_patch_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_patch_type_1 = NativeEnvironmentDetailsPATCH.from_dict(data)

            return componentsschemasenv_specific_details_patch_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        _plan = d.pop("plan", UNSET)
        plan: PaidPlan | Unset
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PaidPlan(_plan)

        schedule = d.pop("schedule", UNSET)

        _runtime = d.pop("runtime", UNSET)
        runtime: ServiceRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = ServiceRuntime(_runtime)

        cron_job_details_patch = cls(
            env_specific_details=env_specific_details,
            plan=plan,
            schedule=schedule,
            runtime=runtime,
        )

        cron_job_details_patch.additional_properties = d
        return cron_job_details_patch

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
