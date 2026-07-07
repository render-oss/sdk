from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_exec_stream_output_event_stream import (
    SandboxExecStreamOutputEventStream,
)

T = TypeVar("T", bound="SandboxExecStreamOutputEvent")


@_attrs_define
class SandboxExecStreamOutputEvent:
    """Payload for `event: output` in a sandbox exec SSE stream.

    Attributes:
        stream (SandboxExecStreamOutputEventStream): Output stream that produced this chunk.
        data (str): Output chunk.
    """

    stream: SandboxExecStreamOutputEventStream
    data: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stream = self.stream.value

        data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stream": stream,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stream = SandboxExecStreamOutputEventStream(d.pop("stream"))

        data = d.pop("data")

        sandbox_exec_stream_output_event = cls(
            stream=stream,
            data=data,
        )

        sandbox_exec_stream_output_event.additional_properties = d
        return sandbox_exec_stream_output_event

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
