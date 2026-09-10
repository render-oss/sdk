import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.auto_deploy import AutoDeploy
from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..models.notify_setting import NotifySetting
from ..models.service_service_suspended_state import ServiceServiceSuspendedState
from ..models.service_type import ServiceType
from ..models.suspender_type import SuspenderType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.background_worker_details import BackgroundWorkerDetails
    from ..models.build_filter import BuildFilter
    from ..models.cron_job_details import CronJobDetails
    from ..models.private_service_details import PrivateServiceDetails
    from ..models.registry_credential_summary import RegistryCredentialSummary
    from ..models.static_site_details import StaticSiteDetails
    from ..models.web_service_details import WebServiceDetails


T = TypeVar("T", bound="Service")


@_attrs_define
class Service:
    """
    Attributes:
        id (str):
        auto_deploy (AutoDeploy):
        created_at (datetime.datetime):
        dashboard_url (str): The URL to view the service in the Render Dashboard
        name (str):
        notify_on_fail (NotifySetting):
        owner_id (str):
        root_dir (str):
        slug (str):
        suspended (ServiceServiceSuspendedState):
        suspenders (list[SuspenderType]):
        type_ (ServiceType):
        updated_at (datetime.datetime):
        service_details (Union['BackgroundWorkerDetails', 'CronJobDetails', 'PrivateServiceDetails',
            'StaticSiteDetails', 'WebServiceDetails']):
        build_source_id (Union[Unset, str]):
        auto_deploy_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. commit deploys when a
            commit is pushed to a branch. checksPass waits for the branch to be green.
        branch (Union[Unset, str]):
        build_filter (Union[Unset, BuildFilter]):
        environment_id (Union[Unset, str]):
        image_path (Union[Unset, str]):
        registry_credential (Union[Unset, RegistryCredentialSummary]):
        repo (Union[Unset, str]):  Example: https://github.com/render-examples/flask-hello-world.
    """

    id: str
    auto_deploy: AutoDeploy
    created_at: datetime.datetime
    dashboard_url: str
    name: str
    notify_on_fail: NotifySetting
    owner_id: str
    root_dir: str
    slug: str
    suspended: ServiceServiceSuspendedState
    suspenders: list[SuspenderType]
    type_: ServiceType
    updated_at: datetime.datetime
    service_details: Union[
        "BackgroundWorkerDetails", "CronJobDetails", "PrivateServiceDetails", "StaticSiteDetails", "WebServiceDetails"
    ]
    build_source_id: Union[Unset, str] = UNSET
    auto_deploy_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    branch: Union[Unset, str] = UNSET
    build_filter: Union[Unset, "BuildFilter"] = UNSET
    environment_id: Union[Unset, str] = UNSET
    image_path: Union[Unset, str] = UNSET
    registry_credential: Union[Unset, "RegistryCredentialSummary"] = UNSET
    repo: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.background_worker_details import BackgroundWorkerDetails
        from ..models.private_service_details import PrivateServiceDetails
        from ..models.static_site_details import StaticSiteDetails
        from ..models.web_service_details import WebServiceDetails

        id = self.id

        auto_deploy = self.auto_deploy.value

        created_at = self.created_at.isoformat()

        dashboard_url = self.dashboard_url

        name = self.name

        notify_on_fail = self.notify_on_fail.value

        owner_id = self.owner_id

        root_dir = self.root_dir

        slug = self.slug

        suspended = self.suspended.value

        suspenders = []
        for suspenders_item_data in self.suspenders:
            suspenders_item = suspenders_item_data.value
            suspenders.append(suspenders_item)

        type_ = self.type_.value

        updated_at = self.updated_at.isoformat()

        service_details: dict[str, Any]
        if isinstance(self.service_details, StaticSiteDetails):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, WebServiceDetails):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, PrivateServiceDetails):
            service_details = self.service_details.to_dict()
        elif isinstance(self.service_details, BackgroundWorkerDetails):
            service_details = self.service_details.to_dict()
        else:
            service_details = self.service_details.to_dict()

        build_source_id = self.build_source_id

        auto_deploy_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        branch = self.branch

        build_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        environment_id = self.environment_id

        image_path = self.image_path

        registry_credential: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.registry_credential, Unset):
            registry_credential = self.registry_credential.to_dict()

        repo = self.repo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "autoDeploy": auto_deploy,
                "createdAt": created_at,
                "dashboardUrl": dashboard_url,
                "name": name,
                "notifyOnFail": notify_on_fail,
                "ownerId": owner_id,
                "rootDir": root_dir,
                "slug": slug,
                "suspended": suspended,
                "suspenders": suspenders,
                "type": type_,
                "updatedAt": updated_at,
                "serviceDetails": service_details,
            }
        )
        if build_source_id is not UNSET:
            field_dict["buildSourceId"] = build_source_id
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger
        if branch is not UNSET:
            field_dict["branch"] = branch
        if build_filter is not UNSET:
            field_dict["buildFilter"] = build_filter
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if image_path is not UNSET:
            field_dict["imagePath"] = image_path
        if registry_credential is not UNSET:
            field_dict["registryCredential"] = registry_credential
        if repo is not UNSET:
            field_dict["repo"] = repo

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.background_worker_details import BackgroundWorkerDetails
        from ..models.build_filter import BuildFilter
        from ..models.cron_job_details import CronJobDetails
        from ..models.private_service_details import PrivateServiceDetails
        from ..models.registry_credential_summary import RegistryCredentialSummary
        from ..models.static_site_details import StaticSiteDetails
        from ..models.web_service_details import WebServiceDetails

        d = dict(src_dict)
        id = d.pop("id")

        auto_deploy = AutoDeploy(d.pop("autoDeploy"))

        created_at = isoparse(d.pop("createdAt"))

        dashboard_url = d.pop("dashboardUrl")

        name = d.pop("name")

        notify_on_fail = NotifySetting(d.pop("notifyOnFail"))

        owner_id = d.pop("ownerId")

        root_dir = d.pop("rootDir")

        slug = d.pop("slug")

        suspended = ServiceServiceSuspendedState(d.pop("suspended"))

        suspenders = []
        _suspenders = d.pop("suspenders")
        for suspenders_item_data in _suspenders:
            suspenders_item = SuspenderType(suspenders_item_data)

            suspenders.append(suspenders_item)

        type_ = ServiceType(d.pop("type"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_service_details(
            data: object,
        ) -> Union[
            "BackgroundWorkerDetails",
            "CronJobDetails",
            "PrivateServiceDetails",
            "StaticSiteDetails",
            "WebServiceDetails",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_0 = StaticSiteDetails.from_dict(data)

                return service_details_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_1 = WebServiceDetails.from_dict(data)

                return service_details_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_2 = PrivateServiceDetails.from_dict(data)

                return service_details_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_details_type_3 = BackgroundWorkerDetails.from_dict(data)

                return service_details_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            service_details_type_4 = CronJobDetails.from_dict(data)

            return service_details_type_4

        service_details = _parse_service_details(d.pop("serviceDetails"))

        build_source_id = d.pop("buildSourceId", UNSET)

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        branch = d.pop("branch", UNSET)

        _build_filter = d.pop("buildFilter", UNSET)
        build_filter: Union[Unset, BuildFilter]
        if isinstance(_build_filter, Unset):
            build_filter = UNSET
        else:
            build_filter = BuildFilter.from_dict(_build_filter)

        environment_id = d.pop("environmentId", UNSET)

        image_path = d.pop("imagePath", UNSET)

        _registry_credential = d.pop("registryCredential", UNSET)
        registry_credential: Union[Unset, RegistryCredentialSummary]
        if isinstance(_registry_credential, Unset):
            registry_credential = UNSET
        else:
            registry_credential = RegistryCredentialSummary.from_dict(_registry_credential)

        repo = d.pop("repo", UNSET)

        service = cls(
            id=id,
            auto_deploy=auto_deploy,
            created_at=created_at,
            dashboard_url=dashboard_url,
            name=name,
            notify_on_fail=notify_on_fail,
            owner_id=owner_id,
            root_dir=root_dir,
            slug=slug,
            suspended=suspended,
            suspenders=suspenders,
            type_=type_,
            updated_at=updated_at,
            service_details=service_details,
            build_source_id=build_source_id,
            auto_deploy_trigger=auto_deploy_trigger,
            branch=branch,
            build_filter=build_filter,
            environment_id=environment_id,
            image_path=image_path,
            registry_credential=registry_credential,
            repo=repo,
        )

        service.additional_properties = d
        return service

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
