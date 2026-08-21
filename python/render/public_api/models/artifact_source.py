import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_source_git import ArtifactSourceGit
    from ..models.artifact_source_image import ArtifactSourceImage
    from ..models.artifact_source_service_link import ArtifactSourceServiceLink


T = TypeVar("T", bound="ArtifactSource")


@_attrs_define
class ArtifactSource:
    """
    Attributes:
        id (str):
        name (str):
        owner_id (str): ID of the workspace this artifact source belongs to.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        service_links (list['ArtifactSourceServiceLink']): Services currently linked to this artifact source.
        project_id (Union[Unset, str]): ID of the project this artifact source is scoped to, if any.
        git (Union[Unset, ArtifactSourceGit]):
        image (Union[Unset, ArtifactSourceImage]):
    """

    id: str
    name: str
    owner_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    service_links: list["ArtifactSourceServiceLink"]
    project_id: Union[Unset, str] = UNSET
    git: Union[Unset, "ArtifactSourceGit"] = UNSET
    image: Union[Unset, "ArtifactSourceImage"] = UNSET
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

        git: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.git, Unset):
            git = self.git.to_dict()

        image: Union[Unset, dict[str, Any]] = UNSET
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
        from ..models.artifact_source_git import ArtifactSourceGit
        from ..models.artifact_source_image import ArtifactSourceImage
        from ..models.artifact_source_service_link import ArtifactSourceServiceLink

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        owner_id = d.pop("ownerId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        service_links = []
        _service_links = d.pop("serviceLinks")
        for service_links_item_data in _service_links:
            service_links_item = ArtifactSourceServiceLink.from_dict(service_links_item_data)

            service_links.append(service_links_item)

        project_id = d.pop("projectId", UNSET)

        _git = d.pop("git", UNSET)
        git: Union[Unset, ArtifactSourceGit]
        if isinstance(_git, Unset):
            git = UNSET
        else:
            git = ArtifactSourceGit.from_dict(_git)

        _image = d.pop("image", UNSET)
        image: Union[Unset, ArtifactSourceImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = ArtifactSourceImage.from_dict(_image)

        artifact_source = cls(
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

        artifact_source.additional_properties = d
        return artifact_source

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
