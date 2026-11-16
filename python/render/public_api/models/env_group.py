from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env_group_link import EnvGroupLink
    from ..models.env_var import EnvVar
    from ..models.secret_file import SecretFile


T = TypeVar("T", bound="EnvGroup")


@_attrs_define
class EnvGroup:
    """
    Attributes:
        id (str):
        name (str):
        owner_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        service_links (list[EnvGroupLink]): List of serviceIds linked to the envGroup
        environment_id (str | Unset):
        env_vars (list[EnvVar] | Unset): Omitted if the caller doesn't have the permission to read the environment
            group's secret values.
        secret_files (list[SecretFile] | Unset): Omitted if the caller doesn't have the permission to read the
            environment group's secret values.
    """

    id: str
    name: str
    owner_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    service_links: list[EnvGroupLink]
    environment_id: str | Unset = UNSET
    env_vars: list[EnvVar] | Unset = UNSET
    secret_files: list[SecretFile] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        owner_id = self.owner_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        service_links = []
        for service_links_item_data in self.service_links:
            service_links_item = service_links_item_data.to_dict()
            service_links.append(service_links_item)

        environment_id = self.environment_id

        env_vars: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = []
            for env_vars_item_data in self.env_vars:
                env_vars_item = env_vars_item_data.to_dict()
                env_vars.append(env_vars_item)

        secret_files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secret_files, Unset):
            secret_files = []
            for secret_files_item_data in self.secret_files:
                secret_files_item = secret_files_item_data.to_dict()
                secret_files.append(secret_files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ownerId": owner_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "serviceLinks": service_links,
            }
        )
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars
        if secret_files is not UNSET:
            field_dict["secretFiles"] = secret_files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.env_group_link import EnvGroupLink  # noqa: PLC0415
        from ..models.env_var import EnvVar  # noqa: PLC0415
        from ..models.secret_file import SecretFile  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        service_links = []
        _service_links = d.pop("serviceLinks")
        for service_links_item_data in _service_links:
            service_links_item = EnvGroupLink.from_dict(service_links_item_data)

            service_links.append(service_links_item)

        environment_id = d.pop("environmentId", UNSET)

        _env_vars = d.pop("envVars", UNSET)
        env_vars: list[EnvVar] | Unset = UNSET
        if _env_vars is not UNSET:
            env_vars = []
            for env_vars_item_data in _env_vars:
                env_vars_item = EnvVar.from_dict(env_vars_item_data)

                env_vars.append(env_vars_item)

        _secret_files = d.pop("secretFiles", UNSET)
        secret_files: list[SecretFile] | Unset = UNSET
        if _secret_files is not UNSET:
            secret_files = []
            for secret_files_item_data in _secret_files:
                secret_files_item = SecretFile.from_dict(secret_files_item_data)

                secret_files.append(secret_files_item)

        env_group = cls(
            id=id,
            name=name,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            service_links=service_links,
            environment_id=environment_id,
            env_vars=env_vars,
            secret_files=secret_files,
        )

        env_group.additional_properties = d
        return env_group

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
