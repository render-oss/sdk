from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_credential_injection_type import SandboxCredentialInjectionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxCredentialInjection")


@_attrs_define
class SandboxCredentialInjection:
    """Settings for injecting the secret value into matching outbound HTTPS requests.

    Attributes:
        type_ (SandboxCredentialInjectionType): How Render adds the credential to a matching request. For `basic`, the
            value after applying `template` must have the form `username:password`. Do not provide `name`.
        name (str | Unset): The header, cookie, or query parameter to set. Required for `header`, `cookie`, and `query`.
            Headers that control routing or connection behavior cannot be used.
        template (str | Unset): A template containing 1–5 occurrences of `${SECRET}`, such as `Bearer ${SECRET}`. Render
            replaces each occurrence with the secret value. Omit to use the secret value without a template.
             Example: Bearer ${SECRET}.
    """

    type_: SandboxCredentialInjectionType
    name: str | Unset = UNSET
    template: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        name = self.name

        template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = SandboxCredentialInjectionType(d.pop("type"))

        name = d.pop("name", UNSET)

        template = d.pop("template", UNSET)

        sandbox_credential_injection = cls(
            type_=type_,
            name=name,
            template=template,
        )

        sandbox_credential_injection.additional_properties = d
        return sandbox_credential_injection

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
