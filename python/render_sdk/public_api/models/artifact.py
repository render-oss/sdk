import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build import Build
    from ..models.schemas_image import SchemasImage


T = TypeVar("T", bound="Artifact")


@_attrs_define
class Artifact:
    """
    Attributes:
        id (str):
        artifact_source_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        build (Union[Unset, Build]): Present when the artifact source is currently build-based. Mutually exclusive with
            `image`.
        image (Union[Unset, SchemasImage]): Present when the artifact source is currently image-based. Mutually
            exclusive with `build`.
    """

    id: str
    artifact_source_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    build: Union[Unset, "Build"] = UNSET
    image: Union[Unset, "SchemasImage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        artifact_source_id = self.artifact_source_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        build: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build, Unset):
            build = self.build.to_dict()

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "artifactSourceId": artifact_source_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if build is not UNSET:
            field_dict["build"] = build
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build import Build
        from ..models.schemas_image import SchemasImage

        d = dict(src_dict)
        id = d.pop("id")

        artifact_source_id = d.pop("artifactSourceId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _build = d.pop("build", UNSET)
        build: Union[Unset, Build]
        if isinstance(_build, Unset):
            build = UNSET
        else:
            build = Build.from_dict(_build)

        _image = d.pop("image", UNSET)
        image: Union[Unset, SchemasImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = SchemasImage.from_dict(_image)

        artifact = cls(
            id=id,
            artifact_source_id=artifact_source_id,
            created_at=created_at,
            updated_at=updated_at,
            build=build,
            image=image,
        )

        artifact.additional_properties = d
        return artifact

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
