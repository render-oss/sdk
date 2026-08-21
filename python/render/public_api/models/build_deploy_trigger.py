from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="BuildDeployTrigger")


@_attrs_define
class BuildDeployTrigger:
    """
    Attributes:
        first_build (bool): Deploy was triggered by service creation
        env_updated (bool): Deploy was triggered by an environment update
        manual (bool): Deploy was triggered manually from the dashboard
        deployed_by_render (bool): Deploy was triggered by Render
        clear_cache (bool): Whether the cache was cleared for the deploy
        rollback (bool): Whether the deploy was triggered by a rollback
        user (Union[Unset, SchemasUser]): User who triggered the action
        updated_property (Union[Unset, str]): Updated property that triggered the deploy
        new_commit (Union[Unset, str]): Commit that triggered the deploy
        rollback_target_deploy_id (Union[Unset, str]): Deploy ID that was rolled back to
    """

    first_build: bool
    env_updated: bool
    manual: bool
    deployed_by_render: bool
    clear_cache: bool
    rollback: bool
    user: Union[Unset, "SchemasUser"] = UNSET
    updated_property: Union[Unset, str] = UNSET
    new_commit: Union[Unset, str] = UNSET
    rollback_target_deploy_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        first_build = self.first_build

        env_updated = self.env_updated

        manual = self.manual

        deployed_by_render = self.deployed_by_render

        clear_cache = self.clear_cache

        rollback = self.rollback

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        updated_property = self.updated_property

        new_commit = self.new_commit

        rollback_target_deploy_id = self.rollback_target_deploy_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "firstBuild": first_build,
                "envUpdated": env_updated,
                "manual": manual,
                "deployedByRender": deployed_by_render,
                "clearCache": clear_cache,
                "rollback": rollback,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user
        if updated_property is not UNSET:
            field_dict["updatedProperty"] = updated_property
        if new_commit is not UNSET:
            field_dict["newCommit"] = new_commit
        if rollback_target_deploy_id is not UNSET:
            field_dict["rollbackTargetDeployId"] = rollback_target_deploy_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_user import SchemasUser

        d = dict(src_dict)
        first_build = d.pop("firstBuild")

        env_updated = d.pop("envUpdated")

        manual = d.pop("manual")

        deployed_by_render = d.pop("deployedByRender")

        clear_cache = d.pop("clearCache")

        rollback = d.pop("rollback")

        _user = d.pop("user", UNSET)
        user: Union[Unset, SchemasUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = SchemasUser.from_dict(_user)

        updated_property = d.pop("updatedProperty", UNSET)

        new_commit = d.pop("newCommit", UNSET)

        rollback_target_deploy_id = d.pop("rollbackTargetDeployId", UNSET)

        build_deploy_trigger = cls(
            first_build=first_build,
            env_updated=env_updated,
            manual=manual,
            deployed_by_render=deployed_by_render,
            clear_cache=clear_cache,
            rollback=rollback,
            user=user,
            updated_property=updated_property,
            new_commit=new_commit,
            rollback_target_deploy_id=rollback_target_deploy_id,
        )

        build_deploy_trigger.additional_properties = d
        return build_deploy_trigger

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
