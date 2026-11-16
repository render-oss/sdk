from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan import Plan
from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.render_subdomain_policy import RenderSubdomainPolicy
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cache import Cache
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.docker_details_patch import DockerDetailsPATCH
    from ..models.maintenance_mode import MaintenanceMode
    from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH
    from ..models.previews import Previews


T = TypeVar("T", bound="WebServiceDetailsPATCH")


@_attrs_define
class WebServiceDetailsPATCH:
    """
    Attributes:
        env_specific_details (DockerDetailsPATCH | NativeEnvironmentDetailsPATCH | Unset):
        health_check_path (str | Unset):
        maintenance_mode (MaintenanceMode | Unset):
        plan (Plan | Unset): The compute plan to use. Legacy variants (`*_legacy`) identify grandfathered plans no
            longer offered for new services. Note that base services on any paid compute plan can't create preview instances
            with the `free` plan. Example: starter.
        pre_deploy_command (str | Unset):
        pull_request_previews_enabled (PullRequestPreviewsEnabled | Unset): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Previews | Unset):
        runtime (ServiceRuntime | Unset): Runtime
        max_shutdown_delay_seconds (int | Unset): The maximum amount of time (in seconds) that Render waits for your
            application process to exit gracefully after sending it a SIGTERM signal.
        render_subdomain_policy (RenderSubdomainPolicy | Unset): Controls whether render.com subdomains are available
            for the service
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
        cache (Cache | Unset):
    """

    env_specific_details: DockerDetailsPATCH | NativeEnvironmentDetailsPATCH | Unset = UNSET
    health_check_path: str | Unset = UNSET
    maintenance_mode: MaintenanceMode | Unset = UNSET
    plan: Plan | Unset = UNSET
    pre_deploy_command: str | Unset = UNSET
    pull_request_previews_enabled: PullRequestPreviewsEnabled | Unset = UNSET
    previews: Previews | Unset = UNSET
    runtime: ServiceRuntime | Unset = UNSET
    max_shutdown_delay_seconds: int | Unset = UNSET
    render_subdomain_policy: RenderSubdomainPolicy | Unset = UNSET
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    cache: Cache | Unset = UNSET
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

        health_check_path = self.health_check_path

        maintenance_mode: dict[str, Any] | Unset = UNSET
        if not isinstance(self.maintenance_mode, Unset):
            maintenance_mode = self.maintenance_mode.to_dict()

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

        runtime: str | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

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

        cache: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cache, Unset):
            cache = self.cache.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
        if health_check_path is not UNSET:
            field_dict["healthCheckPath"] = health_check_path
        if maintenance_mode is not UNSET:
            field_dict["maintenanceMode"] = maintenance_mode
        if plan is not UNSET:
            field_dict["plan"] = plan
        if pre_deploy_command is not UNSET:
            field_dict["preDeployCommand"] = pre_deploy_command
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if max_shutdown_delay_seconds is not UNSET:
            field_dict["maxShutdownDelaySeconds"] = max_shutdown_delay_seconds
        if render_subdomain_policy is not UNSET:
            field_dict["renderSubdomainPolicy"] = render_subdomain_policy
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list
        if cache is not UNSET:
            field_dict["cache"] = cache

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cache import Cache  # noqa: PLC0415
        from ..models.cidr_block_and_description import CidrBlockAndDescription  # noqa: PLC0415
        from ..models.docker_details_patch import DockerDetailsPATCH  # noqa: PLC0415
        from ..models.maintenance_mode import MaintenanceMode  # noqa: PLC0415
        from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH  # noqa: PLC0415
        from ..models.previews import Previews  # noqa: PLC0415

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

        health_check_path = d.pop("healthCheckPath", UNSET)

        _maintenance_mode = d.pop("maintenanceMode", UNSET)
        maintenance_mode: MaintenanceMode | Unset
        if isinstance(_maintenance_mode, Unset):
            maintenance_mode = UNSET
        else:
            maintenance_mode = MaintenanceMode.from_dict(_maintenance_mode)

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

        _runtime = d.pop("runtime", UNSET)
        runtime: ServiceRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = ServiceRuntime(_runtime)

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

        _cache = d.pop("cache", UNSET)
        cache: Cache | Unset
        if isinstance(_cache, Unset):
            cache = UNSET
        else:
            cache = Cache.from_dict(_cache)

        web_service_details_patch = cls(
            env_specific_details=env_specific_details,
            health_check_path=health_check_path,
            maintenance_mode=maintenance_mode,
            plan=plan,
            pre_deploy_command=pre_deploy_command,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            runtime=runtime,
            max_shutdown_delay_seconds=max_shutdown_delay_seconds,
            render_subdomain_policy=render_subdomain_policy,
            ip_allow_list=ip_allow_list,
            cache=cache,
        )

        web_service_details_patch.additional_properties = d
        return web_service_details_patch

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
