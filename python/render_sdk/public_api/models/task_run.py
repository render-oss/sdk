import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_run_status import TaskRunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskRun")


@_attrs_define
class TaskRun:
    """
    Attributes:
        id (str):
        task_id (str):
        status (TaskRunStatus):
        parent_task_run_id (str):
        root_task_run_id (str):
        retries (int):
        started_at (Union[Unset, datetime.datetime]):
        completed_at (Union[Unset, datetime.datetime]):
    """

    id: str
    task_id: str
    status: TaskRunStatus
    parent_task_run_id: str
    root_task_run_id: str
    retries: int
    started_at: Union[Unset, datetime.datetime] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        task_id = self.task_id

        status = self.status.value

        parent_task_run_id = self.parent_task_run_id

        root_task_run_id = self.root_task_run_id

        retries = self.retries

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "taskId": task_id,
                "status": status,
                "parentTaskRunId": parent_task_run_id,
                "rootTaskRunId": root_task_run_id,
                "retries": retries,
            }
        )
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        task_id = d.pop("taskId")

        status = TaskRunStatus(d.pop("status"))

        parent_task_run_id = d.pop("parentTaskRunId")

        root_task_run_id = d.pop("rootTaskRunId")

        retries = d.pop("retries")

        _started_at = d.pop("startedAt", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _completed_at = d.pop("completedAt", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        task_run = cls(
            id=id,
            task_id=task_id,
            status=status,
            parent_task_run_id=parent_task_run_id,
            root_task_run_id=root_task_run_id,
            retries=retries,
            started_at=started_at,
            completed_at=completed_at,
        )

        task_run.additional_properties = d
        return task_run

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
