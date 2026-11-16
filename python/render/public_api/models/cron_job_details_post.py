from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.paid_plan import PaidPlan
from ..models.region import Region
from ..models.service_env import ServiceEnv
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docker_details import DockerDetails
    from ..models.native_environment_details import NativeEnvironmentDetails


T = TypeVar("T", bound="CronJobDetailsPOST")


@_attrs_define
class CronJobDetailsPOST:
    """
    Attributes:
        schedule (str):
        build_source_id (str | Unset):
        env (ServiceEnv | Unset): This field has been deprecated, runtime should be used in its place.
        runtime (ServiceRuntime | Unset): Runtime
        env_specific_details (DockerDetails | NativeEnvironmentDetails | Unset):
        plan (PaidPlan | Unset): Defaults to `0.5c-512mb` when creating a new service.
        region (Region | Unset): Defaults to "oregon"
    """

    schedule: str
    build_source_id: str | Unset = UNSET
    env: ServiceEnv | Unset = UNSET
    runtime: ServiceRuntime | Unset = UNSET
    env_specific_details: DockerDetails | NativeEnvironmentDetails | Unset = UNSET
    plan: PaidPlan | Unset = UNSET
    region: Region | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details import DockerDetails  # noqa: PLC0415

        schedule = self.schedule

        build_source_id = self.build_source_id

        env: str | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.value

        runtime: str | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        env_specific_details: dict[str, Any] | Unset
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetails):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        plan: str | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        region: str | Unset = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schedule": schedule,
            }
        )
        if build_source_id is not UNSET:
            field_dict["buildSourceId"] = build_source_id
        if env is not UNSET:
            field_dict["env"] = env
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if plan is not UNSET:
            field_dict["plan"] = plan
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_details import DockerDetails  # noqa: PLC0415
        from ..models.native_environment_details import NativeEnvironmentDetails  # noqa: PLC0415

        d = dict(src_dict)
        schedule = d.pop("schedule")

        build_source_id = d.pop("buildSourceId", UNSET)

        _env = d.pop("env", UNSET)
        env: ServiceEnv | Unset
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ServiceEnv(_env)

        _runtime = d.pop("runtime", UNSET)
        runtime: ServiceRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = ServiceRuntime(_runtime)

        def _parse_env_specific_details(data: object) -> DockerDetails | NativeEnvironmentDetails | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_type_0 = DockerDetails.from_dict(data)

                return componentsschemasenv_specific_details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_type_1 = NativeEnvironmentDetails.from_dict(data)

            return componentsschemasenv_specific_details_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        _plan = d.pop("plan", UNSET)
        plan: PaidPlan | Unset
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PaidPlan(_plan)

        _region = d.pop("region", UNSET)
        region: Region | Unset
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

        cron_job_details_post = cls(
            schedule=schedule,
            build_source_id=build_source_id,
            env=env,
            runtime=runtime,
            env_specific_details=env_specific_details,
            plan=plan,
            region=region,
        )

        cron_job_details_post.additional_properties = d
        return cron_job_details_post

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
