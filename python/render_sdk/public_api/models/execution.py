import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.execution_operation import ExecutionOperation
from ..models.execution_type import ExecutionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Execution")


@_attrs_define
class Execution:
    """One recorded sandbox execution (a command run or file transfer).
    `startedAt` is the token provisioning time. `command` may be present
    while the execution is in flight (recorded at token mint). `stoppedAt`
    and `exitCode` are absent until a status report or sandbox finalization.

        Attributes:
            id (str):  Example: exe-cph1rs3idesc73a2b2mg.
            sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
            type_ (ExecutionType):
            operation (ExecutionOperation):
            user_id (str): The ID of the user the execution token was minted for. Example: usr-cph1rs3idesc73a2b2mg.
            started_at (datetime.datetime):  Example: 2026-08-01T10:00:00Z.
            command (Union[Unset, str]): The execution target. For runs, the truncated command; for file transfers, the
                target file path.
            stopped_at (Union[Unset, datetime.datetime]):  Example: 2026-08-01T10:05:00Z.
            exit_code (Union[Unset, int]):
    """

    id: str
    sandbox_id: str
    type_: ExecutionType
    operation: ExecutionOperation
    user_id: str
    started_at: datetime.datetime
    command: Union[Unset, str] = UNSET
    stopped_at: Union[Unset, datetime.datetime] = UNSET
    exit_code: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sandbox_id = self.sandbox_id

        type_ = self.type_.value

        operation = self.operation.value

        user_id = self.user_id

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
                "id": id,
                "sandboxId": sandbox_id,
                "type": type_,
                "operation": operation,
                "userId": user_id,
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
        id = d.pop("id")

        sandbox_id = d.pop("sandboxId")

        type_ = ExecutionType(d.pop("type"))

        operation = ExecutionOperation(d.pop("operation"))

        user_id = d.pop("userId")

        started_at = isoparse(d.pop("startedAt"))

        command = d.pop("command", UNSET)

        _stopped_at = d.pop("stoppedAt", UNSET)
        stopped_at: Union[Unset, datetime.datetime]
        if isinstance(_stopped_at, Unset):
            stopped_at = UNSET
        else:
            stopped_at = isoparse(_stopped_at)

        exit_code = d.pop("exitCode", UNSET)

        execution = cls(
            id=id,
            sandbox_id=sandbox_id,
            type_=type_,
            operation=operation,
            user_id=user_id,
            started_at=started_at,
            command=command,
            stopped_at=stopped_at,
            exit_code=exit_code,
        )

        execution.additional_properties = d
        return execution

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
