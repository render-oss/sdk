from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workflow_version import WorkflowVersion


T = TypeVar("T", bound="WorkflowVersionWithCursor")


@_attrs_define
class WorkflowVersionWithCursor:
    """
    Attributes:
        workflow_version (WorkflowVersion):
        cursor (str):
    """

    workflow_version: "WorkflowVersion"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_version = self.workflow_version.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowVersion": workflow_version,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_version import WorkflowVersion

        d = dict(src_dict)
        workflow_version = WorkflowVersion.from_dict(d.pop("workflowVersion"))

        cursor = d.pop("cursor")

        workflow_version_with_cursor = cls(
            workflow_version=workflow_version,
            cursor=cursor,
        )

        workflow_version_with_cursor.additional_properties = d
        return workflow_version_with_cursor

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
