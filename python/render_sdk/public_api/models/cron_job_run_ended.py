from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cron_job_run_status import CronJobRunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.failure_reason import FailureReason
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="CronJobRunEnded")


@_attrs_define
class CronJobRunEnded:
    """
    Attributes:
        cron_job_run_id (str):
        status (CronJobRunStatus):
        reason (Union[Unset, FailureReason]):
        user (Union[Unset, SchemasUser]): User who triggered the action
    """

    cron_job_run_id: str
    status: CronJobRunStatus
    reason: Union[Unset, "FailureReason"] = UNSET
    user: Union[Unset, "SchemasUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cron_job_run_id = self.cron_job_run_id

        status = self.status.value

        reason: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.to_dict()

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cronJobRunId": cron_job_run_id,
                "status": status,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.failure_reason import FailureReason
        from ..models.schemas_user import SchemasUser

        d = dict(src_dict)
        cron_job_run_id = d.pop("cronJobRunId")

        status = CronJobRunStatus(d.pop("status"))

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, FailureReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = FailureReason.from_dict(_reason)

        _user = d.pop("user", UNSET)
        user: Union[Unset, SchemasUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = SchemasUser.from_dict(_user)

        cron_job_run_ended = cls(
            cron_job_run_id=cron_job_run_id,
            status=status,
            reason=reason,
            user=user,
        )

        cron_job_run_ended.additional_properties = d
        return cron_job_run_ended

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
