from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_credential_injection_type import SandboxCredentialInjectionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxCredentialInjection")


@_attrs_define
class SandboxCredentialInjection:
    """
    Attributes:
        type_ (SandboxCredentialInjectionType): How to inject the credential into a matching request. Basic
            authentication
            uses the rendered value in username:password form and does not accept name.
        name (Union[Unset, str]): Required for header, cookie, and query injection. Routing and connection
            headers cannot be targeted.
        template (Union[Unset, str]): Literal template containing 1-5 occurrences of ${SECRET}, such as
            "Bearer ${SECRET}". Each ${SECRET} is replaced directly with the
            assigned secret value. Omit to use the raw secret value.
             Example: Bearer ${SECRET}.
    """

    type_: SandboxCredentialInjectionType
    name: Union[Unset, str] = UNSET
    template: Union[Unset, str] = UNSET
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
