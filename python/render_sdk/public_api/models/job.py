import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Job")


@_attrs_define
class Job:
    """
    Attributes:
        id (str):  Example: job-cph1rs3idesc73a2b2mg.
        service_id (str):  Example: srv-xxxxx.
        start_command (str):  Example: echo 'hello world'.
        plan_id (str):  Example: plan-srv-004.
        created_at (datetime.datetime):  Example: 2021-07-15T07:20:05.777035-07:00.
        status (Union[Unset, JobStatus]):
        started_at (Union[Unset, datetime.datetime]):  Example: 2021-07-15T07:20:05.777035-07:00.
        finished_at (Union[Unset, datetime.datetime]):  Example: 2021-07-15T07:20:05.777035-07:00.
    """

    id: str
    service_id: str
    start_command: str
    plan_id: str
    created_at: datetime.datetime
    status: Union[Unset, JobStatus] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    finished_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        service_id = self.service_id

        start_command = self.start_command

        plan_id = self.plan_id

        created_at = self.created_at.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "serviceId": service_id,
                "startCommand": start_command,
                "planId": plan_id,
                "createdAt": created_at,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        service_id = d.pop("serviceId")

        start_command = d.pop("startCommand")

        plan_id = d.pop("planId")

        created_at = isoparse(d.pop("createdAt"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = JobStatus(_status)

        _started_at = d.pop("startedAt", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _finished_at = d.pop("finishedAt", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        job = cls(
            id=id,
            service_id=service_id,
            start_command=start_command,
            plan_id=plan_id,
            created_at=created_at,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
        )

        job.additional_properties = d
        return job

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
