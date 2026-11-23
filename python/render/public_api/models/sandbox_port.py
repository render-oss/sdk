from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.sandbox_port_protocol import SandboxPortProtocol

T = TypeVar("T", bound="SandboxPort")


@_attrs_define
class SandboxPort:
    """A single port exposed through public HTTP/WebSocket ingress.

    Attributes:
        protocol (SandboxPortProtocol): The transport protocol. Only TCP is supported.
        port (int):
    """

    protocol: SandboxPortProtocol
    port: int

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol.value

        port = self.port

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocol": protocol,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocol = SandboxPortProtocol(d.pop("protocol"))

        port = d.pop("port")

        sandbox_port = cls(
            protocol=protocol,
            port=port,
        )

        return sandbox_port
