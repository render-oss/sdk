from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_operation import ExecutionOperation
from ..models.execution_type import ExecutionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Execution")


@_attrs_define
class Execution:
    """A record of a command run or file transfer in a sandbox. `startedAt` records when the connect token was created. The
    command can appear while the execution is running. `stoppedAt` and `exitCode` are omitted until Render receives the
    result or finalizes the execution when the sandbox stops.

        Attributes:
            id (str): The ID of the sandbox execution. Example: exe-cph1rs3idesc73a2b2mg.
            sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
            type_ (ExecutionType): Whether the execution is a command run or a file transfer.
            operation (ExecutionOperation): The command run or file transfer operation authorized by the connect token.
            user_id (str): The ID of the user the execution token was created for. Example: usr-cph1rs3idesc73a2b2mg.
            started_at (datetime.datetime): The timestamp when the execution token was created, in ISO 8601 format. Example:
                2026-08-01T10:00:00Z.
            command (str | Unset): The command run in the sandbox, or the target path for a file transfer. Command text may
                be redacted or truncated. Omitted if you do not have permission to view execution commands.
            stopped_at (datetime.datetime | Unset): The timestamp when the execution stopped, in ISO 8601 format. Omitted
                until a result is available. Example: 2026-08-01T10:05:00Z.
            exit_code (int | Unset): The execution exit code. Omitted until a result is available. Example: 0.
    """

    id: str
    sandbox_id: str
    type_: ExecutionType
    operation: ExecutionOperation
    user_id: str
    started_at: datetime.datetime
    command: str | Unset = UNSET
    stopped_at: datetime.datetime | Unset = UNSET
    exit_code: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sandbox_id = self.sandbox_id

        type_ = self.type_.value

        operation = self.operation.value

        user_id = self.user_id

        started_at = self.started_at.isoformat()

        command = self.command

        stopped_at: str | Unset = UNSET
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

        started_at = datetime.datetime.fromisoformat(d.pop("startedAt"))

        command = d.pop("command", UNSET)

        _stopped_at = d.pop("stoppedAt", UNSET)
        stopped_at: datetime.datetime | Unset
        if isinstance(_stopped_at, Unset):
            stopped_at = UNSET
        else:
            stopped_at = datetime.datetime.fromisoformat(_stopped_at)

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
