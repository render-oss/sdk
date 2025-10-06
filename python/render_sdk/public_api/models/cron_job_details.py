import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.build_plan import BuildPlan
from ..models.plan import Plan
from ..models.region import Region
from ..models.service_env import ServiceEnv
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docker_details import DockerDetails
    from ..models.native_environment_details import NativeEnvironmentDetails


T = TypeVar("T", bound="CronJobDetails")


@_attrs_define
class CronJobDetails:
    """
    Attributes:
        env (ServiceEnv): This field has been deprecated, runtime should be used in its place.
        env_specific_details (Union['DockerDetails', 'NativeEnvironmentDetails']):
        plan (Plan): The instance type to use for the preview instance. Note that base services with any paid instance
            type can't create preview instances with the `free` instance type. Example: starter.
        region (Region): Defaults to "oregon"
        runtime (ServiceRuntime): Runtime
        schedule (str):
        build_plan (BuildPlan):
        last_successful_run_at (Union[Unset, datetime.datetime]):
    """

    env: ServiceEnv
    env_specific_details: Union["DockerDetails", "NativeEnvironmentDetails"]
    plan: Plan
    region: Region
    runtime: ServiceRuntime
    schedule: str
    build_plan: BuildPlan
    last_successful_run_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details import DockerDetails

        env = self.env.value

        env_specific_details: dict[str, Any]
        if isinstance(self.env_specific_details, DockerDetails):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        plan = self.plan.value

        region = self.region.value

        runtime = self.runtime.value

        schedule = self.schedule

        build_plan = self.build_plan.value

        last_successful_run_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_successful_run_at, Unset):
            last_successful_run_at = self.last_successful_run_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "env": env,
                "envSpecificDetails": env_specific_details,
                "plan": plan,
                "region": region,
                "runtime": runtime,
                "schedule": schedule,
                "buildPlan": build_plan,
            }
        )
        if last_successful_run_at is not UNSET:
            field_dict["lastSuccessfulRunAt"] = last_successful_run_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_details import DockerDetails
        from ..models.native_environment_details import NativeEnvironmentDetails

        d = dict(src_dict)
        env = ServiceEnv(d.pop("env"))

        def _parse_env_specific_details(data: object) -> Union["DockerDetails", "NativeEnvironmentDetails"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_type_0 = DockerDetails.from_dict(data)

                return componentsschemasenv_specific_details_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_type_1 = NativeEnvironmentDetails.from_dict(data)

            return componentsschemasenv_specific_details_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails"))

        plan = Plan(d.pop("plan"))

        region = Region(d.pop("region"))

        runtime = ServiceRuntime(d.pop("runtime"))

        schedule = d.pop("schedule")

        build_plan = BuildPlan(d.pop("buildPlan"))

        _last_successful_run_at = d.pop("lastSuccessfulRunAt", UNSET)
        last_successful_run_at: Union[Unset, datetime.datetime]
        if isinstance(_last_successful_run_at, Unset):
            last_successful_run_at = UNSET
        else:
            last_successful_run_at = isoparse(_last_successful_run_at)

        cron_job_details = cls(
            env=env,
            env_specific_details=env_specific_details,
            plan=plan,
            region=region,
            runtime=runtime,
            schedule=schedule,
            build_plan=build_plan,
            last_successful_run_at=last_successful_run_at,
        )

        cron_job_details.additional_properties = d
        return cron_job_details

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
