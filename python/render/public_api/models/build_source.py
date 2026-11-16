from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_source_git import BuildSourceGit
    from ..models.build_source_image import BuildSourceImage
    from ..models.build_source_service_link import BuildSourceServiceLink


T = TypeVar("T", bound="BuildSource")


@_attrs_define
class BuildSource:
    """
    Attributes:
        id (str):
        name (str):
        owner_id (str): ID of the workspace this build source belongs to.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        service_links (list[BuildSourceServiceLink]): Services currently linked to this build source.
        project_id (str | Unset): ID of the project this build source is scoped to, if any.
        git (BuildSourceGit | Unset):
        image (BuildSourceImage | Unset):
    """

    id: str
    name: str
    owner_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    service_links: list[BuildSourceServiceLink]
    project_id: str | Unset = UNSET
    git: BuildSourceGit | Unset = UNSET
    image: BuildSourceImage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        owner_id = self.owner_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        service_links = []
        for service_links_item_data in self.service_links:
            service_links_item = service_links_item_data.to_dict()
            service_links.append(service_links_item)

        project_id = self.project_id

        git: dict[str, Any] | Unset = UNSET
        if not isinstance(self.git, Unset):
            git = self.git.to_dict()

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ownerId": owner_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "serviceLinks": service_links,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if git is not UNSET:
            field_dict["git"] = git
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_source_git import BuildSourceGit  # noqa: PLC0415
        from ..models.build_source_image import BuildSourceImage  # noqa: PLC0415
        from ..models.build_source_service_link import BuildSourceServiceLink  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        service_links = []
        _service_links = d.pop("serviceLinks")
        for service_links_item_data in _service_links:
            service_links_item = BuildSourceServiceLink.from_dict(service_links_item_data)

            service_links.append(service_links_item)

        project_id = d.pop("projectId", UNSET)

        _git = d.pop("git", UNSET)
        git: BuildSourceGit | Unset
        if isinstance(_git, Unset):
            git = UNSET
        else:
            git = BuildSourceGit.from_dict(_git)

        _image = d.pop("image", UNSET)
        image: BuildSourceImage | Unset
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = BuildSourceImage.from_dict(_image)

        build_source = cls(
            id=id,
            name=name,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            service_links=service_links,
            project_id=project_id,
            git=git,
            image=image,
        )

        build_source.additional_properties = d
        return build_source

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
