import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_ref import ResourceRef


T = TypeVar("T", bound="BlueprintDetail")


@_attrs_define
class BlueprintDetail:
    """
    Attributes:
        id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        name (str):
        status (Status):
        auto_sync (bool): Automatically sync changes to render.yaml
        repo (str):
        branch (str):
        resources (list['ResourceRef']):
        last_sync (Union[Unset, datetime.datetime]):
    """

    id: str
    name: str
    status: Status
    auto_sync: bool
    repo: str
    branch: str
    resources: list["ResourceRef"]
    last_sync: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        status = self.status.value

        auto_sync = self.auto_sync

        repo = self.repo

        branch = self.branch

        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)

        last_sync: Union[Unset, str] = UNSET
        if not isinstance(self.last_sync, Unset):
            last_sync = self.last_sync.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "status": status,
                "autoSync": auto_sync,
                "repo": repo,
                "branch": branch,
                "resources": resources,
            }
        )
        if last_sync is not UNSET:
            field_dict["lastSync"] = last_sync

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_ref import ResourceRef

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        status = Status(d.pop("status"))

        auto_sync = d.pop("autoSync")

        repo = d.pop("repo")

        branch = d.pop("branch")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = ResourceRef.from_dict(resources_item_data)

            resources.append(resources_item)

        _last_sync = d.pop("lastSync", UNSET)
        last_sync: Union[Unset, datetime.datetime]
        if isinstance(_last_sync, Unset):
            last_sync = UNSET
        else:
            last_sync = isoparse(_last_sync)

        blueprint_detail = cls(
            id=id,
            name=name,
            status=status,
            auto_sync=auto_sync,
            repo=repo,
            branch=branch,
            resources=resources,
            last_sync=last_sync,
        )

        blueprint_detail.additional_properties = d
        return blueprint_detail

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
