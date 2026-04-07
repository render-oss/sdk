from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_network_policy_rule_action import SandboxNetworkPolicyRuleAction

T = TypeVar("T", bound="SandboxNetworkPolicyRule")


@_attrs_define
class SandboxNetworkPolicyRule:
    """
    Attributes:
        cidr (str): CIDR block to match outbound traffic against. Example: 198.51.100.0/24.
        action (SandboxNetworkPolicyRuleAction):
    """

    cidr: str
    action: SandboxNetworkPolicyRuleAction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cidr = self.cidr

        action = self.action.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cidr": cidr,
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cidr = d.pop("cidr")

        action = SandboxNetworkPolicyRuleAction(d.pop("action"))

        sandbox_network_policy_rule = cls(
            cidr=cidr,
            action=action,
        )

        sandbox_network_policy_rule.additional_properties = d
        return sandbox_network_policy_rule

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
