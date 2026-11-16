from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_credential_injection import SandboxCredentialInjection


T = TypeVar("T", bound="SandboxCredentialUpdate")


@_attrs_define
class SandboxCredentialUpdate:
    """The credential settings to update. Omitted top-level fields keep their current values. Providing `injection`
    replaces the entire object. Its `template` defaults to `${SECRET}` when omitted. Empty `methods` or `paths` lists
    remove those filters. Developers can update `injection`, `methods`, `paths`, and `enabled`. Changing `domain` or
    `value` requires an admin.

    Changes to routing, injection, or enabled state create a new version. Setting `value` creates a new version even if
    the secret value is unchanged. The credential ID cannot be changed.

        Attributes:
            value (Union[Unset, str]): The replacement secret value, up to 5 KiB (5120 UTF-8 bytes). Requires an admin. Omit
                to preserve the current value.
            domain (Union[Unset, str]): The destination hostname to match for credential injection. Must be a public DNS
                hostname. Render normalizes it to lowercase and matches it exactly. IP addresses, ports, wildcards, and local or
                internal hostnames are not supported. Omit to preserve the current hostname.
            enabled (Union[Unset, bool]): Whether this credential is enabled for injection. Omit to preserve the current
                setting.
            methods (Union[Unset, list[str]]): The HTTP methods to match for credential injection. Supported methods are
                GET, HEAD, POST, PUT, PATCH, DELETE, and OPTIONS, normalized to uppercase. An empty list matches any method.
                Omit to preserve the current filter.
            paths (Union[Unset, list[str]]): The request path patterns to match for credential injection. Each pattern must
                match the entire absolute path. Use `*` for one nonempty path segment or `**` for one or more segments.
                Wildcards must occupy whole segments. For example, `/a/*` matches `/a/b`, and `/a/**` also matches `/a/b/c`.
                Neither matches `/a`. Patterns do not support query strings, fragments, or escaping. Request query strings do
                not affect matching. An empty list matches any path. Omit to preserve the current filter.
            injection (Union[Unset, SandboxCredentialInjection]): Settings for injecting the secret value into matching
                outbound HTTPS requests.
    """

    value: Union[Unset, str] = UNSET
    domain: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    methods: Union[Unset, list[str]] = UNSET
    paths: Union[Unset, list[str]] = UNSET
    injection: Union[Unset, "SandboxCredentialInjection"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        domain = self.domain

        enabled = self.enabled

        methods: Union[Unset, list[str]] = UNSET
        if not isinstance(self.methods, Unset):
            methods = self.methods

        paths: Union[Unset, list[str]] = UNSET
        if not isinstance(self.paths, Unset):
            paths = self.paths

        injection: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.injection, Unset):
            injection = self.injection.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if domain is not UNSET:
            field_dict["domain"] = domain
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if methods is not UNSET:
            field_dict["methods"] = methods
        if paths is not UNSET:
            field_dict["paths"] = paths
        if injection is not UNSET:
            field_dict["injection"] = injection

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_credential_injection import SandboxCredentialInjection

        d = dict(src_dict)
        value = d.pop("value", UNSET)

        domain = d.pop("domain", UNSET)

        enabled = d.pop("enabled", UNSET)

        methods = cast(list[str], d.pop("methods", UNSET))

        paths = cast(list[str], d.pop("paths", UNSET))

        _injection = d.pop("injection", UNSET)
        injection: Union[Unset, SandboxCredentialInjection]
        if isinstance(_injection, Unset):
            injection = UNSET
        else:
            injection = SandboxCredentialInjection.from_dict(_injection)

        sandbox_credential_update = cls(
            value=value,
            domain=domain,
            enabled=enabled,
            methods=methods,
            paths=paths,
            injection=injection,
        )

        sandbox_credential_update.additional_properties = d
        return sandbox_credential_update

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
