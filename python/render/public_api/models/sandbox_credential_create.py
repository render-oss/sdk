from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_credential_injection import SandboxCredentialInjection


T = TypeVar("T", bound="SandboxCredentialCreate")


@_attrs_define
class SandboxCredentialCreate:
    """
    Attributes:
        id (str): Caller-supplied URL-safe name, unique within the sandbox group. The names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        domain (str): Exact public DNS hostname, normalized to lowercase. IP addresses, ports,
            wildcards, and local/internal hostnames are not supported.
        value (str): Secret value to store for this credential ID. The largest supported secret
            value is 5 KiB (5120 UTF-8 bytes).
        injection (SandboxCredentialInjection):
        enabled (Union[Unset, bool]):  Default: True.
        methods (Union[Unset, list[str]]): GET, HEAD, POST, PUT, PATCH, DELETE, or OPTIONS, normalized to uppercase.
            Omitted or empty matches any method.
        paths (Union[Unset, list[str]]): Exact absolute request paths, without query strings, fragments,
            escaping, or patterns. Omitted or empty matches any path.
    """

    id: str
    domain: str
    value: str
    injection: "SandboxCredentialInjection"
    enabled: Union[Unset, bool] = True
    methods: Union[Unset, list[str]] = UNSET
    paths: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        domain = self.domain

        value = self.value

        injection = self.injection.to_dict()

        enabled = self.enabled

        methods: Union[Unset, list[str]] = UNSET
        if not isinstance(self.methods, Unset):
            methods = self.methods

        paths: Union[Unset, list[str]] = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "domain": domain,
                "value": value,
                "injection": injection,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if methods is not UNSET:
            field_dict["methods"] = methods
        if paths is not UNSET:
            field_dict["paths"] = paths

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_credential_injection import SandboxCredentialInjection

        d = dict(src_dict)
        id = d.pop("id")

        domain = d.pop("domain")

        value = d.pop("value")

        injection = SandboxCredentialInjection.from_dict(d.pop("injection"))

        enabled = d.pop("enabled", UNSET)

        methods = cast(list[str], d.pop("methods", UNSET))

        paths = cast(list[str], d.pop("paths", UNSET))

        sandbox_credential_create = cls(
            id=id,
            domain=domain,
            value=value,
            injection=injection,
            enabled=enabled,
            methods=methods,
            paths=paths,
        )

        sandbox_credential_create.additional_properties = d
        return sandbox_credential_create

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
