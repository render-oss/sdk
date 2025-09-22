from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_plan import BuildPlan
from ..models.plan import Plan
from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.region import Region
from ..models.service_env import ServiceEnv
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autoscaling_config import AutoscalingConfig
    from ..models.disk import Disk
    from ..models.docker_details import DockerDetails
    from ..models.native_environment_details import NativeEnvironmentDetails
    from ..models.previews import Previews
    from ..models.resource import Resource


T = TypeVar("T", bound="BackgroundWorkerDetails")


@_attrs_define
class BackgroundWorkerDetails:
    """
    Attributes:
        env (ServiceEnv): This field has been deprecated, runtime should be used in its place.
        env_specific_details (Union['DockerDetails', 'NativeEnvironmentDetails']):
        num_instances (int): For a *manually* scaled service, this is the number of instances the service is scaled to.
            DOES NOT indicate the number of running instances for an *autoscaled* service.
        plan (Plan): The instance type to use for the preview instance. Note that base services with any paid instance
            type can't create preview instances with the `free` instance type. Example: starter.
        region (Region): Defaults to "oregon"
        runtime (ServiceRuntime): Runtime
        build_plan (BuildPlan):
        autoscaling (Union[Unset, AutoscalingConfig]):
        disk (Union[Unset, Disk]):
        parent_server (Union[Unset, Resource]):
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        ssh_address (Union[Unset, str]): The SSH address for the service. Only present for services that have SSH
            enabled.
        max_shutdown_delay_seconds (Union[Unset, int]): The maximum amount of time (in seconds) that Render waits for
            your application process to exit gracefully after sending it a SIGTERM signal.
    """

    env: ServiceEnv
    env_specific_details: Union["DockerDetails", "NativeEnvironmentDetails"]
    num_instances: int
    plan: Plan
    region: Region
    runtime: ServiceRuntime
    build_plan: BuildPlan
    autoscaling: Union[Unset, "AutoscalingConfig"] = UNSET
    disk: Union[Unset, "Disk"] = UNSET
    parent_server: Union[Unset, "Resource"] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    ssh_address: Union[Unset, str] = UNSET
    max_shutdown_delay_seconds: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details import DockerDetails

        env = self.env.value

        env_specific_details: dict[str, Any]
        if isinstance(self.env_specific_details, DockerDetails):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        num_instances = self.num_instances

        plan = self.plan.value

        region = self.region.value

        runtime = self.runtime.value

        build_plan = self.build_plan.value

        autoscaling: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.autoscaling, Unset):
            autoscaling = self.autoscaling.to_dict()

        disk: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.disk, Unset):
            disk = self.disk.to_dict()

        parent_server: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent_server, Unset):
            parent_server = self.parent_server.to_dict()

        pull_request_previews_enabled: Union[Unset, str] = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        ssh_address = self.ssh_address

        max_shutdown_delay_seconds = self.max_shutdown_delay_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "env": env,
                "envSpecificDetails": env_specific_details,
                "numInstances": num_instances,
                "plan": plan,
                "region": region,
                "runtime": runtime,
                "buildPlan": build_plan,
            }
        )
        if autoscaling is not UNSET:
            field_dict["autoscaling"] = autoscaling
        if disk is not UNSET:
            field_dict["disk"] = disk
        if parent_server is not UNSET:
            field_dict["parentServer"] = parent_server
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if ssh_address is not UNSET:
            field_dict["sshAddress"] = ssh_address
        if max_shutdown_delay_seconds is not UNSET:
            field_dict["maxShutdownDelaySeconds"] = max_shutdown_delay_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_config import AutoscalingConfig
        from ..models.disk import Disk
        from ..models.docker_details import DockerDetails
        from ..models.native_environment_details import NativeEnvironmentDetails
        from ..models.previews import Previews
        from ..models.resource import Resource

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

        num_instances = d.pop("numInstances")

        plan = Plan(d.pop("plan"))

        region = Region(d.pop("region"))

        runtime = ServiceRuntime(d.pop("runtime"))

        build_plan = BuildPlan(d.pop("buildPlan"))

        _autoscaling = d.pop("autoscaling", UNSET)
        autoscaling: Union[Unset, AutoscalingConfig]
        if isinstance(_autoscaling, Unset):
            autoscaling = UNSET
        else:
            autoscaling = AutoscalingConfig.from_dict(_autoscaling)

        _disk = d.pop("disk", UNSET)
        disk: Union[Unset, Disk]
        if isinstance(_disk, Unset):
            disk = UNSET
        else:
            disk = Disk.from_dict(_disk)

        _parent_server = d.pop("parentServer", UNSET)
        parent_server: Union[Unset, Resource]
        if isinstance(_parent_server, Unset):
            parent_server = UNSET
        else:
            parent_server = Resource.from_dict(_parent_server)

        _pull_request_previews_enabled = d.pop("pullRequestPreviewsEnabled", UNSET)
        pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled]
        if isinstance(_pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = UNSET
        else:
            pull_request_previews_enabled = PullRequestPreviewsEnabled(_pull_request_previews_enabled)

        _previews = d.pop("previews", UNSET)
        previews: Union[Unset, Previews]
        if isinstance(_previews, Unset):
            previews = UNSET
        else:
            previews = Previews.from_dict(_previews)

        ssh_address = d.pop("sshAddress", UNSET)

        max_shutdown_delay_seconds = d.pop("maxShutdownDelaySeconds", UNSET)

        background_worker_details = cls(
            env=env,
            env_specific_details=env_specific_details,
            num_instances=num_instances,
            plan=plan,
            region=region,
            runtime=runtime,
            build_plan=build_plan,
            autoscaling=autoscaling,
            disk=disk,
            parent_server=parent_server,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            ssh_address=ssh_address,
            max_shutdown_delay_seconds=max_shutdown_delay_seconds,
        )

        background_worker_details.additional_properties = d
        return background_worker_details

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
