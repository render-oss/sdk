from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SandboxExecStreamExitEvent")


@_attrs_define
class SandboxExecStreamExitEvent:
    """Payload for terminal `event: exit` in a sandbox exec SSE stream. Non-zero process exit codes are reported here
    rather than as HTTP errors.

        Attributes:
            exit_code (int): Process exit code.
    """

    exit_code: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exit_code = self.exit_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exit_code": exit_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exit_code = d.pop("exit_code")

        sandbox_exec_stream_exit_event = cls(
            exit_code=exit_code,
        )

        sandbox_exec_stream_exit_event.additional_properties = d
        return sandbox_exec_stream_exit_event

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
