from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_network_policy_default import SandboxNetworkPolicyDefault
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxNetworkPolicy")


@_attrs_define
class SandboxNetworkPolicy:
    """
    Attributes:
        default (SandboxNetworkPolicyDefault): Default action for outbound traffic.
        allowed_domains (Union[Unset, list[str]]): Domains the sandbox may reach, required when `default` is
            `allow-list` and rejected otherwise.

            Matching is exact: `foo.local` does not cover `api.foo.local`,
            leftmost-only wildcarding e.g. `*.foo.local` is allowed. Only HTTP
            and HTTPS traffic is matched against this list; under
            `allow-list` all other outbound TCP is dropped.
             Example: ['foo.local', '*.bar.local'].
    """

    default: SandboxNetworkPolicyDefault
    allowed_domains: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default = self.default.value

        allowed_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_domains, Unset):
            allowed_domains = self.allowed_domains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default": default,
            }
        )
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default = SandboxNetworkPolicyDefault(d.pop("default"))

        allowed_domains = cast(list[str], d.pop("allowedDomains", UNSET))

        sandbox_network_policy = cls(
            default=default,
            allowed_domains=allowed_domains,
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
