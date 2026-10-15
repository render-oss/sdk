import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="FlowRunStepAttempt")


@_attrs_define
class FlowRunStepAttempt:
    """
    Attributes:
        attempt (int): The step's attempt number. It continues across flow run attempts.
        flow_run_attempt (int): The 0-indexed flow run attempt this step attempt ran in.
        started_at (datetime.datetime):
        completed_at (datetime.datetime):
        error (str): Error message of the failed attempt.
    """

    attempt: int
    flow_run_attempt: int
    started_at: datetime.datetime
    completed_at: datetime.datetime
    error: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        flow_run_attempt = self.flow_run_attempt

        started_at = self.started_at.isoformat()

        completed_at = self.completed_at.isoformat()

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempt": attempt,
                "flowRunAttempt": flow_run_attempt,
                "startedAt": started_at,
                "completedAt": completed_at,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt = d.pop("attempt")

        flow_run_attempt = d.pop("flowRunAttempt")

        started_at = isoparse(d.pop("startedAt"))

        completed_at = isoparse(d.pop("completedAt"))

        error = d.pop("error")

        flow_run_step_attempt = cls(
            attempt=attempt,
            flow_run_attempt=flow_run_attempt,
            started_at=started_at,
            completed_at=completed_at,
            error=error,
        )

        flow_run_step_attempt.additional_properties = d
        return flow_run_step_attempt

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
