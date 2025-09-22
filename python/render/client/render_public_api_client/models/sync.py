import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sync_state import SyncState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.commit_ref import CommitRef


T = TypeVar("T", bound="Sync")


@_attrs_define
class Sync:
    """
    Attributes:
        id (str):  Example: exe-cph1rs3idesc73a2b2mg.
        commit (CommitRef):
        state (SyncState):
        started_at (Union[Unset, datetime.datetime]):
        completed_at (Union[Unset, datetime.datetime]):
    """

    id: str
    commit: "CommitRef"
    state: SyncState
    started_at: Union[Unset, datetime.datetime] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        commit = self.commit.to_dict()

        state = self.state.value

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "commit": commit,
                "state": state,
            }
        )
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.commit_ref import CommitRef

        d = dict(src_dict)
        id = d.pop("id")

        commit = CommitRef.from_dict(d.pop("commit"))

        state = SyncState(d.pop("state"))

        _started_at = d.pop("startedAt", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _completed_at = d.pop("completedAt", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        sync = cls(
            id=id,
            commit=commit,
            state=state,
            started_at=started_at,
            completed_at=completed_at,
        )

        sync.additional_properties = d
        return sync

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
