from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_port_protocol import SandboxPortProtocol

T = TypeVar("T", bound="SandboxExposedPort")


@_attrs_define
class SandboxExposedPort:
    """
    Attributes:
        protocol (SandboxPortProtocol): The transport protocol. Only TCP is supported.
        port (int):
        url (str): The HTTPS URL for the exposed port.
    """

    protocol: SandboxPortProtocol
    port: int
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol.value

        port = self.port

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protocol": protocol,
                "port": port,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocol = SandboxPortProtocol(d.pop("protocol"))

        port = d.pop("port")

        url = d.pop("url")

        sandbox_exposed_port = cls(
            protocol=protocol,
            port=port,
            url=url,
        )

        sandbox_exposed_port.additional_properties = d
        return sandbox_exposed_port

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
