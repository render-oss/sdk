from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_network_policy_default import SandboxNetworkPolicyDefault

T = TypeVar("T", bound="SandboxNetworkPolicy")


@_attrs_define
class SandboxNetworkPolicy:
    """
    Attributes:
        default (SandboxNetworkPolicyDefault): Default action for outbound traffic.
    """

    default: SandboxNetworkPolicyDefault
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default = self.default.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default": default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default = SandboxNetworkPolicyDefault(d.pop("default"))

        sandbox_network_policy = cls(
            default=default,
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
