import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxExecUpdateResponse")


@_attrs_define
class SandboxExecUpdateResponse:
    """Updated sandbox execution after a client update.

    Attributes:
        exec_id (str):
        sandbox_id (str):
        type_ (str):
        operation (str):
        started_at (datetime.datetime):
        command (Union[Unset, str]):
        stopped_at (Union[Unset, datetime.datetime]):
        exit_code (Union[Unset, int]):
    """

    exec_id: str
    sandbox_id: str
    type_: str
    operation: str
    started_at: datetime.datetime
    command: Union[Unset, str] = UNSET
    stopped_at: Union[Unset, datetime.datetime] = UNSET
    exit_code: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exec_id = self.exec_id

        sandbox_id = self.sandbox_id

        type_ = self.type_

        operation = self.operation

        started_at = self.started_at.isoformat()

        command = self.command

        stopped_at: Union[Unset, str] = UNSET
        if not isinstance(self.stopped_at, Unset):
            stopped_at = self.stopped_at.isoformat()

        exit_code = self.exit_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execId": exec_id,
                "sandboxId": sandbox_id,
                "type": type_,
                "operation": operation,
                "startedAt": started_at,
            }
        )
        if command is not UNSET:
            field_dict["command"] = command
        if stopped_at is not UNSET:
            field_dict["stoppedAt"] = stopped_at
        if exit_code is not UNSET:
            field_dict["exitCode"] = exit_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exec_id = d.pop("execId")

        sandbox_id = d.pop("sandboxId")

        type_ = d.pop("type")

        operation = d.pop("operation")

        started_at = isoparse(d.pop("startedAt"))

        command = d.pop("command", UNSET)

        _stopped_at = d.pop("stoppedAt", UNSET)
        stopped_at: Union[Unset, datetime.datetime]
        if isinstance(_stopped_at, Unset):
            stopped_at = UNSET
        else:
            stopped_at = isoparse(_stopped_at)

        exit_code = d.pop("exitCode", UNSET)

        sandbox_exec_update_response = cls(
            exec_id=exec_id,
            sandbox_id=sandbox_id,
            type_=type_,
            operation=operation,
            started_at=started_at,
            command=command,
            stopped_at=stopped_at,
            exit_code=exit_code,
        )

        sandbox_exec_update_response.additional_properties = d
        return sandbox_exec_update_response

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
