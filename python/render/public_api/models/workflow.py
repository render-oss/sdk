import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..models.region import Region
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_config import BuildConfig


T = TypeVar("T", bound="Workflow")


@_attrs_define
class Workflow:
    """
    Attributes:
        id (str):
        name (str):
        owner_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        build_config (BuildConfig):
        run_command (str): Command to run the workflow.
        region (Region): Defaults to "oregon"
        environment_id (Union[Unset, str]):
        slug (Union[Unset, str]):
        auto_deploy_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. "commit" deploys when a
            commit is pushed to the branch. "checksPass" waits for CI checks to pass before deploying. "off" disables
            autodeploy.
        default_version_id (Union[Unset, str]): ID of the workflow version that new task runs use by default. Omitted
            until a version has been registered.
    """

    id: str
    name: str
    owner_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    build_config: "BuildConfig"
    run_command: str
    region: Region
    environment_id: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    auto_deploy_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    default_version_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        owner_id = self.owner_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        build_config = self.build_config.to_dict()

        run_command = self.run_command

        region = self.region.value

        environment_id = self.environment_id

        slug = self.slug

        auto_deploy_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        default_version_id = self.default_version_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ownerId": owner_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "buildConfig": build_config,
                "runCommand": run_command,
                "region": region,
            }
        )
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if slug is not UNSET:
            field_dict["slug"] = slug
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger
        if default_version_id is not UNSET:
            field_dict["defaultVersionId"] = default_version_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_config import BuildConfig

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        build_config = BuildConfig.from_dict(d.pop("buildConfig"))

        run_command = d.pop("runCommand")

        region = Region(d.pop("region"))

        environment_id = d.pop("environmentId", UNSET)

        slug = d.pop("slug", UNSET)

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        default_version_id = d.pop("defaultVersionId", UNSET)

        workflow = cls(
            id=id,
            name=name,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            build_config=build_config,
            run_command=run_command,
            region=region,
            environment_id=environment_id,
            slug=slug,
            auto_deploy_trigger=auto_deploy_trigger,
            default_version_id=default_version_id,
        )

        workflow.additional_properties = d
        return workflow

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
