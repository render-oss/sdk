from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_credential_injection import SandboxCredentialInjection
    from ..models.sandbox_credential_version import SandboxCredentialVersion


T = TypeVar("T", bound="SandboxCredential")


@_attrs_define
class SandboxCredential:
    """Desired credential configuration scoped to one sandbox group. Secret values
    are independent for each credential ID and are never returned, including to admins.

        Attributes:
            id (str): Caller-supplied URL-safe name, unique within the sandbox group. The names
                `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
                 Example: my-inference-key.
            domain (str): Exact public DNS hostname, normalized to lowercase. IP addresses, ports,
                wildcards, and local/internal hostnames are not supported.
                 Example: api.render.com.
            enabled (bool):
            methods (list[str]): GET, HEAD, POST, PUT, PATCH, DELETE, or OPTIONS, normalized to uppercase.
                An empty list matches any method.
            paths (list[str]): Exact absolute request paths, without query strings, fragments,
                escaping, or patterns. An empty list matches any path.
            injection (SandboxCredentialInjection):
            version (Union[Unset, SandboxCredentialVersion]):
    """

    id: str
    domain: str
    enabled: bool
    methods: list[str]
    paths: list[str]
    injection: "SandboxCredentialInjection"
    version: Union[Unset, "SandboxCredentialVersion"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        domain = self.domain

        enabled = self.enabled

        methods = self.methods

        paths = self.paths

        injection = self.injection.to_dict()

        version: Union[Unset, dict[str, Any]] = UNSET
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
        from ..models.sandbox_credential_injection import SandboxCredentialInjection
        from ..models.sandbox_credential_version import SandboxCredentialVersion

        d = dict(src_dict)
        id = d.pop("id")

        domain = d.pop("domain")

        enabled = d.pop("enabled")

        methods = cast(list[str], d.pop("methods"))

        paths = cast(list[str], d.pop("paths"))

        injection = SandboxCredentialInjection.from_dict(d.pop("injection"))

        _version = d.pop("version", UNSET)
        version: Union[Unset, SandboxCredentialVersion]
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
