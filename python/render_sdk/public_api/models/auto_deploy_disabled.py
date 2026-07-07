from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_deploy_trigger import AutoDeployTrigger
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoDeployDisabled")


@_attrs_define
class AutoDeployDisabled:
    """
    Attributes:
        reason (str): Why auto-deploy was disabled (manual_deploy, rollback, or setting_change)
        from_trigger (Union[Unset, AutoDeployTrigger]): Controls autodeploy behavior. commit deploys when a commit is
            pushed to a branch. checksPass waits for the branch to be green.
    """

    reason: str
    from_trigger: Union[Unset, AutoDeployTrigger] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        from_trigger: Union[Unset, str] = UNSET
        if not isinstance(self.from_trigger, Unset):
            from_trigger = self.from_trigger.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )
        if from_trigger is not UNSET:
            field_dict["fromTrigger"] = from_trigger

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        _from_trigger = d.pop("fromTrigger", UNSET)
        from_trigger: Union[Unset, AutoDeployTrigger]
        if isinstance(_from_trigger, Unset):
            from_trigger = UNSET
        else:
            from_trigger = AutoDeployTrigger(_from_trigger)

        auto_deploy_disabled = cls(
            reason=reason,
            from_trigger=from_trigger,
        )

        auto_deploy_disabled.additional_properties = d
        return auto_deploy_disabled

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
