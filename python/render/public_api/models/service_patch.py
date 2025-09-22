from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy import AutoDeploy
from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.background_worker_details_patch import BackgroundWorkerDetailsPATCH
    from ..models.build_filter import BuildFilter
    from ..models.cron_job_details_patch import CronJobDetailsPATCH
    from ..models.image import Image
    from ..models.private_service_details_patch import PrivateServiceDetailsPATCH
    from ..models.static_site_details_patch import StaticSiteDetailsPATCH
    from ..models.web_service_details_patch import WebServiceDetailsPATCH


T = TypeVar("T", bound="ServicePATCH")


@_attrs_define
class ServicePATCH:
    """
    Attributes:
        auto_deploy (Union[Unset, AutoDeploy]):
        auto_deploy_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. commit deploys when a
            commit is pushed to a branch. checksPass waits for the branch to be green.
        repo (Union[Unset, str]):
        branch (Union[Unset, str]):
        image (Union[Unset, Image]):
        name (Union[Unset, str]):
        build_filter (Union[Unset, BuildFilter]):
        root_dir (Union[Unset, str]):
        service_details (Union['BackgroundWorkerDetailsPATCH', 'CronJobDetailsPATCH', 'PrivateServiceDetailsPATCH',
            'StaticSiteDetailsPATCH', 'WebServiceDetailsPATCH', Unset]):
    """

    auto_deploy: Union[Unset, AutoDeploy] = UNSET
    auto_deploy_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    repo: Union[Unset, str] = UNSET
    branch: Union[Unset, str] = UNSET
    image: Union[Unset, "Image"] = UNSET
    name: Union[Unset, str] = UNSET
    build_filter: Union[Unset, "BuildFilter"] = UNSET
    root_dir: Union[Unset, str] = UNSET
    service_details: Union[
        "BackgroundWorkerDetailsPATCH",
        "CronJobDetailsPATCH",
        "PrivateServiceDetailsPATCH",
        "StaticSiteDetailsPATCH",
        "WebServiceDetailsPATCH",
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.background_worker_details_patch import BackgroundWorkerDetailsPATCH
        from ..models.private_service_details_patch import PrivateServiceDetailsPATCH
        from ..models.static_site_details_patch import StaticSiteDetailsPATCH
        from ..models.web_service_details_patch import WebServiceDetailsPATCH

        auto_deploy: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy, Unset):
            auto_deploy = self.auto_deploy.value

        auto_deploy_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        repo = self.repo

        branch = self.branch

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        name = self.name

        build_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        root_dir = self.root_dir

        service_details: Union[Unset, dict[str, Any]]
        if isinstance(self.service_details, Unset):
            service_details = UNSET
        elif isinstance(self.service_details, StaticSiteDetailsPATCH):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, WebServiceDetailsPATCH):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, PrivateServiceDetailsPATCH):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, BackgroundWorkerDetailsPATCH):
            service_details = self.service_details.to_dict()
        else:
            service_details = self.service_details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_deploy is not UNSET:
            field_dict["autoDeploy"] = auto_deploy
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger
        if repo is not UNSET:
            field_dict["repo"] = repo
        if branch is not UNSET:
            field_dict["branch"] = branch
        if image is not UNSET:
            field_dict["image"] = image
        if name is not UNSET:
            field_dict["name"] = name
        if build_filter is not UNSET:
            field_dict["buildFilter"] = build_filter
        if root_dir is not UNSET:
            field_dict["rootDir"] = root_dir
        if service_details is not UNSET:
            field_dict["serviceDetails"] = service_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.background_worker_details_patch import BackgroundWorkerDetailsPATCH
        from ..models.build_filter import BuildFilter
        from ..models.cron_job_details_patch import CronJobDetailsPATCH
        from ..models.image import Image
        from ..models.private_service_details_patch import PrivateServiceDetailsPATCH
        from ..models.static_site_details_patch import StaticSiteDetailsPATCH
        from ..models.web_service_details_patch import WebServiceDetailsPATCH

        d = dict(src_dict)
        _auto_deploy = d.pop("autoDeploy", UNSET)
        auto_deploy: Union[Unset, AutoDeploy]
        if isinstance(_auto_deploy, Unset):
            auto_deploy = UNSET
        else:
            auto_deploy = AutoDeploy(_auto_deploy)

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        repo = d.pop("repo", UNSET)

        branch = d.pop("branch", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, Image]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Image.from_dict(_image)

        name = d.pop("name", UNSET)

        _build_filter = d.pop("buildFilter", UNSET)
        build_filter: Union[Unset, BuildFilter]
        if isinstance(_build_filter, Unset):
            build_filter = UNSET
        else:
            build_filter = BuildFilter.from_dict(_build_filter)

        root_dir = d.pop("rootDir", UNSET)

        def _parse_service_details(
            data: object,
        ) -> Union[
            "BackgroundWorkerDetailsPATCH",
            "CronJobDetailsPATCH",
            "PrivateServiceDetailsPATCH",
            "StaticSiteDetailsPATCH",
            "WebServiceDetailsPATCH",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_0 = StaticSiteDetailsPATCH.from_dict(data)

                return service_details_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_1 = WebServiceDetailsPATCH.from_dict(data)

                return service_details_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_2 = PrivateServiceDetailsPATCH.from_dict(data)

                return service_details_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_3 = BackgroundWorkerDetailsPATCH.from_dict(data)

                return service_details_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            service_details_type_4 = CronJobDetailsPATCH.from_dict(data)

            return service_details_type_4

        service_details = _parse_service_details(d.pop("serviceDetails", UNSET))

        service_patch = cls(
            auto_deploy=auto_deploy,
            auto_deploy_trigger=auto_deploy_trigger,
            repo=repo,
            branch=branch,
            image=image,
            name=name,
            build_filter=build_filter,
            root_dir=root_dir,
            service_details=service_details,
        )

        service_patch.additional_properties = d
        return service_patch

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
