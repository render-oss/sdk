from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_network_policy_type import SandboxNetworkPolicyType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_egress_rule import SandboxEgressRule


T = TypeVar("T", bound="SandboxNetworkPolicyPOST")


@_attrs_define
class SandboxNetworkPolicyPOST:
    """Set either `type` or its deprecated alias `default`. Sending both is
    only accepted when they name the same policy.

        Attributes:
            type_ (Union[Unset, SandboxNetworkPolicyType]): How outbound traffic is handled. `allow-all`, `deny-all`, or
                `allow-list` (requires additional `rules`).
            default (Union[Unset, SandboxNetworkPolicyType]): How outbound traffic is handled. `allow-all`, `deny-all`, or
                `allow-list` (requires additional `rules`).
            rules (Union[Unset, list['SandboxEgressRule']]): Destinations the sandbox may reach, required when the policy is
                `allow-list` and rejected otherwise. Each domain may be listed once.
    """

    type_: Union[Unset, SandboxNetworkPolicyType] = UNSET
    default: Union[Unset, SandboxNetworkPolicyType] = UNSET
    rules: Union[Unset, list["SandboxEgressRule"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        default: Union[Unset, str] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.value

        rules: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if default is not UNSET:
            field_dict["default"] = default
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_egress_rule import SandboxEgressRule

        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, SandboxNetworkPolicyType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SandboxNetworkPolicyType(_type_)

        _default = d.pop("default", UNSET)
        default: Union[Unset, SandboxNetworkPolicyType]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = SandboxNetworkPolicyType(_default)

        rules = []
        _rules = d.pop("rules", UNSET)
        for rules_item_data in _rules or []:
            rules_item = SandboxEgressRule.from_dict(rules_item_data)

            rules.append(rules_item)

        sandbox_network_policy_post = cls(
            type_=type_,
            default=default,
            rules=rules,
        )

        sandbox_network_policy_post.additional_properties = d
        return sandbox_network_policy_post

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
