import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.image_version import ImageVersion


T = TypeVar("T", bound="WorkflowVersion")


@_attrs_define
class WorkflowVersion:
    """
    Attributes:
        id (str):
        workflow_id (str):
        name (str):
        image (ImageVersion):
        created_at (datetime.datetime):
    """

    id: str
    workflow_id: str
    name: str
    image: "ImageVersion"
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        workflow_id = self.workflow_id

        name = self.name

        image = self.image.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workflowId": workflow_id,
                "name": name,
                "image": image,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.image_version import ImageVersion

        d = dict(src_dict)
        id = d.pop("id")

        workflow_id = d.pop("workflowId")

        name = d.pop("name")

        image = ImageVersion.from_dict(d.pop("image"))

        created_at = isoparse(d.pop("createdAt"))

        workflow_version = cls(
            id=id,
            workflow_id=workflow_id,
            name=name,
            image=image,
            created_at=created_at,
        )

        workflow_version.additional_properties = d
        return workflow_version

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
