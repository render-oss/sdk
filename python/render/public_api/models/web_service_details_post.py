from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.internal_routing import InternalRouting
from ..models.plan import Plan
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
        build_source_id (str | Unset):
        autoscaling (AutoscalingConfig | Unset):
        disk (ServiceDisk | Unset):
        env (ServiceEnv | Unset): This field has been deprecated, runtime should be used in its place.
        runtime (ServiceRuntime | Unset): Runtime
        env_specific_details (DockerDetailsPOST | NativeEnvironmentDetailsPOST | Unset):
        health_check_path (str | Unset):
        maintenance_mode (MaintenanceMode | Unset):
        num_instances (int | Unset): Defaults to 1
        internal_routing (InternalRouting | Unset): How requests from other services in the same workspace are routed to
            this service's instances. When unset, Render's standard routing is used. `ipOnly` routes requests directly to
            individual instance IPs. Only available to workspaces that Render has granted access. Can only be set when
            creating a service.
        plan (Plan | Unset): The compute plan to use. Legacy variants (`*_legacy`) identify grandfathered plans no
            longer offered for new services. Note that base services on any paid compute plan can't create preview instances
            with the `free` plan. Example: starter.
        pre_deploy_command (str | Unset):
        pull_request_previews_enabled (PullRequestPreviewsEnabled | Unset): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Previews | Unset):
        region (Region | Unset): Defaults to "oregon"
        max_shutdown_delay_seconds (int | Unset): The maximum amount of time (in seconds) that Render waits for your
            application process to exit gracefully after sending it a SIGTERM signal.
        render_subdomain_policy (RenderSubdomainPolicy | Unset): Controls whether render.com subdomains are available
            for the service
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
    """

    build_source_id: str | Unset = UNSET
    autoscaling: AutoscalingConfig | Unset = UNSET
    disk: ServiceDisk | Unset = UNSET
    env: ServiceEnv | Unset = UNSET
    runtime: ServiceRuntime | Unset = UNSET
    env_specific_details: DockerDetailsPOST | NativeEnvironmentDetailsPOST | Unset = UNSET
    health_check_path: str | Unset = UNSET
    maintenance_mode: MaintenanceMode | Unset = UNSET
    num_instances: int | Unset = UNSET
    internal_routing: InternalRouting | Unset = UNSET
    plan: Plan | Unset = UNSET
    pre_deploy_command: str | Unset = UNSET
    pull_request_previews_enabled: PullRequestPreviewsEnabled | Unset = UNSET
    previews: Previews | Unset = UNSET
    region: Region | Unset = UNSET
    max_shutdown_delay_seconds: int | Unset = UNSET
    render_subdomain_policy: RenderSubdomainPolicy | Unset = UNSET
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details_post import DockerDetailsPOST  # noqa: PLC0415

        build_source_id = self.build_source_id

        autoscaling: dict[str, Any] | Unset = UNSET
        if not isinstance(self.autoscaling, Unset):
            autoscaling = self.autoscaling.to_dict()

        disk: dict[str, Any] | Unset = UNSET
        if not isinstance(self.disk, Unset):
            disk = self.disk.to_dict()

        env: str | Unset = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.value

        runtime: str | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        env_specific_details: dict[str, Any] | Unset
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetailsPOST):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        health_check_path = self.health_check_path

        maintenance_mode: dict[str, Any] | Unset = UNSET
        if not isinstance(self.maintenance_mode, Unset):
            maintenance_mode = self.maintenance_mode.to_dict()

        num_instances = self.num_instances

        internal_routing: str | Unset = UNSET
        if not isinstance(self.internal_routing, Unset):
            internal_routing = self.internal_routing.value

        plan: str | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        pre_deploy_command = self.pre_deploy_command

        pull_request_previews_enabled: str | Unset = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: dict[str, Any] | Unset = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        region: str | Unset = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        max_shutdown_delay_seconds = self.max_shutdown_delay_seconds

        render_subdomain_policy: str | Unset = UNSET
        if not isinstance(self.render_subdomain_policy, Unset):
            render_subdomain_policy = self.render_subdomain_policy.value

        ip_allow_list: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if build_source_id is not UNSET:
            field_dict["buildSourceId"] = build_source_id
        if autoscaling is not UNSET:
            field_dict["autoscaling"] = autoscaling
        if disk is not UNSET:
            field_dict["disk"] = disk
        if env is not UNSET:
            field_dict["env"] = env
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if health_check_path is not UNSET:
            field_dict["healthCheckPath"] = health_check_path
        if maintenance_mode is not UNSET:
            field_dict["maintenanceMode"] = maintenance_mode
        if num_instances is not UNSET:
            field_dict["numInstances"] = num_instances
        if internal_routing is not UNSET:
            field_dict["internalRouting"] = internal_routing
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
        from ..models.autoscaling_config import AutoscalingConfig  # noqa: PLC0415
        from ..models.cidr_block_and_description import CidrBlockAndDescription  # noqa: PLC0415
        from ..models.docker_details_post import DockerDetailsPOST  # noqa: PLC0415
        from ..models.maintenance_mode import MaintenanceMode  # noqa: PLC0415
        from ..models.native_environment_details_post import NativeEnvironmentDetailsPOST  # noqa: PLC0415
        from ..models.previews import Previews  # noqa: PLC0415
        from ..models.service_disk import ServiceDisk  # noqa: PLC0415

        d = dict(src_dict)
        build_source_id = d.pop("buildSourceId", UNSET)

        _autoscaling = d.pop("autoscaling", UNSET)
        autoscaling: AutoscalingConfig | Unset
        if isinstance(_autoscaling, Unset):
            autoscaling = UNSET
        else:
            autoscaling = AutoscalingConfig.from_dict(_autoscaling)

        _disk = d.pop("disk", UNSET)
        disk: ServiceDisk | Unset
        if isinstance(_disk, Unset):
            disk = UNSET
        else:
            disk = ServiceDisk.from_dict(_disk)

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

        def _parse_env_specific_details(data: object) -> DockerDetailsPOST | NativeEnvironmentDetailsPOST | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_post_type_0 = DockerDetailsPOST.from_dict(data)

                return componentsschemasenv_specific_details_post_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_post_type_1 = NativeEnvironmentDetailsPOST.from_dict(data)

            return componentsschemasenv_specific_details_post_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        health_check_path = d.pop("healthCheckPath", UNSET)

        _maintenance_mode = d.pop("maintenanceMode", UNSET)
        maintenance_mode: MaintenanceMode | Unset
        if isinstance(_maintenance_mode, Unset):
            maintenance_mode = UNSET
        else:
            maintenance_mode = MaintenanceMode.from_dict(_maintenance_mode)

        num_instances = d.pop("numInstances", UNSET)

        _internal_routing = d.pop("internalRouting", UNSET)
        internal_routing: InternalRouting | Unset
        if isinstance(_internal_routing, Unset):
            internal_routing = UNSET
        else:
            internal_routing = InternalRouting(_internal_routing)

        _plan = d.pop("plan", UNSET)
        plan: Plan | Unset
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = Plan(_plan)

        pre_deploy_command = d.pop("preDeployCommand", UNSET)

        _pull_request_previews_enabled = d.pop("pullRequestPreviewsEnabled", UNSET)
        pull_request_previews_enabled: PullRequestPreviewsEnabled | Unset
        if isinstance(_pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = UNSET
        else:
            pull_request_previews_enabled = PullRequestPreviewsEnabled(_pull_request_previews_enabled)

        _previews = d.pop("previews", UNSET)
        previews: Previews | Unset
        if isinstance(_previews, Unset):
            previews = UNSET
        else:
            previews = Previews.from_dict(_previews)

        _region = d.pop("region", UNSET)
        region: Region | Unset
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = Region(_region)

        max_shutdown_delay_seconds = d.pop("maxShutdownDelaySeconds", UNSET)

        _render_subdomain_policy = d.pop("renderSubdomainPolicy", UNSET)
        render_subdomain_policy: RenderSubdomainPolicy | Unset
        if isinstance(_render_subdomain_policy, Unset):
            render_subdomain_policy = UNSET
        else:
            render_subdomain_policy = RenderSubdomainPolicy(_render_subdomain_policy)

        _ip_allow_list = d.pop("ipAllowList", UNSET)
        ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
        if _ip_allow_list is not UNSET:
            ip_allow_list = []
            for ip_allow_list_item_data in _ip_allow_list:
                ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

                ip_allow_list.append(ip_allow_list_item)

        web_service_details_post = cls(
            build_source_id=build_source_id,
            autoscaling=autoscaling,
            disk=disk,
            env=env,
            runtime=runtime,
            env_specific_details=env_specific_details,
            health_check_path=health_check_path,
            maintenance_mode=maintenance_mode,
            num_instances=num_instances,
            internal_routing=internal_routing,
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
