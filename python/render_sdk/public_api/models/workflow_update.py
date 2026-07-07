from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_config import BuildConfig


T = TypeVar("T", bound="WorkflowUpdate")


@_attrs_define
class WorkflowUpdate:
    """
    Attributes:
        name (Union[Unset, str]):
        build_config (Union[Unset, BuildConfig]):
        run_command (Union[Unset, str]): The command to run the workflow
        auto_deploy_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. "commit" deploys when a
            commit is pushed to the branch. "checksPass" waits for CI checks to pass before deploying. "off" disables
            autodeploy.
    """

    name: Union[Unset, str] = UNSET
    build_config: Union[Unset, "BuildConfig"] = UNSET
    run_command: Union[Unset, str] = UNSET
    auto_deploy_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        build_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_config, Unset):
            build_config = self.build_config.to_dict()

        run_command = self.run_command

        auto_deploy_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if build_config is not UNSET:
            field_dict["buildConfig"] = build_config
        if run_command is not UNSET:
            field_dict["runCommand"] = run_command
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_config import BuildConfig

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _build_config = d.pop("buildConfig", UNSET)
        build_config: Union[Unset, BuildConfig]
        if isinstance(_build_config, Unset):
            build_config = UNSET
        else:
            build_config = BuildConfig.from_dict(_build_config)

        run_command = d.pop("runCommand", UNSET)

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        workflow_update = cls(
            name=name,
            build_config=build_config,
            run_command=run_command,
            auto_deploy_trigger=auto_deploy_trigger,
        )

        workflow_update.additional_properties = d
        return workflow_update

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
