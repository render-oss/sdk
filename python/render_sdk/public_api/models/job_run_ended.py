from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.failure_reason import FailureReason


T = TypeVar("T", bound="JobRunEnded")


@_attrs_define
class JobRunEnded:
    """
    Attributes:
        job_id (str):  Example: job-cph1rs3idesc73a2b2mg.
        status (JobStatus):
        reason (Union[Unset, FailureReason]):
    """

    job_id: str
    status: JobStatus
    reason: Union[Unset, "FailureReason"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        status = self.status.value

        reason: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobId": job_id,
                "status": status,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.failure_reason import FailureReason

        d = dict(src_dict)
        job_id = d.pop("jobId")

        status = JobStatus(d.pop("status"))

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, FailureReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = FailureReason.from_dict(_reason)

        job_run_ended = cls(
            job_id=job_id,
            status=status,
            reason=reason,
        )

        job_run_ended.additional_properties = d
        return job_run_ended

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
