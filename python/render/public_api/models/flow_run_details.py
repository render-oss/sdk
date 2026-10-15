import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.flow_run_status import FlowRunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_input_type_1 import FlowInputType1
    from ..models.flow_run_attempt import FlowRunAttempt


T = TypeVar("T", bound="FlowRunDetails")


@_attrs_define
class FlowRunDetails:
    """
    Attributes:
        id (str):  Example: frn-d0hp8fs9c44c73a6f1qg.
        flow_id (str):  Example: flw-d0hp8fs9c44c73a6f1qg.
        status (FlowRunStatus): The status of a flow run.
        input_ (Union['FlowInputType1', list[Any]]): Input data for a flow. Can be either an array (for positional
            arguments) or an object (for named parameters).
        results (list[Any]):
        attempts (list['FlowRunAttempt']): The flow run's attempts. A flow run gets a new attempt when it resumes after
            its process is interrupted; it replays completed steps instead of rerunning them.
        started_at (Union[Unset, datetime.datetime]):
        completed_at (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]): Error message if the flow run failed.
    """

    id: str
    flow_id: str
    status: FlowRunStatus
    input_: Union["FlowInputType1", list[Any]]
    results: list[Any]
    attempts: list["FlowRunAttempt"]
    started_at: Union[Unset, datetime.datetime] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        flow_id = self.flow_id

        status = self.status.value

        input_: Union[dict[str, Any], list[Any]]
        if isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_.to_dict()

        results = self.results

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "flowId": flow_id,
                "status": status,
                "input": input_,
                "results": results,
                "attempts": attempts,
            }
        )
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_input_type_1 import FlowInputType1
        from ..models.flow_run_attempt import FlowRunAttempt

        d = dict(src_dict)
        id = d.pop("id")

        flow_id = d.pop("flowId")

        status = FlowRunStatus(d.pop("status"))

        def _parse_input_(data: object) -> Union["FlowInputType1", list[Any]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_flow_input_type_0 = cast(list[Any], data)

                return componentsschemas_flow_input_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_flow_input_type_1 = FlowInputType1.from_dict(data)

            return componentsschemas_flow_input_type_1

        input_ = _parse_input_(d.pop("input"))

        results = cast(list[Any], d.pop("results"))

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = FlowRunAttempt.from_dict(attempts_item_data)

            attempts.append(attempts_item)

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

        error = d.pop("error", UNSET)

        flow_run_details = cls(
            id=id,
            flow_id=flow_id,
            status=status,
            input_=input_,
            results=results,
            attempts=attempts,
            started_at=started_at,
            completed_at=completed_at,
            error=error,
        )

        flow_run_details.additional_properties = d
        return flow_run_details

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
