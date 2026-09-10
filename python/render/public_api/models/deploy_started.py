from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_deploy_trigger import BuildDeployTrigger


T = TypeVar("T", bound="DeployStarted")


@_attrs_define
class DeployStarted:
    """
    Attributes:
        deploy_id (str):
        trigger (BuildDeployTrigger):
        build_id (Union[Unset, str]): Set when the deploy ships a build published by the service's linked build source.
    """

    deploy_id: str
    trigger: "BuildDeployTrigger"
    build_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deploy_id = self.deploy_id

        trigger = self.trigger.to_dict()

        build_id = self.build_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deployId": deploy_id,
                "trigger": trigger,
            }
        )
        if build_id is not UNSET:
            field_dict["buildId"] = build_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_deploy_trigger import BuildDeployTrigger

        d = dict(src_dict)
        deploy_id = d.pop("deployId")

        trigger = BuildDeployTrigger.from_dict(d.pop("trigger"))

        build_id = d.pop("buildId", UNSET)

        deploy_started = cls(
            deploy_id=deploy_id,
            trigger=trigger,
            build_id=build_id,
        )

        deploy_started.additional_properties = d
        return deploy_started

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
