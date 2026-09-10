import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_run import BuildRun
    from ..models.schemas_image import SchemasImage


T = TypeVar("T", bound="Build")


@_attrs_define
class Build:
    """
    Attributes:
        id (str):
        build_source_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        build_run (Union[Unset, BuildRun]): The Render build run that produced this build. Present when the build source
            is currently build-based. Mutually exclusive with `image`.
        image (Union[Unset, SchemasImage]): Present when the build source is currently image-based. Mutually exclusive
            with `buildRun`.
        assets_deleted_at (Union[Unset, datetime.datetime]):
    """

    id: str
    build_source_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    build_run: Union[Unset, "BuildRun"] = UNSET
    image: Union[Unset, "SchemasImage"] = UNSET
    assets_deleted_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        build_source_id = self.build_source_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        build_run: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_run, Unset):
            build_run = self.build_run.to_dict()

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        assets_deleted_at: Union[Unset, str] = UNSET
        if not isinstance(self.assets_deleted_at, Unset):
            assets_deleted_at = self.assets_deleted_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "buildSourceId": build_source_id,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if build_run is not UNSET:
            field_dict["buildRun"] = build_run
        if image is not UNSET:
            field_dict["image"] = image
        if assets_deleted_at is not UNSET:
            field_dict["assetsDeletedAt"] = assets_deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_run import BuildRun
        from ..models.schemas_image import SchemasImage

        d = dict(src_dict)
        id = d.pop("id")

        build_source_id = d.pop("buildSourceId")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _build_run = d.pop("buildRun", UNSET)
        build_run: Union[Unset, BuildRun]
        if isinstance(_build_run, Unset):
            build_run = UNSET
        else:
            build_run = BuildRun.from_dict(_build_run)

        _image = d.pop("image", UNSET)
        image: Union[Unset, SchemasImage]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = SchemasImage.from_dict(_image)

        _assets_deleted_at = d.pop("assetsDeletedAt", UNSET)
        assets_deleted_at: Union[Unset, datetime.datetime]
        if isinstance(_assets_deleted_at, Unset):
            assets_deleted_at = UNSET
        else:
            assets_deleted_at = isoparse(_assets_deleted_at)

        build = cls(
            id=id,
            build_source_id=build_source_id,
            created_at=created_at,
            updated_at=updated_at,
            build_run=build_run,
            image=image,
            assets_deleted_at=assets_deleted_at,
        )

        build.additional_properties = d
        return build

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
