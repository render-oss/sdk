from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        runtime (ServiceRuntime): Runtime
        schedule (str):
        env (Union[Unset, ServiceEnv]): This field has been deprecated, runtime should be used in its place.
        env_specific_details (Union['DockerDetails', 'NativeEnvironmentDetails', Unset]):
        plan (Union[Unset, PaidPlan]): Defaults to "starter"
        region (Union[Unset, Region]): Defaults to "oregon"
    """

    runtime: ServiceRuntime
    schedule: str
    env: Union[Unset, ServiceEnv] = UNSET
    env_specific_details: Union["DockerDetails", "NativeEnvironmentDetails", Unset] = UNSET
    plan: Union[Unset, PaidPlan] = UNSET
    region: Union[Unset, Region] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details import DockerDetails

        runtime = self.runtime.value

        schedule = self.schedule

        env: Union[Unset, str] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.value

        env_specific_details: Union[Unset, dict[str, Any]]
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetails):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runtime": runtime,
                "schedule": schedule,
            }
        )
        if env is not UNSET:
            field_dict["env"] = env
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if plan is not UNSET:
            field_dict["plan"] = plan
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_details import DockerDetails
        from ..models.native_environment_details import NativeEnvironmentDetails

        d = dict(src_dict)
        runtime = ServiceRuntime(d.pop("runtime"))

        schedule = d.pop("schedule")

        _env = d.pop("env", UNSET)
        env: Union[Unset, ServiceEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ServiceEnv(_env)

        def _parse_env_specific_details(data: object) -> Union["DockerDetails", "NativeEnvironmentDetails", Unset]:
            if isinstance(data, Unset):
                return data
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

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, PaidPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PaidPlan(_plan)

        _region = d.pop("region", UNSET)
        region: Union[Unset, Region]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

        cron_job_details_post = cls(
            runtime=runtime,
            schedule=schedule,
            env=env,
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
