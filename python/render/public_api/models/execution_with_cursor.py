from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.execution import Execution


T = TypeVar("T", bound="ExecutionWithCursor")


@_attrs_define
class ExecutionWithCursor:
    """A sandbox execution with a cursor

    Attributes:
        execution (Execution): One recorded sandbox execution (a command run or file transfer).
            `startedAt` is the token provisioning time. `command` may be present
            while the execution is in flight (recorded at token mint). `stoppedAt`
            and `exitCode` are absent until a status report or sandbox finalization.
        cursor (str):
    """

    execution: "Execution"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution = self.execution.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execution": execution,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.execution import Execution

        d = dict(src_dict)
        execution = Execution.from_dict(d.pop("execution"))

        cursor = d.pop("cursor")

        execution_with_cursor = cls(
            execution=execution,
            cursor=cursor,
        )

        execution_with_cursor.additional_properties = d
        return execution_with_cursor

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
