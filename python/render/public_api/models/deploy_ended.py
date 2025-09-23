from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus

if TYPE_CHECKING:
    from ..models.build_deploy_end_reason import BuildDeployEndReason


T = TypeVar("T", bound="DeployEnded")


@_attrs_define
class DeployEnded:
    """
    Attributes:
        deploy_id (str):
        reason (BuildDeployEndReason):
        deploy_status (EventStatus):
        status (int):
    """

    deploy_id: str
    reason: "BuildDeployEndReason"
    deploy_status: EventStatus
    status: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deploy_id = self.deploy_id

        reason = self.reason.to_dict()

        deploy_status = self.deploy_status.value

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deployId": deploy_id,
                "reason": reason,
                "deployStatus": deploy_status,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_deploy_end_reason import BuildDeployEndReason

        d = dict(src_dict)
        deploy_id = d.pop("deployId")

        reason = BuildDeployEndReason.from_dict(d.pop("reason"))

        deploy_status = EventStatus(d.pop("deployStatus"))

        status = d.pop("status")

        deploy_ended = cls(
            deploy_id=deploy_id,
            reason=reason,
            deploy_status=deploy_status,
            status=status,
        )

        deploy_ended.additional_properties = d
        return deploy_ended

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
