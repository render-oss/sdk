from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_source_patch_git import ArtifactSourcePATCHGit
    from ..models.artifact_source_patch_image import ArtifactSourcePATCHImage


T = TypeVar("T", bound="ArtifactSourcePATCHInput")


@_attrs_define
class ArtifactSourcePATCHInput:
    """
    Attributes:
        name (Union[Unset, str]):
        git (Union[Unset, ArtifactSourcePATCHGit]):
        image (Union[Unset, ArtifactSourcePATCHImage]): Patch shape for an artifact source's image identity. Unset
            fields are left unchanged on the underlying image reference. ownerId is intentionally omitted — an artifact
            source's owner is fixed at creation, and changing the image's owner would amount to a different identity.
    """

    name: Union[Unset, str] = UNSET
    git: Union[Unset, "ArtifactSourcePATCHGit"] = UNSET
    image: Union[Unset, "ArtifactSourcePATCHImage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        git: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.git, Unset):
            git = self.git.to_dict()

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if git is not UNSET:
            field_dict["git"] = git
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_source_patch_git import ArtifactSourcePATCHGit
        from ..models.artifact_source_patch_image import ArtifactSourcePATCHImage

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _git = d.pop("git", UNSET)
        git: Union[Unset, ArtifactSourcePATCHGit]
        if isinstance(_git, Unset):
            git = UNSET
        else:
            git = ArtifactSourcePATCHGit.from_dict(_git)

        _image = d.pop("image", UNSET)
        image: Union[Unset, ArtifactSourcePATCHImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = ArtifactSourcePATCHImage.from_dict(_image)

        artifact_source_patch_input = cls(
            name=name,
            git=git,
            image=image,
        )

        artifact_source_patch_input.additional_properties = d
        return artifact_source_patch_input

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
