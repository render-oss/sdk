import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_run_status import TaskRunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskAttemptDetails")


@_attrs_define
class TaskAttemptDetails:
    """
    Attributes:
        attempt (int): The 0-indexed attempt number.
        status (TaskRunStatus):
        started_at (datetime.datetime):
        task_run_id (Union[Unset, str]): The ID of the task run this attempt belongs to.
        enqueued_at (Union[Unset, datetime.datetime]):
        completed_at (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]): Error message if the task attempt failed.
        results (Union[Unset, list[Any]]):
    """

    attempt: int
    status: TaskRunStatus
    started_at: datetime.datetime
    task_run_id: Union[Unset, str] = UNSET
    enqueued_at: Union[Unset, datetime.datetime] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    results: Union[Unset, list[Any]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        status = self.status.value

        started_at = self.started_at.isoformat()

        task_run_id = self.task_run_id

        enqueued_at: Union[Unset, str] = UNSET
        if not isinstance(self.enqueued_at, Unset):
            enqueued_at = self.enqueued_at.isoformat()

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error = self.error

        results: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.results, Unset):
            results = self.results

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempt": attempt,
                "status": status,
                "startedAt": started_at,
            }
        )
        if task_run_id is not UNSET:
            field_dict["taskRunId"] = task_run_id
        if enqueued_at is not UNSET:
            field_dict["enqueuedAt"] = enqueued_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if error is not UNSET:
            field_dict["error"] = error
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt = d.pop("attempt")

        status = TaskRunStatus(d.pop("status"))

        started_at = isoparse(d.pop("startedAt"))

        task_run_id = d.pop("taskRunId", UNSET)

        _enqueued_at = d.pop("enqueuedAt", UNSET)
        enqueued_at: Union[Unset, datetime.datetime]
        if isinstance(_enqueued_at, Unset):
            enqueued_at = UNSET
        else:
            enqueued_at = isoparse(_enqueued_at)

        _completed_at = d.pop("completedAt", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        error = d.pop("error", UNSET)

        results = cast(list[Any], d.pop("results", UNSET))

        task_attempt_details = cls(
            attempt=attempt,
            status=status,
            started_at=started_at,
            task_run_id=task_run_id,
            enqueued_at=enqueued_at,
            completed_at=completed_at,
            error=error,
            results=results,
        )

        task_attempt_details.additional_properties = d
        return task_attempt_details

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
