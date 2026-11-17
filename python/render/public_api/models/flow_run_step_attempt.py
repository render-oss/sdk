from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowRunStepAttempt")


@_attrs_define
class FlowRunStepAttempt:
    """
    Attributes:
        attempt (int):
        flow_attempt (int):
        started_at (datetime.datetime):
        completed_at (datetime.datetime):
        retry_at (datetime.datetime | Unset):
    """

    attempt: int
    flow_attempt: int
    started_at: datetime.datetime
    completed_at: datetime.datetime
    retry_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        flow_attempt = self.flow_attempt

        started_at = self.started_at.isoformat()

        completed_at = self.completed_at.isoformat()

        retry_at: str | Unset = UNSET
        if not isinstance(self.retry_at, Unset):
            retry_at = self.retry_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempt": attempt,
                "flowAttempt": flow_attempt,
                "startedAt": started_at,
                "completedAt": completed_at,
            }
        )
        if retry_at is not UNSET:
            field_dict["retryAt"] = retry_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt = d.pop("attempt")

        flow_attempt = d.pop("flowAttempt")

        started_at = datetime.datetime.fromisoformat(d.pop("startedAt"))

        completed_at = datetime.datetime.fromisoformat(d.pop("completedAt"))

        _retry_at = d.pop("retryAt", UNSET)
        retry_at: datetime.datetime | Unset
        if isinstance(_retry_at, Unset):
            retry_at = UNSET
        else:
            retry_at = datetime.datetime.fromisoformat(_retry_at)

        flow_run_step_attempt = cls(
            attempt=attempt,
            flow_attempt=flow_attempt,
            started_at=started_at,
            completed_at=completed_at,
            retry_at=retry_at,
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
