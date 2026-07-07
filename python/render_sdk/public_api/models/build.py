import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.build_status import BuildStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Build")


@_attrs_define
class Build:
    """Present when the artifact source is currently build-based. Mutually exclusive with `image`.

    Attributes:
        id (str):
        status (Union[Unset, BuildStatus]):
        build_started_at (Union[Unset, datetime.datetime]):
        build_finished_at (Union[Unset, datetime.datetime]):
        runtime (Union[Unset, str]):
        commit_id (Union[Unset, str]):
        commit_url (Union[Unset, str]):
    """

    id: str
    status: Union[Unset, BuildStatus] = UNSET
    build_started_at: Union[Unset, datetime.datetime] = UNSET
    build_finished_at: Union[Unset, datetime.datetime] = UNSET
    runtime: Union[Unset, str] = UNSET
    commit_id: Union[Unset, str] = UNSET
    commit_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        build_started_at: Union[Unset, str] = UNSET
        if not isinstance(self.build_started_at, Unset):
            build_started_at = self.build_started_at.isoformat()

        build_finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.build_finished_at, Unset):
            build_finished_at = self.build_finished_at.isoformat()

        runtime = self.runtime

        commit_id = self.commit_id

        commit_url = self.commit_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if build_started_at is not UNSET:
            field_dict["buildStartedAt"] = build_started_at
        if build_finished_at is not UNSET:
            field_dict["buildFinishedAt"] = build_finished_at
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if commit_id is not UNSET:
            field_dict["commitId"] = commit_id
        if commit_url is not UNSET:
            field_dict["commitUrl"] = commit_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        _status = d.pop("status", UNSET)
        status: Union[Unset, BuildStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BuildStatus(_status)

        _build_started_at = d.pop("buildStartedAt", UNSET)
        build_started_at: Union[Unset, datetime.datetime]
        if isinstance(_build_started_at, Unset):
            build_started_at = UNSET
        else:
            build_started_at = isoparse(_build_started_at)

        _build_finished_at = d.pop("buildFinishedAt", UNSET)
        build_finished_at: Union[Unset, datetime.datetime]
        if isinstance(_build_finished_at, Unset):
            build_finished_at = UNSET
        else:
            build_finished_at = isoparse(_build_finished_at)

        runtime = d.pop("runtime", UNSET)

        commit_id = d.pop("commitId", UNSET)

        commit_url = d.pop("commitUrl", UNSET)

        build = cls(
            id=id,
            status=status,
            build_started_at=build_started_at,
            build_finished_at=build_finished_at,
            runtime=runtime,
            commit_id=commit_id,
            commit_url=commit_url,
        )

        build.additional_properties = d
        return build

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
