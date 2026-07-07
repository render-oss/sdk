from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..models.region import Region
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_config import BuildConfig
    from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue
    from ..models.env_var_key_value import EnvVarKeyValue


T = TypeVar("T", bound="WorkflowCreate")


@_attrs_define
class WorkflowCreate:
    """
    Attributes:
        name (str):
        owner_id (str):
        build_config (BuildConfig):
        run_command (str): The command to run the workflow
        region (Region): Defaults to "oregon"
        auto_deploy_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. "commit" deploys when a
            commit is pushed to the branch. "checksPass" waits for CI checks to pass before deploying. "off" disables
            autodeploy.
        env_vars (Union[Unset, list[Union['EnvVarKeyGenerateValue', 'EnvVarKeyValue']]]):
    """

    name: str
    owner_id: str
    build_config: "BuildConfig"
    run_command: str
    region: Region
    auto_deploy_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    env_vars: Union[Unset, list[Union["EnvVarKeyGenerateValue", "EnvVarKeyValue"]]] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.env_var_key_value import EnvVarKeyValue

        name = self.name

        owner_id = self.owner_id

        build_config = self.build_config.to_dict()

        run_command = self.run_command

        region = self.region.value

        auto_deploy_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.auto_deploy_trigger, Unset):
            auto_deploy_trigger = self.auto_deploy_trigger.value

        env_vars: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = []
            for componentsschemasenv_var_input_array_item_data in self.env_vars:
                componentsschemasenv_var_input_array_item: dict[str, Any]
                if isinstance(
                    componentsschemasenv_var_input_array_item_data, EnvVarKeyValue
                ):
                    componentsschemasenv_var_input_array_item = (
                        componentsschemasenv_var_input_array_item_data.to_dict()
                    )
                else:
                    componentsschemasenv_var_input_array_item = (
                        componentsschemasenv_var_input_array_item_data.to_dict()
                    )

                env_vars.append(componentsschemasenv_var_input_array_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "buildConfig": build_config,
                "runCommand": run_command,
                "region": region,
            }
        )
        if auto_deploy_trigger is not UNSET:
            field_dict["autoDeployTrigger"] = auto_deploy_trigger
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_config import BuildConfig
        from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue
        from ..models.env_var_key_value import EnvVarKeyValue

        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        build_config = BuildConfig.from_dict(d.pop("buildConfig"))

        run_command = d.pop("runCommand")

        region = Region(d.pop("region"))

        _auto_deploy_trigger = d.pop("autoDeployTrigger", UNSET)
        auto_deploy_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_auto_deploy_trigger, Unset):
            auto_deploy_trigger = UNSET
        else:
            auto_deploy_trigger = AutoDeployTrigger(_auto_deploy_trigger)

        env_vars = []
        _env_vars = d.pop("envVars", UNSET)
        for componentsschemasenv_var_input_array_item_data in _env_vars or []:

            def _parse_componentsschemasenv_var_input_array_item(
                data: object,
            ) -> Union["EnvVarKeyGenerateValue", "EnvVarKeyValue"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasenv_var_input_type_0 = EnvVarKeyValue.from_dict(
                        data
                    )

                    return componentsschemasenv_var_input_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasenv_var_input_type_1 = (
                    EnvVarKeyGenerateValue.from_dict(data)
                )

                return componentsschemasenv_var_input_type_1

            componentsschemasenv_var_input_array_item = (
                _parse_componentsschemasenv_var_input_array_item(
                    componentsschemasenv_var_input_array_item_data
                )
            )

            env_vars.append(componentsschemasenv_var_input_array_item)

        workflow_create = cls(
            name=name,
            owner_id=owner_id,
            build_config=build_config,
            run_command=run_command,
            region=region,
            auto_deploy_trigger=auto_deploy_trigger,
            env_vars=env_vars,
        )

        workflow_create.additional_properties = d
        return workflow_create

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
