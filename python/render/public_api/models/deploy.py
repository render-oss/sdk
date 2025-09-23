import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.deploy_status import DeployStatus
from ..models.deploy_trigger import DeployTrigger
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deploy_commit import DeployCommit
    from ..models.deploy_image import DeployImage


T = TypeVar("T", bound="Deploy")


@_attrs_define
class Deploy:
    """
    Attributes:
        id (str):
        commit (Union[Unset, DeployCommit]):
        image (Union[Unset, DeployImage]): Image information used when creating the deploy. Not present for Git-backed
            deploys
        status (Union[Unset, DeployStatus]):
        trigger (Union[Unset, DeployTrigger]):
        started_at (Union[Unset, datetime.datetime]):
        finished_at (Union[Unset, datetime.datetime]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    id: str
    commit: Union[Unset, "DeployCommit"] = UNSET
    image: Union[Unset, "DeployImage"] = UNSET
    status: Union[Unset, DeployStatus] = UNSET
    trigger: Union[Unset, DeployTrigger] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    finished_at: Union[Unset, datetime.datetime] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        commit: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.commit, Unset):
            commit = self.commit.to_dict()

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        trigger: Union[Unset, str] = UNSET
        if not isinstance(self.trigger, Unset):
            trigger = self.trigger.value

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if commit is not UNSET:
            field_dict["commit"] = commit
        if image is not UNSET:
            field_dict["image"] = image
        if status is not UNSET:
            field_dict["status"] = status
        if trigger is not UNSET:
            field_dict["trigger"] = trigger
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deploy_commit import DeployCommit
        from ..models.deploy_image import DeployImage

        d = dict(src_dict)
        id = d.pop("id")

        _commit = d.pop("commit", UNSET)
        commit: Union[Unset, DeployCommit]
        if isinstance(_commit, Unset):
            commit = UNSET
        else:
            commit = DeployCommit.from_dict(_commit)

        _image = d.pop("image", UNSET)
        image: Union[Unset, DeployImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = DeployImage.from_dict(_image)

        _status = d.pop("status", UNSET)
        status: Union[Unset, DeployStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DeployStatus(_status)

        _trigger = d.pop("trigger", UNSET)
        trigger: Union[Unset, DeployTrigger]
        if isinstance(_trigger, Unset):
            trigger = UNSET
        else:
            trigger = DeployTrigger(_trigger)

        _started_at = d.pop("startedAt", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _finished_at = d.pop("finishedAt", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        deploy = cls(
            id=id,
            commit=commit,
            image=image,
            status=status,
            trigger=trigger,
            started_at=started_at,
            finished_at=finished_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        deploy.additional_properties = d
        return deploy

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
