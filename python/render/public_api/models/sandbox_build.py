import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sandbox_build_status import SandboxBuildStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_build_source import SandboxBuildSource


T = TypeVar("T", bound="SandboxBuild")


@_attrs_define
class SandboxBuild:
    """
    Attributes:
        id (str):  Example: sbb-cph1rs3idesc73a2b2mg.
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        name (str): Names the image. Every build of an image shares it.
        source (SandboxBuildSource):
        source_digest (str): The image digest the build converts. Example: sha256:c19d4a1....
        status (SandboxBuildStatus):
        created_at (datetime.datetime):
        failure_reason (Union[None, Unset, str]): Why the build failed. Null unless `failed`.
        finished_at (Union[None, Unset, datetime.datetime]): When the build succeeded or failed.
    """

    id: str
    sandbox_group_id: str
    name: str
    source: "SandboxBuildSource"
    source_digest: str
    status: SandboxBuildStatus
    created_at: datetime.datetime
    failure_reason: Union[None, Unset, str] = UNSET
    finished_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sandbox_group_id = self.sandbox_group_id

        name = self.name

        source = self.source.to_dict()

        source_digest = self.source_digest

        status = self.status.value

        created_at = self.created_at.isoformat()

        failure_reason: Union[None, Unset, str]
        if isinstance(self.failure_reason, Unset):
            failure_reason = UNSET
        else:
            failure_reason = self.failure_reason

        finished_at: Union[None, Unset, str]
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
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_build_source import SandboxBuildSource

        d = dict(src_dict)
        id = d.pop("id")

        sandbox_group_id = d.pop("sandboxGroupId")

        name = d.pop("name")

        source = SandboxBuildSource.from_dict(d.pop("source"))

        source_digest = d.pop("sourceDigest")

        status = SandboxBuildStatus(d.pop("status"))

        created_at = isoparse(d.pop("createdAt"))

        def _parse_failure_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        failure_reason = _parse_failure_reason(d.pop("failureReason", UNSET))

        def _parse_finished_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

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
