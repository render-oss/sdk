from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_credential_injection import SandboxCredentialInjection


T = TypeVar("T", bound="SandboxCredentialCreate")


@_attrs_define
class SandboxCredentialCreate:
    """The credential configuration to create, including request matching and injection settings.

    Attributes:
        id (str): The case-sensitive ID you assign to the credential, unique within its sandbox group. Use only letters,
            numbers, periods, underscores, tildes, and hyphens. The names `.` and `..` and IDs starting with `rnd-` are
            reserved.
             Example: my-inference-key.
        domain (str): The destination hostname to match for credential injection. Must be a public DNS hostname. Render
            normalizes it to lowercase and matches it exactly. IP addresses, ports, wildcards, and local or internal
            hostnames are not supported.
        value (str): The secret value to store, up to 5 KiB (5120 UTF-8 bytes).
        injection (SandboxCredentialInjection): Settings for injecting the secret value into matching outbound HTTPS
            requests.
        enabled (bool | Unset): Whether this credential is enabled for injection. Defaults to `true`. Default: True.
        methods (list[str] | Unset): The HTTP methods to match for credential injection. Supported methods are GET,
            HEAD, POST, PUT, PATCH, DELETE, and OPTIONS, normalized to uppercase. Omit or provide an empty list to match any
            method.
        paths (list[str] | Unset): The request path patterns to match for credential injection. Each pattern must match
            the entire absolute path. Use `*` for one nonempty path segment or `**` for one or more segments. Wildcards must
            occupy whole segments. For example, `/a/*` matches `/a/b`, and `/a/**` also matches `/a/b/c`. Neither matches
            `/a`. Patterns do not support query strings, fragments, or escaping. Request query strings do not affect
            matching. Omit or provide an empty list to match any path.
    """

    id: str
    domain: str
    value: str
    injection: SandboxCredentialInjection
    enabled: bool | Unset = True
    methods: list[str] | Unset = UNSET
    paths: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        domain = self.domain

        value = self.value

        injection = self.injection.to_dict()

        enabled = self.enabled

        methods: list[str] | Unset = UNSET
        if not isinstance(self.methods, Unset):
            methods = self.methods

        paths: list[str] | Unset = UNSET
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
        from ..models.sandbox_credential_injection import SandboxCredentialInjection  # noqa: PLC0415

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
