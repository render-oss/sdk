from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.paid_plan import PaidPlan
from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.region import Region
from ..models.render_subdomain_policy import RenderSubdomainPolicy
from ..models.service_env import ServiceEnv
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autoscaling_config import AutoscalingConfig
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.docker_details_post import DockerDetailsPOST
    from ..models.maintenance_mode import MaintenanceMode
    from ..models.native_environment_details_post import NativeEnvironmentDetailsPOST
    from ..models.previews import Previews
    from ..models.service_disk import ServiceDisk


T = TypeVar("T", bound="WebServiceDetailsPOST")


@_attrs_define
class WebServiceDetailsPOST:
    """
    Attributes:
        runtime (ServiceRuntime): Runtime
        autoscaling (Union[Unset, AutoscalingConfig]):
        disk (Union[Unset, ServiceDisk]):
        env (Union[Unset, ServiceEnv]): This field has been deprecated, runtime should be used in its place.
        env_specific_details (Union['DockerDetailsPOST', 'NativeEnvironmentDetailsPOST', Unset]):
        health_check_path (Union[Unset, str]):
        maintenance_mode (Union[Unset, MaintenanceMode]):
        num_instances (Union[Unset, int]): Defaults to 1
        plan (Union[Unset, PaidPlan]): Defaults to "starter"
        pre_deploy_command (Union[Unset, str]):
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        region (Union[Unset, Region]): Defaults to "oregon"
        max_shutdown_delay_seconds (Union[Unset, int]): The maximum amount of time (in seconds) that Render waits for
            your application process to exit gracefully after sending it a SIGTERM signal.
        render_subdomain_policy (Union[Unset, RenderSubdomainPolicy]): Controls whether render.com subdomains are
            available for the service
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    runtime: ServiceRuntime
    autoscaling: Union[Unset, "AutoscalingConfig"] = UNSET
    disk: Union[Unset, "ServiceDisk"] = UNSET
    env: Union[Unset, ServiceEnv] = UNSET
    env_specific_details: Union["DockerDetailsPOST", "NativeEnvironmentDetailsPOST", Unset] = UNSET
    health_check_path: Union[Unset, str] = UNSET
    maintenance_mode: Union[Unset, "MaintenanceMode"] = UNSET
    num_instances: Union[Unset, int] = UNSET
    plan: Union[Unset, PaidPlan] = UNSET
    pre_deploy_command: Union[Unset, str] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    region: Union[Unset, Region] = UNSET
    max_shutdown_delay_seconds: Union[Unset, int] = UNSET
    render_subdomain_policy: Union[Unset, RenderSubdomainPolicy] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details_post import DockerDetailsPOST

        runtime = self.runtime.value

        autoscaling: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.autoscaling, Unset):
            autoscaling = self.autoscaling.to_dict()

        disk: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.disk, Unset):
            disk = self.disk.to_dict()

        env: Union[Unset, str] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.value

        env_specific_details: Union[Unset, dict[str, Any]]
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetailsPOST):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        health_check_path = self.health_check_path

        maintenance_mode: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maintenance_mode, Unset):
            maintenance_mode = self.maintenance_mode.to_dict()

        num_instances = self.num_instances

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        pre_deploy_command = self.pre_deploy_command

        pull_request_previews_enabled: Union[Unset, str] = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        max_shutdown_delay_seconds = self.max_shutdown_delay_seconds

        render_subdomain_policy: Union[Unset, str] = UNSET
        if not isinstance(self.render_subdomain_policy, Unset):
            render_subdomain_policy = self.render_subdomain_policy.value

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runtime": runtime,
            }
        )
        if autoscaling is not UNSET:
            field_dict["autoscaling"] = autoscaling
        if disk is not UNSET:
            field_dict["disk"] = disk
        if env is not UNSET:
            field_dict["env"] = env
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if health_check_path is not UNSET:
            field_dict["healthCheckPath"] = health_check_path
        if maintenance_mode is not UNSET:
            field_dict["maintenanceMode"] = maintenance_mode
        if num_instances is not UNSET:
            field_dict["numInstances"] = num_instances
        if plan is not UNSET:
            field_dict["plan"] = plan
        if pre_deploy_command is not UNSET:
            field_dict["preDeployCommand"] = pre_deploy_command
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if region is not UNSET:
            field_dict["region"] = region
        if max_shutdown_delay_seconds is not UNSET:
            field_dict["maxShutdownDelaySeconds"] = max_shutdown_delay_seconds
        if render_subdomain_policy is not UNSET:
            field_dict["renderSubdomainPolicy"] = render_subdomain_policy
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_config import AutoscalingConfig
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.docker_details_post import DockerDetailsPOST
        from ..models.maintenance_mode import MaintenanceMode
        from ..models.native_environment_details_post import NativeEnvironmentDetailsPOST
        from ..models.previews import Previews
        from ..models.service_disk import ServiceDisk

        d = dict(src_dict)
        runtime = ServiceRuntime(d.pop("runtime"))

        _autoscaling = d.pop("autoscaling", UNSET)
        autoscaling: Union[Unset, AutoscalingConfig]
        if isinstance(_autoscaling, Unset):
            autoscaling = UNSET
        else:
            autoscaling = AutoscalingConfig.from_dict(_autoscaling)

        _disk = d.pop("disk", UNSET)
        disk: Union[Unset, ServiceDisk]
        if isinstance(_disk, Unset):
            disk = UNSET
        else:
            disk = ServiceDisk.from_dict(_disk)

        _env = d.pop("env", UNSET)
        env: Union[Unset, ServiceEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ServiceEnv(_env)

        def _parse_env_specific_details(
            data: object,
        ) -> Union["DockerDetailsPOST", "NativeEnvironmentDetailsPOST", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_post_type_0 = DockerDetailsPOST.from_dict(data)

                return componentsschemasenv_specific_details_post_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_post_type_1 = NativeEnvironmentDetailsPOST.from_dict(data)

            return componentsschemasenv_specific_details_post_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        health_check_path = d.pop("healthCheckPath", UNSET)

        _maintenance_mode = d.pop("maintenanceMode", UNSET)
        maintenance_mode: Union[Unset, MaintenanceMode]
        if isinstance(_maintenance_mode, Unset):
            maintenance_mode = UNSET
        else:
            maintenance_mode = MaintenanceMode.from_dict(_maintenance_mode)

        num_instances = d.pop("numInstances", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, PaidPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PaidPlan(_plan)

        pre_deploy_command = d.pop("preDeployCommand", UNSET)

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

        _region = d.pop("region", UNSET)
        region: Union[Unset, Region]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

        max_shutdown_delay_seconds = d.pop("maxShutdownDelaySeconds", UNSET)

        _render_subdomain_policy = d.pop("renderSubdomainPolicy", UNSET)
        render_subdomain_policy: Union[Unset, RenderSubdomainPolicy]
        if isinstance(_render_subdomain_policy, Unset):
            render_subdomain_policy = UNSET
        else:
            render_subdomain_policy = RenderSubdomainPolicy(_render_subdomain_policy)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        web_service_details_post = cls(
            runtime=runtime,
            autoscaling=autoscaling,
            disk=disk,
            env=env,
            env_specific_details=env_specific_details,
            health_check_path=health_check_path,
            maintenance_mode=maintenance_mode,
            num_instances=num_instances,
            plan=plan,
            pre_deploy_command=pre_deploy_command,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            region=region,
            max_shutdown_delay_seconds=max_shutdown_delay_seconds,
            render_subdomain_policy=render_subdomain_policy,
            ip_allow_list=ip_allow_list,
        )

        web_service_details_post.additional_properties = d
        return web_service_details_post

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
