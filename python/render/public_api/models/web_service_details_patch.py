from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.paid_plan import PaidPlan
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
        env_specific_details (Union['DockerDetailsPATCH', 'NativeEnvironmentDetailsPATCH', Unset]):
        health_check_path (Union[Unset, str]):
        maintenance_mode (Union[Unset, MaintenanceMode]):
        plan (Union[Unset, PaidPlan]): Defaults to "starter"
        pre_deploy_command (Union[Unset, str]):
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        runtime (Union[Unset, ServiceRuntime]): Runtime
        max_shutdown_delay_seconds (Union[Unset, int]): The maximum amount of time (in seconds) that Render waits for
            your application process to exit gracefully after sending it a SIGTERM signal.
        render_subdomain_policy (Union[Unset, RenderSubdomainPolicy]): Controls whether render.com subdomains are
            available for the service
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
        cache (Union[Unset, Cache]):
    """

    env_specific_details: Union["DockerDetailsPATCH", "NativeEnvironmentDetailsPATCH", Unset] = UNSET
    health_check_path: Union[Unset, str] = UNSET
    maintenance_mode: Union[Unset, "MaintenanceMode"] = UNSET
    plan: Union[Unset, PaidPlan] = UNSET
    pre_deploy_command: Union[Unset, str] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    runtime: Union[Unset, ServiceRuntime] = UNSET
    max_shutdown_delay_seconds: Union[Unset, int] = UNSET
    render_subdomain_policy: Union[Unset, RenderSubdomainPolicy] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    cache: Union[Unset, "Cache"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.docker_details_patch import DockerDetailsPATCH

        env_specific_details: Union[Unset, dict[str, Any]]
        if isinstance(self.env_specific_details, Unset):
            env_specific_details = UNSET
        elif isinstance(self.env_specific_details, DockerDetailsPATCH):
            env_specific_details = self.env_specific_details.to_dict()
        else:
            env_specific_details = self.env_specific_details.to_dict()

        health_check_path = self.health_check_path

        maintenance_mode: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maintenance_mode, Unset):
            maintenance_mode = self.maintenance_mode.to_dict()

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

        runtime: Union[Unset, str] = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

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

        cache: Union[Unset, dict[str, Any]] = UNSET
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
        from ..models.cache import Cache
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.docker_details_patch import DockerDetailsPATCH
        from ..models.maintenance_mode import MaintenanceMode
        from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH
        from ..models.previews import Previews

        d = dict(src_dict)

        def _parse_env_specific_details(
            data: object,
        ) -> Union["DockerDetailsPATCH", "NativeEnvironmentDetailsPATCH", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_specific_details_patch_type_0 = DockerDetailsPATCH.from_dict(data)

                return componentsschemasenv_specific_details_patch_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasenv_specific_details_patch_type_1 = NativeEnvironmentDetailsPATCH.from_dict(data)

            return componentsschemasenv_specific_details_patch_type_1

        env_specific_details = _parse_env_specific_details(d.pop("envSpecificDetails", UNSET))

        health_check_path = d.pop("healthCheckPath", UNSET)

        _maintenance_mode = d.pop("maintenanceMode", UNSET)
        maintenance_mode: Union[Unset, MaintenanceMode]
        if isinstance(_maintenance_mode, Unset):
            maintenance_mode = UNSET
        else:
            maintenance_mode = MaintenanceMode.from_dict(_maintenance_mode)

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

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, ServiceRuntime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = ServiceRuntime(_runtime)

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

        _cache = d.pop("cache", UNSET)
        cache: Union[Unset, Cache]
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
