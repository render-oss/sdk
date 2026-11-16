from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_build_status import SandboxBuildStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_build_source import SandboxBuildSource


T = TypeVar("T", bound="SandboxBuild")


@_attrs_define
class SandboxBuild:
    """A build that converts a container image into an image that sandboxes can use.

    Attributes:
        id (str): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        name (str): The name used to select this image when creating a sandbox. Multiple builds can share a name.
        source (SandboxBuildSource): The source container image used for this build.
        source_digest (str): The digest of the source image converted by this build. Example: sha256:c19d4a1....
        status (SandboxBuildStatus): The sandbox build's current status.
        created_at (datetime.datetime): The timestamp when the sandbox build was created, in ISO 8601 format.
        failure_reason (None | str | Unset): A description of why the build failed. Null unless the status is `failed`.
            May include error text from the image registry. When displaying errors, use `failureCode` to select the main
            message and show this value as additional detail.
        failure_code (None | str | Unset): A machine-readable reason the build failed. Null unless the status is
            `failed`. See `sandboxBuildFailureCode` for known codes. Treat unrecognized codes as `internal_error`.
             Example: image_pull_failed.
        finished_at (datetime.datetime | None | Unset): The timestamp when the build succeeded or failed, in ISO 8601
            format. Null while the build is pending or running.
    """

    id: str
    sandbox_group_id: str
    name: str
    source: SandboxBuildSource
    source_digest: str
    status: SandboxBuildStatus
    created_at: datetime.datetime
    failure_reason: None | str | Unset = UNSET
    failure_code: None | str | Unset = UNSET
    finished_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sandbox_group_id = self.sandbox_group_id

        name = self.name

        source = self.source.to_dict()

        source_digest = self.source_digest

        status = self.status.value

        created_at = self.created_at.isoformat()

        failure_reason: None | str | Unset
        if isinstance(self.failure_reason, Unset):
            failure_reason = UNSET
        else:
            failure_reason = self.failure_reason

        failure_code: None | str | Unset
        if isinstance(self.failure_code, Unset):
            failure_code = UNSET
        else:
            failure_code = self.failure_code

        finished_at: None | str | Unset
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sandboxGroupId": sandbox_group_id,
                "name": name,
                "source": source,
                "sourceDigest": source_digest,
                "status": status,
                "createdAt": created_at,
            }
        )
        if failure_reason is not UNSET:
            field_dict["failureReason"] = failure_reason
        if failure_code is not UNSET:
            field_dict["failureCode"] = failure_code
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_build_source import SandboxBuildSource  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        sandbox_group_id = d.pop("sandboxGroupId")

        name = d.pop("name")

        source = SandboxBuildSource.from_dict(d.pop("source"))

        source_digest = d.pop("sourceDigest")

        status = SandboxBuildStatus(d.pop("status"))

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        def _parse_failure_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason", UNSET))

        def _parse_failure_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        failure_code = _parse_failure_code(d.pop("failureCode", UNSET))

        def _parse_finished_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = datetime.datetime.fromisoformat(data)

                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        finished_at = _parse_finished_at(d.pop("finishedAt", UNSET))

        sandbox_build = cls(
            id=id,
            sandbox_group_id=sandbox_group_id,
            name=name,
            source=source,
            source_digest=source_digest,
            status=status,
            created_at=created_at,
            failure_reason=failure_reason,
            failure_code=failure_code,
            finished_at=finished_at,
        )

        sandbox_build.additional_properties = d
        return sandbox_build

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
