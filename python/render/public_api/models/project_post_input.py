from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_post_environment_input import ProjectPOSTEnvironmentInput


T = TypeVar("T", bound="ProjectPOSTInput")


@_attrs_define
class ProjectPOSTInput:
    """
    Attributes:
        name (str): The name of the project
        owner_id (str): The ID of the owner that the project belongs to
        environments (list['ProjectPOSTEnvironmentInput']): The environments to create when creating the project
    """

    name: str
    owner_id: str
    environments: list["ProjectPOSTEnvironmentInput"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        owner_id = self.owner_id

        environments = []
        for environments_item_data in self.environments:
            environments_item = environments_item_data.to_dict()
            environments.append(environments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "environments": environments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_post_environment_input import ProjectPOSTEnvironmentInput

        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        environments = []
        _environments = d.pop("environments")
        for environments_item_data in _environments:
            environments_item = ProjectPOSTEnvironmentInput.from_dict(environments_item_data)

            environments.append(environments_item)

        project_post_input = cls(
            name=name,
            owner_id=owner_id,
            environments=environments,
        )

        project_post_input.additional_properties = d
        return project_post_input

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
