from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus

if TYPE_CHECKING:
    from ..models.build_deploy_end_reason import BuildDeployEndReason


T = TypeVar("T", bound="PreDeployEnded")


@_attrs_define
class PreDeployEnded:
    """
    Attributes:
        deploy_command_execution_id (str):
        deploy_id (str):
        pre_deploy_status (EventStatus):
        reason (BuildDeployEndReason):
        status (int):
    """

    deploy_command_execution_id: str
    deploy_id: str
    pre_deploy_status: EventStatus
    reason: "BuildDeployEndReason"
    status: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deploy_command_execution_id = self.deploy_command_execution_id

        deploy_id = self.deploy_id

        pre_deploy_status = self.pre_deploy_status.value

        reason = self.reason.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deployCommandExecutionId": deploy_command_execution_id,
                "deployId": deploy_id,
                "preDeployStatus": pre_deploy_status,
                "reason": reason,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_deploy_end_reason import BuildDeployEndReason

        d = dict(src_dict)
        deploy_command_execution_id = d.pop("deployCommandExecutionId")

        deploy_id = d.pop("deployId")

        pre_deploy_status = EventStatus(d.pop("preDeployStatus"))

        reason = BuildDeployEndReason.from_dict(d.pop("reason"))

        status = d.pop("status")

        pre_deploy_ended = cls(
            deploy_command_execution_id=deploy_command_execution_id,
            deploy_id=deploy_id,
            pre_deploy_status=pre_deploy_status,
            reason=reason,
            status=status,
        )

        pre_deploy_ended.additional_properties = d
        return pre_deploy_ended

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
