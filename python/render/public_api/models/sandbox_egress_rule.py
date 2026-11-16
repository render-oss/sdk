from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_egress_rule_protocol import SandboxEgressRuleProtocol
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxEgressRule")


@_attrs_define
class SandboxEgressRule:
    """A destination that sandboxes can access when the network policy is `allow-list`.

    Attributes:
        domain (str): The hostname this rule allows, up to 253 characters. Matching is exact: `foo.local` does not match
            `api.foo.local`. Use a separate rule or `*.foo.local` for subdomains. A wildcard is allowed only as the leftmost
            label.
             Example: *.bar.local.
        protocol (SandboxEgressRuleProtocol | Unset): The protocol allowed for this destination. Defaults to `https`.
            The `allow-list` policy blocks outbound traffic that uses other protocols. Default:
            SandboxEgressRuleProtocol.HTTPS.
    """

    domain: str
    protocol: SandboxEgressRuleProtocol | Unset = SandboxEgressRuleProtocol.HTTPS
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain = self.domain

        protocol: str | Unset = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
            }
        )
        if protocol is not UNSET:
            field_dict["protocol"] = protocol

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        domain = d.pop("domain")

        _protocol = d.pop("protocol", UNSET)
        protocol: SandboxEgressRuleProtocol | Unset
        if isinstance(_protocol, Unset):
            protocol = UNSET
        else:
            protocol = SandboxEgressRuleProtocol(_protocol)

        sandbox_egress_rule = cls(
            domain=domain,
            protocol=protocol,
        )

        sandbox_egress_rule.additional_properties = d
        return sandbox_egress_rule

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
