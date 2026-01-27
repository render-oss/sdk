from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
    """

    name: Union[Unset, str] = UNSET
    build_config: Union[Unset, "BuildConfig"] = UNSET
    run_command: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        build_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_config, Unset):
            build_config = self.build_config.to_dict()

        run_command = self.run_command

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if build_config is not UNSET:
            field_dict["buildConfig"] = build_config
        if run_command is not UNSET:
            field_dict["runCommand"] = run_command

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

        workflow_update = cls(
            name=name,
            build_config=build_config,
            run_command=run_command,
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
