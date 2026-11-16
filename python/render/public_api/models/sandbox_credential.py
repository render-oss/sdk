from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_credential_injection import SandboxCredentialInjection
    from ..models.sandbox_credential_version import SandboxCredentialVersion


T = TypeVar("T", bound="SandboxCredential")


@_attrs_define
class SandboxCredential:
    """A credential configured for injection into matching outbound HTTPS requests from sandboxes in one sandbox group.
    Each credential stores its own secret value. These endpoints do not return secret values, including to admins.

    Credential injection supports HTTPS requests on port 443. Avoid overlapping credential configurations for the same
    hostname. Multiple matching credentials are not combined.

        Attributes:
            id (str): The case-sensitive ID you assign to the credential, unique within its sandbox group. Use only letters,
                numbers, periods, underscores, tildes, and hyphens. The names `.` and `..` and IDs starting with `rnd-` are
                reserved.
                 Example: my-inference-key.
            domain (str): The destination hostname to match for credential injection. Must be a public DNS hostname. Render
                normalizes it to lowercase and matches it exactly. IP addresses, ports, wildcards, and local or internal
                hostnames are not supported.
                 Example: api.render.com.
            enabled (bool): Whether this credential is enabled for injection.
            methods (list[str]): The HTTP methods to match for credential injection. Supported methods are GET, HEAD, POST,
                PUT, PATCH, DELETE, and OPTIONS, normalized to uppercase. An empty list matches any method.
            paths (list[str]): The request path patterns to match for credential injection. Each pattern must match the
                entire absolute path. Use `*` for one nonempty path segment or `**` for one or more segments. Wildcards must
                occupy whole segments. For example, `/a/*` matches `/a/b`, and `/a/**` also matches `/a/b/c`. Neither matches
                `/a`. Patterns do not support query strings, fragments, or escaping. Request query strings do not affect
                matching. An empty list matches any path.
            injection (SandboxCredentialInjection): Settings for injecting the secret value into matching outbound HTTPS
                requests.
            version (SandboxCredentialVersion | Unset): Metadata for a credential version. These endpoints do not return
                secret values.
    """

    id: str
    domain: str
    enabled: bool
    methods: list[str]
    paths: list[str]
    injection: SandboxCredentialInjection
    version: SandboxCredentialVersion | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        domain = self.domain

        enabled = self.enabled

        methods = self.methods

        paths = self.paths

        injection = self.injection.to_dict()

        version: dict[str, Any] | Unset = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "domain": domain,
                "enabled": enabled,
                "methods": methods,
                "paths": paths,
                "injection": injection,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_credential_injection import SandboxCredentialInjection  # noqa: PLC0415
        from ..models.sandbox_credential_version import SandboxCredentialVersion  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        domain = d.pop("domain")

        enabled = d.pop("enabled")

        methods = cast(list[str], d.pop("methods"))

        paths = cast(list[str], d.pop("paths"))

        injection = SandboxCredentialInjection.from_dict(d.pop("injection"))

        _version = d.pop("version", UNSET)
        version: SandboxCredentialVersion | Unset
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = SandboxCredentialVersion.from_dict(_version)

        sandbox_credential = cls(
            id=id,
            domain=domain,
            enabled=enabled,
            methods=methods,
            paths=paths,
            injection=injection,
            version=version,
        )

        sandbox_credential.additional_properties = d
        return sandbox_credential

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
