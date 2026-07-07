from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_source_git import ArtifactSourceGit
    from ..models.artifact_source_image import ArtifactSourceImage


T = TypeVar("T", bound="ArtifactSourcePOSTInput")


@_attrs_define
class ArtifactSourcePOSTInput:
    """
    Attributes:
        owner_id (str):
        name (str):
        project_id (Union[Unset, str]):
        git (Union[Unset, ArtifactSourceGit]):
        image (Union[Unset, ArtifactSourceImage]):
    """

    owner_id: str
    name: str
    project_id: Union[Unset, str] = UNSET
    git: Union[Unset, "ArtifactSourceGit"] = UNSET
    image: Union[Unset, "ArtifactSourceImage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        name = self.name

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
                "ownerId": owner_id,
                "name": name,
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

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        name = d.pop("name")

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

        artifact_source_post_input = cls(
            owner_id=owner_id,
            name=name,
            project_id=project_id,
            git=git,
            image=image,
        )

        artifact_source_post_input.additional_properties = d
        return artifact_source_post_input

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
