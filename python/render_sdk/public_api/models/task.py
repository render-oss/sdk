import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """
    Attributes:
        id (str):
        name (str):
        created_at (datetime.datetime):
        workflow_id (Union[Unset, str]):
        workflow_version_id (Union[Unset, str]):
    """

    id: str
    name: str
    created_at: datetime.datetime
    workflow_id: Union[Unset, str] = UNSET
    workflow_version_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        created_at = self.created_at.isoformat()

        workflow_id = self.workflow_id

        workflow_version_id = self.workflow_version_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "createdAt": created_at,
            }
        )
        if workflow_id is not UNSET:
            field_dict["workflowId"] = workflow_id
        if workflow_version_id is not UNSET:
            field_dict["workflowVersionId"] = workflow_version_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        workflow_id = d.pop("workflowId", UNSET)

        workflow_version_id = d.pop("workflowVersionId", UNSET)

        task = cls(
            id=id,
            name=name,
            created_at=created_at,
            workflow_id=workflow_id,
            workflow_version_id=workflow_version_id,
        )

        task.additional_properties = d
        return task

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
