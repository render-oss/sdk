import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.flow_run_step_status import FlowRunStepStatus
from ..models.flow_run_step_type import FlowRunStepType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_run_step_attempt import FlowRunStepAttempt


T = TypeVar("T", bound="FlowRunStepDetails")


@_attrs_define
class FlowRunStepDetails:
    """
    Attributes:
        seq (int): The step's position in the flow run. Steps are numbered densely in the order the flow started them.
        step_key (str): The SDK's key for the step.
        type_ (FlowRunStepType): The kind of step. `inline` runs a function inside the flow's process and retries in
            place. `detached` runs a registered task as its own task run. `sleep` is a durable sleep.
        status (FlowRunStepStatus): `running` until the step records an outcome, then `succeeded` or `failed`.
        started_at (datetime.datetime):
        flow_run_attempt (int): The 0-indexed flow run attempt that completed the step, 0 until then. A hint to how many
            flow run attempts the step took.
        attempts (list['FlowRunStepAttempt']): Failed attempts of an inline step, in attempt order. Empty for other step
            types.
        name (Union[Unset, str]): For inline steps, the function's name. For detached steps, the task's registered name.
            Omitted for sleep steps.
        completed_at (Union[Unset, datetime.datetime]):
        wake_at (Union[Unset, datetime.datetime]): For sleep steps, when the sleep ends.
        child_task_run_id (Union[Unset, str]): For detached steps, the ID of the task run the step started. Example:
            trn-d0hp8fs9c44c73a6f1qg.
        input_ (Union[Unset, Any]): The step's input. For detached steps, the input of the child task run.
        result (Union[Unset, Any]): The step's result. Present only when the step succeeded; null when the step returned
            no value.
        error (Union[Unset, str]): Error message if the step failed.
    """

    seq: int
    step_key: str
    type_: FlowRunStepType
    status: FlowRunStepStatus
    started_at: datetime.datetime
    flow_run_attempt: int
    attempts: list["FlowRunStepAttempt"]
    name: Union[Unset, str] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    wake_at: Union[Unset, datetime.datetime] = UNSET
    child_task_run_id: Union[Unset, str] = UNSET
    input_: Union[Unset, Any] = UNSET
    result: Union[Unset, Any] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seq = self.seq

        step_key = self.step_key

        type_ = self.type_.value

        status = self.status.value

        started_at = self.started_at.isoformat()

        flow_run_attempt = self.flow_run_attempt

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        name = self.name

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        wake_at: Union[Unset, str] = UNSET
        if not isinstance(self.wake_at, Unset):
            wake_at = self.wake_at.isoformat()

        child_task_run_id = self.child_task_run_id

        input_ = self.input_

        result = self.result

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seq": seq,
                "stepKey": step_key,
                "type": type_,
                "status": status,
                "startedAt": started_at,
                "flowRunAttempt": flow_run_attempt,
                "attempts": attempts,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if wake_at is not UNSET:
            field_dict["wakeAt"] = wake_at
        if child_task_run_id is not UNSET:
            field_dict["childTaskRunId"] = child_task_run_id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if result is not UNSET:
            field_dict["result"] = result
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_run_step_attempt import FlowRunStepAttempt

        d = dict(src_dict)
        seq = d.pop("seq")

        step_key = d.pop("stepKey")

        type_ = FlowRunStepType(d.pop("type"))

        status = FlowRunStepStatus(d.pop("status"))

        started_at = isoparse(d.pop("startedAt"))

        flow_run_attempt = d.pop("flowRunAttempt")

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = FlowRunStepAttempt.from_dict(attempts_item_data)

            attempts.append(attempts_item)

        name = d.pop("name", UNSET)

        _completed_at = d.pop("completedAt", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        _wake_at = d.pop("wakeAt", UNSET)
        wake_at: Union[Unset, datetime.datetime]
        if isinstance(_wake_at, Unset):
            wake_at = UNSET
        else:
            wake_at = isoparse(_wake_at)

        child_task_run_id = d.pop("childTaskRunId", UNSET)

        input_ = d.pop("input", UNSET)

        result = d.pop("result", UNSET)

        error = d.pop("error", UNSET)

        flow_run_step_details = cls(
            seq=seq,
            step_key=step_key,
            type_=type_,
            status=status,
            started_at=started_at,
            flow_run_attempt=flow_run_attempt,
            attempts=attempts,
            name=name,
            completed_at=completed_at,
            wake_at=wake_at,
            child_task_run_id=child_task_run_id,
            input_=input_,
            result=result,
            error=error,
        )

        flow_run_step_details.additional_properties = d
        return flow_run_step_details

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
