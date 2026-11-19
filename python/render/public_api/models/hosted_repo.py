from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hosted_repo_state import HostedRepoState
from ..types import UNSET, Unset

T = TypeVar("T", bound="HostedRepo")


@_attrs_define
class HostedRepo:
    """
    Attributes:
        id (str):  Example: hrp-d04m9b1r0fns73ckp94f.
        owner_id (str):  Example: tea-cph1rs3idesc73a2b2mg.
        name (str):  Example: bookmarks.
        state (HostedRepoState): An `inactive` repo has nothing that uses it and is deleted at `deleteAt`.
        remote_url (str): The URL git pushes to and clones from Example: https://code.render.com/tea-
            cph1rs3idesc73a2b2mg/bookmarks.git.
        web_url (str): The URL a service deploys from Example: https://code.render.com/tea-
            cph1rs3idesc73a2b2mg/bookmarks.
        service_ids (list[str]): The services that deploy from the repo
        created_at (datetime.datetime):
        delete_at (datetime.datetime | Unset): When the repo will be deleted. Set only while it's inactive.
    """

    id: str
    owner_id: str
    name: str
    state: HostedRepoState
    remote_url: str
    web_url: str
    service_ids: list[str]
    created_at: datetime.datetime
    delete_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        owner_id = self.owner_id

        name = self.name

        state = self.state.value

        remote_url = self.remote_url

        web_url = self.web_url

        service_ids = self.service_ids

        created_at = self.created_at.isoformat()

        delete_at: str | Unset = UNSET
        if not isinstance(self.delete_at, Unset):
            delete_at = self.delete_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ownerId": owner_id,
                "name": name,
                "state": state,
                "remoteUrl": remote_url,
                "webUrl": web_url,
                "serviceIds": service_ids,
                "createdAt": created_at,
            }
        )
        if delete_at is not UNSET:
            field_dict["deleteAt"] = delete_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        owner_id = d.pop("ownerId")

        name = d.pop("name")

        state = HostedRepoState(d.pop("state"))

        remote_url = d.pop("remoteUrl")

        web_url = d.pop("webUrl")

        service_ids = cast(list[str], d.pop("serviceIds"))

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        _delete_at = d.pop("deleteAt", UNSET)
        delete_at: datetime.datetime | Unset
        if isinstance(_delete_at, Unset):
            delete_at = UNSET
        else:
            delete_at = datetime.datetime.fromisoformat(_delete_at)

        hosted_repo = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            state=state,
            remote_url=remote_url,
            web_url=web_url,
            service_ids=service_ids,
            created_at=created_at,
            delete_at=delete_at,
        )

        hosted_repo.additional_properties = d
        return hosted_repo

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
