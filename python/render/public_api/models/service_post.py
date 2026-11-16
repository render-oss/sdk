from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy import AutoDeploy
from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..models.service_type import ServiceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.background_worker_details_post import BackgroundWorkerDetailsPOST
    from ..models.build_filter import BuildFilter
    from ..models.cron_job_details_post import CronJobDetailsPOST
    from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue
    from ..models.env_var_key_value import EnvVarKeyValue
    from ..models.image import Image
    from ..models.private_service_details_post import PrivateServiceDetailsPOST
    from ..models.secret_file_input import SecretFileInput
    from ..models.static_site_details_post import StaticSiteDetailsPOST
    from ..models.web_service_details_post import WebServiceDetailsPOST


T = TypeVar("T", bound="ServicePOST")


@_attrs_define
class ServicePOST:
    """
    Attributes:
        type_ (ServiceType):
        name (str): The service's name. Must be unique within the workspace.
        owner_id (str): The ID of the workspace the service belongs to. Obtain your workspace's ID from its Settings
            page in the Render Dashboard.
        repo (str | Unset): The service's repository URL. Do not specify a branch in this string (use the `branch`
            parameter instead). Example: https://github.com/render-examples/flask-hello-world.
        auto_deploy (AutoDeploy | Unset): Deprecated: use `autoDeployTrigger` instead. You can't set both `autoDeploy`
            and `autoDeployTrigger` in the same request.

            - `yes` is equivalent to `autoDeployTrigger: commit`.
            - `no` is equivalent to `autoDeployTrigger: off`.
        auto_deploy_trigger (AutoDeployTrigger | Unset): Controls autodeploy behavior.

            - `commit`: Deploy each time a commit is pushed to the service's linked branch.
            - `checksPass`: Deploy each time a commit is pushed to the linked branch, but only after the commit's CI checks
            pass.
            - `off`: Disable autodeploys.
        branch (str | Unset): The repo branch to pull, build, and deploy. If omitted, uses the repository's default
            branch.
        image (Image | Unset):
        build_filter (BuildFilter | Unset):
        root_dir (str | Unset):
        env_vars (list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset):
        secret_files (list[SecretFileInput] | Unset):
        environment_id (str | Unset): The ID of the environment the service belongs to, if any. Obtain an environment's
            ID from its Settings page in the Render Dashboard.
        service_details (BackgroundWorkerDetailsPOST | CronJobDetailsPOST | PrivateServiceDetailsPOST |
            StaticSiteDetailsPOST | Unset | WebServiceDetailsPOST):
    """

    type_: ServiceType
    name: str
    owner_id: str
    repo: str | Unset = UNSET
    auto_deploy: AutoDeploy | Unset = UNSET
    auto_deploy_trigger: AutoDeployTrigger | Unset = UNSET
    branch: str | Unset = UNSET
    image: Image | Unset = UNSET
    build_filter: BuildFilter | Unset = UNSET
    root_dir: str | Unset = UNSET
    env_vars: list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset = UNSET
    secret_files: list[SecretFileInput] | Unset = UNSET
    environment_id: str | Unset = UNSET
    service_details: (
        BackgroundWorkerDetailsPOST
        | CronJobDetailsPOST
        | PrivateServiceDetailsPOST
        | StaticSiteDetailsPOST
        | Unset
        | WebServiceDetailsPOST
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.background_worker_details_post import BackgroundWorkerDetailsPOST  # noqa: PLC0415
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415
        from ..models.private_service_details_post import PrivateServiceDetailsPOST  # noqa: PLC0415
        from ..models.static_site_details_post import StaticSiteDetailsPOST  # noqa: PLC0415
        from ..models.web_service_details_post import WebServiceDetailsPOST  # noqa: PLC0415

        type_ = self.type_.value

        name = self.name

        owner_id = self.owner_id

        repo = self.repo

        auto_deploy: str | Unset = UNSET
        if not isinstance(self.auto_deploy, Unset):
            auto_deploy = self.auto_deploy.value

        auto_deploy_trigger: str | Unset = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        branch = self.branch

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        build_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        root_dir = self.root_dir

        env_vars: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = []
            for componentsschemasenv_var_input_array_item_data in self.env_vars:
                componentsschemasenv_var_input_array_item: dict[str, Any]
                if isinstance(componentsschemasenv_var_input_array_item_data, EnvVarKeyValue):
                    componentsschemasenv_var_input_array_item = componentsschemasenv_var_input_array_item_data.to_dict()
                else:
                    componentsschemasenv_var_input_array_item = componentsschemasenv_var_input_array_item_data.to_dict()

                env_vars.append(componentsschemasenv_var_input_array_item)

        secret_files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secret_files, Unset):
            secret_files = []
            for secret_files_item_data in self.secret_files:
                secret_files_item = secret_files_item_data.to_dict()
                secret_files.append(secret_files_item)

        environment_id = self.environment_id

        service_details: dict[str, Any] | Unset
        if isinstance(self.service_details, Unset):
            service_details = UNSET
        elif isinstance(self.service_details, StaticSiteDetailsPOST):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, WebServiceDetailsPOST):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, PrivateServiceDetailsPOST):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, BackgroundWorkerDetailsPOST):
            service_details = self.service_details.to_dict()
        else:
            service_details = self.service_details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "ownerId": owner_id,
            }
        )
        if repo is not UNSET:
            field_dict["repo"] = repo
        if auto_deploy is not UNSET:
            field_dict["autoDeploy"] = auto_deploy
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger
        if branch is not UNSET:
            field_dict["branch"] = branch
        if image is not UNSET:
            field_dict["image"] = image
        if build_filter is not UNSET:
            field_dict["buildFilter"] = build_filter
        if root_dir is not UNSET:
            field_dict["rootDir"] = root_dir
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars
        if secret_files is not UNSET:
            field_dict["secretFiles"] = secret_files
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if service_details is not UNSET:
            field_dict["serviceDetails"] = service_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.background_worker_details_post import BackgroundWorkerDetailsPOST  # noqa: PLC0415
        from ..models.build_filter import BuildFilter  # noqa: PLC0415
        from ..models.cron_job_details_post import CronJobDetailsPOST  # noqa: PLC0415
        from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue  # noqa: PLC0415
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415
        from ..models.image import Image  # noqa: PLC0415
        from ..models.private_service_details_post import PrivateServiceDetailsPOST  # noqa: PLC0415
        from ..models.secret_file_input import SecretFileInput  # noqa: PLC0415
        from ..models.static_site_details_post import StaticSiteDetailsPOST  # noqa: PLC0415
        from ..models.web_service_details_post import WebServiceDetailsPOST  # noqa: PLC0415

        d = dict(src_dict)
        type_ = ServiceType(d.pop("type"))

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        repo = d.pop("repo", UNSET)

        _auto_deploy = d.pop("autoDeploy", UNSET)
        auto_deploy: AutoDeploy | Unset
        if isinstance(_auto_deploy, Unset):
            auto_deploy = UNSET
        else:
            auto_deploy = AutoDeploy(_auto_deploy)

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: AutoDeployTrigger | Unset
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        branch = d.pop("branch", UNSET)

        _image = d.pop("image", UNSET)
        image: Image | Unset
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Image.from_dict(_image)

        _build_filter = d.pop("buildFilter", UNSET)
        build_filter: BuildFilter | Unset
        if isinstance(_build_filter, Unset):
            build_filter = UNSET
        else:
            build_filter = BuildFilter.from_dict(_build_filter)

        root_dir = d.pop("rootDir", UNSET)

        _env_vars = d.pop("envVars", UNSET)
        env_vars: list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset = UNSET
        if _env_vars is not UNSET:
            env_vars = []
            for componentsschemasenv_var_input_array_item_data in _env_vars:

                def _parse_componentsschemasenv_var_input_array_item(
                    data: object,
                ) -> EnvVarKeyGenerateValue | EnvVarKeyValue:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemasenv_var_input_type_0 = EnvVarKeyValue.from_dict(data)

                        return componentsschemasenv_var_input_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasenv_var_input_type_1 = EnvVarKeyGenerateValue.from_dict(data)

                    return componentsschemasenv_var_input_type_1

                componentsschemasenv_var_input_array_item = _parse_componentsschemasenv_var_input_array_item(
                    componentsschemasenv_var_input_array_item_data
                )

                env_vars.append(componentsschemasenv_var_input_array_item)

        _secret_files = d.pop("secretFiles", UNSET)
        secret_files: list[SecretFileInput] | Unset = UNSET
        if _secret_files is not UNSET:
            secret_files = []
            for secret_files_item_data in _secret_files:
                secret_files_item = SecretFileInput.from_dict(secret_files_item_data)

                secret_files.append(secret_files_item)

        environment_id = d.pop("environmentId", UNSET)

        def _parse_service_details(
            data: object,
        ) -> (
            BackgroundWorkerDetailsPOST
            | CronJobDetailsPOST
            | PrivateServiceDetailsPOST
            | StaticSiteDetailsPOST
            | Unset
            | WebServiceDetailsPOST
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_0 = StaticSiteDetailsPOST.from_dict(data)

                return service_details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_1 = WebServiceDetailsPOST.from_dict(data)

                return service_details_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_2 = PrivateServiceDetailsPOST.from_dict(data)

                return service_details_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_3 = BackgroundWorkerDetailsPOST.from_dict(data)

                return service_details_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            service_details_type_4 = CronJobDetailsPOST.from_dict(data)

            return service_details_type_4

        service_details = _parse_service_details(d.pop("serviceDetails", UNSET))

        service_post = cls(
            type_=type_,
            name=name,
            owner_id=owner_id,
            repo=repo,
            auto_deploy=auto_deploy,
            auto_deploy_trigger=auto_deploy_trigger,
            branch=branch,
            image=image,
            build_filter=build_filter,
            root_dir=root_dir,
            env_vars=env_vars,
            secret_files=secret_files,
            environment_id=environment_id,
            service_details=service_details,
        )

        service_post.additional_properties = d
        return service_post

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
