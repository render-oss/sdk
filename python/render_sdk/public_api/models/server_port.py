from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.server_port_protocol import ServerPortProtocol

T = TypeVar("T", bound="ServerPort")


@_attrs_define
class ServerPort:
    """
    Attributes:
        port (int):  Example: 10000.
        protocol (ServerPortProtocol):
    """

    port: int
    protocol: ServerPortProtocol
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        port = self.port

        protocol = self.protocol.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "port": port,
                "protocol": protocol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        protocol = ServerPortProtocol(d.pop("protocol"))

        server_port = cls(
            port=port,
            protocol=protocol,
        )

        server_port.additional_properties = d
        return server_port

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
