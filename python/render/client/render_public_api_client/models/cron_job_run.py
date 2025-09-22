import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.cron_job_run_status import CronJobRunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CronJobRun")


@_attrs_define
class CronJobRun:
    """A run of a cron job

    Attributes:
        id (str): The ID of the run
        status (CronJobRunStatus):
        started_at (Union[Unset, datetime.datetime]):  Example: 2021-07-15T07:20:05.777035-07:00.
        finished_at (Union[Unset, datetime.datetime]):  Example: 2021-07-15T07:20:05.777035-07:00.
        triggered_by (Union[Unset, str]): user who triggered the cron job run
        canceled_by (Union[Unset, str]): user who cancelled the cron job run
    """

    id: str
    status: CronJobRunStatus
    started_at: Union[Unset, datetime.datetime] = UNSET
    finished_at: Union[Unset, datetime.datetime] = UNSET
    triggered_by: Union[Unset, str] = UNSET
    canceled_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        triggered_by = self.triggered_by

        canceled_by = self.canceled_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
            }
        )
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if triggered_by is not UNSET:
            field_dict["triggeredBy"] = triggered_by
        if canceled_by is not UNSET:
            field_dict["canceledBy"] = canceled_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = CronJobRunStatus(d.pop("status"))

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

        triggered_by = d.pop("triggeredBy", UNSET)

        canceled_by = d.pop("canceledBy", UNSET)

        cron_job_run = cls(
            id=id,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            triggered_by=triggered_by,
            canceled_by=canceled_by,
        )

        cron_job_run.additional_properties = d
        return cron_job_run

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
