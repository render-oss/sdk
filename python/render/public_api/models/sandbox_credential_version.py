from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxCredentialVersion")


@_attrs_define
class SandboxCredentialVersion:
    """Metadata for a credential version. These endpoints do not return secret values.

    Attributes:
        id (int): The ID of the credential version. Each new version receives a higher ID, including versions created by
            a restore.
        updated_at (datetime.datetime): The timestamp when this credential version was created, in ISO 8601 format.
        updated_by (str): The ID of the authenticated identity that created this credential version.
        fingerprint (str): A fingerprint of the routing settings, injection settings, and secret value. Matching
            fingerprints identify equivalent credential configurations within the same sandbox group. Fingerprints cannot be
            compared across groups.
        restored_from_version_id (int | Unset): The ID of the credential version restored to create this version.
            Omitted for versions created by a create or update request.
    """

    id: int
    updated_at: datetime.datetime
    updated_by: str
    fingerprint: str
    restored_from_version_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        updated_at = self.updated_at.isoformat()

        updated_by = self.updated_by

        fingerprint = self.fingerprint

        restored_from_version_id = self.restored_from_version_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "updatedAt": updated_at,
                "updatedBy": updated_by,
                "fingerprint": fingerprint,
            }
        )
        if restored_from_version_id is not UNSET:
            field_dict["restoredFromVersionId"] = restored_from_version_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        updated_by = d.pop("updatedBy")

        fingerprint = d.pop("fingerprint")

        restored_from_version_id = d.pop("restoredFromVersionId", UNSET)

        sandbox_credential_version = cls(
            id=id,
            updated_at=updated_at,
            updated_by=updated_by,
            fingerprint=fingerprint,
            restored_from_version_id=restored_from_version_id,
        )

        sandbox_credential_version.additional_properties = d
        return sandbox_credential_version

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
