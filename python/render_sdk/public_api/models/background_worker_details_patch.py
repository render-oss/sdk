from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.paid_plan import PaidPlan
from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.service_runtime import ServiceRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.docker_details_patch import DockerDetailsPATCH
    from ..models.native_environment_details_patch import NativeEnvironmentDetailsPATCH
    from ..models.previews import Previews


T = TypeVar("T", bound="BackgroundWorkerDetailsPATCH")


@_attrs_define
class BackgroundWorkerDetailsPATCH:
    """
    Attributes:
        env_specific_details (Union['DockerDetailsPATCH', 'NativeEnvironmentDetailsPATCH', Unset]):
        plan (Union[Unset, PaidPlan]): Defaults to "starter"
        pre_deploy_command (Union[Unset, str]):
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        runtime (Union[Unset, ServiceRuntime]): Runtime
        max_shutdown_delay_seconds (Union[Unset, int]): The maximum amount of time (in seconds) that Render waits for
            your application process to exit gracefully after sending it a SIGTERM signal.
    """

    env_specific_details: Union["DockerDetailsPATCH", "NativeEnvironmentDetailsPATCH", Unset] = UNSET
    plan: Union[Unset, PaidPlan] = UNSET
    pre_deploy_command: Union[Unset, str] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    runtime: Union[Unset, ServiceRuntime] = UNSET
    max_shutdown_delay_seconds: Union[Unset, int] = UNSET
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if env_specific_details is not UNSET:
            field_dict["envSpecificDetails"] = env_specific_details
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.docker_details_patch import DockerDetailsPATCH
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

        background_worker_details_patch = cls(
            env_specific_details=env_specific_details,
            plan=plan,
            pre_deploy_command=pre_deploy_command,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            runtime=runtime,
            max_shutdown_delay_seconds=max_shutdown_delay_seconds,
        )

        background_worker_details_patch.additional_properties = d
        return background_worker_details_patch

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
