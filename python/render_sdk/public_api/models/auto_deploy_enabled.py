from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoDeployEnabled")


@_attrs_define
class AutoDeployEnabled:
    """
    Attributes:
        new_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. commit deploys when a commit is
            pushed to a branch. checksPass waits for the branch to be green.
    """

    new_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.new_trigger, Unset):
            new_trigger = self.new_trigger.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if new_trigger is not UNSET:
            field_dict["newTrigger"] = new_trigger

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _new_trigger = d.pop("newTrigger", UNSET)
        new_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_new_trigger, Unset):
            new_trigger = UNSET
        else:
            new_trigger = AutoDeployTrigger(_new_trigger)

        auto_deploy_enabled = cls(
            new_trigger=new_trigger,
        )

        auto_deploy_enabled.additional_properties = d
        return auto_deploy_enabled

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
