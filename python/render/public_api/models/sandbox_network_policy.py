from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_network_policy_type import SandboxNetworkPolicyType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_egress_rule import SandboxEgressRule


T = TypeVar("T", bound="SandboxNetworkPolicy")


@_attrs_define
class SandboxNetworkPolicy:
    """The policy that controls outbound traffic from the sandbox.

    Attributes:
        type_ (SandboxNetworkPolicyType): How Render handles outbound traffic from the sandbox. The `allow-list` policy
            requires `rules`.
        default (SandboxNetworkPolicyType | Unset): How Render handles outbound traffic from the sandbox. The `allow-
            list` policy requires `rules`.
        rules (list[SandboxEgressRule] | Unset): Destinations the sandbox may reach, present when `type` is `allow-list`
            and absent otherwise. Each domain may be listed once.
    """

    type_: SandboxNetworkPolicyType
    default: SandboxNetworkPolicyType | Unset = UNSET
    rules: list[SandboxEgressRule] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        default: str | Unset = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.value

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if default is not UNSET:
            field_dict["default"] = default
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_egress_rule import SandboxEgressRule  # noqa: PLC0415

        d = dict(src_dict)
        type_ = SandboxNetworkPolicyType(d.pop("type"))

        _default = d.pop("default", UNSET)
        default: SandboxNetworkPolicyType | Unset
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = SandboxNetworkPolicyType(_default)

        _rules = d.pop("rules", UNSET)
        rules: list[SandboxEgressRule] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = SandboxEgressRule.from_dict(rules_item_data)

                rules.append(rules_item)

        sandbox_network_policy = cls(
            type_=type_,
            default=default,
            rules=rules,
        )

        sandbox_network_policy.additional_properties = d
        return sandbox_network_policy

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
