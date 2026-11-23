from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_deploy import BuildDeploy
    from ..models.build_run import BuildRun
    from ..models.build_skipped_service import BuildSkippedService
    from ..models.schemas_image import SchemasImage


T = TypeVar("T", bound="BuildWithDeploys")


@_attrs_define
class BuildWithDeploys:
    """
    Attributes:
        id (str):
        build_source_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        deploys (list[BuildDeploy]): The deploys that the build started, one for each service.
        skipped_services (list[BuildSkippedService]): Services in `deploy.serviceScope` that did not get a deploy, with
            the reason for each. The build still runs for the other services. For `autodeploy_only`, suspended services are
            not listed.
        build_run (BuildRun | Unset): The Render build run that produced this build. Present when the build source is
            currently build-based. Mutually exclusive with `image`.
        image (SchemasImage | Unset): Present when the build source is currently image-based. Mutually exclusive with
            `buildRun`.
        assets_deleted_at (datetime.datetime | Unset):
    """

    id: str
    build_source_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deploys: list[BuildDeploy]
    skipped_services: list[BuildSkippedService]
    build_run: BuildRun | Unset = UNSET
    image: SchemasImage | Unset = UNSET
    assets_deleted_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        build_source_id = self.build_source_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        deploys = []
        for deploys_item_data in self.deploys:
            deploys_item = deploys_item_data.to_dict()
            deploys.append(deploys_item)

        skipped_services = []
        for skipped_services_item_data in self.skipped_services:
            skipped_services_item = skipped_services_item_data.to_dict()
            skipped_services.append(skipped_services_item)

        build_run: dict[str, Any] | Unset = UNSET
        if not isinstance(self.build_run, Unset):
            build_run = self.build_run.to_dict()

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        assets_deleted_at: str | Unset = UNSET
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
                "deploys": deploys,
                "skippedServices": skipped_services,
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
        from ..models.build_deploy import BuildDeploy  # noqa: PLC0415
        from ..models.build_run import BuildRun  # noqa: PLC0415
        from ..models.build_skipped_service import BuildSkippedService  # noqa: PLC0415
        from ..models.schemas_image import SchemasImage  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        build_source_id = d.pop("buildSourceId")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        deploys = []
        _deploys = d.pop("deploys")
        for deploys_item_data in _deploys:
            deploys_item = BuildDeploy.from_dict(deploys_item_data)

            deploys.append(deploys_item)

        skipped_services = []
        _skipped_services = d.pop("skippedServices")
        for skipped_services_item_data in _skipped_services:
            skipped_services_item = BuildSkippedService.from_dict(skipped_services_item_data)

            skipped_services.append(skipped_services_item)

        _build_run = d.pop("buildRun", UNSET)
        build_run: BuildRun | Unset
        if isinstance(_build_run, Unset):
            build_run = UNSET
        else:
            build_run = BuildRun.from_dict(_build_run)

        _image = d.pop("image", UNSET)
        image: SchemasImage | Unset
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = SchemasImage.from_dict(_image)

        _assets_deleted_at = d.pop("assetsDeletedAt", UNSET)
        assets_deleted_at: datetime.datetime | Unset
        if isinstance(_assets_deleted_at, Unset):
            assets_deleted_at = UNSET
        else:
            assets_deleted_at = datetime.datetime.fromisoformat(_assets_deleted_at)

        build_with_deploys = cls(
            id=id,
            build_source_id=build_source_id,
            created_at=created_at,
            updated_at=updated_at,
            deploys=deploys,
            skipped_services=skipped_services,
            build_run=build_run,
            image=image,
            assets_deleted_at=assets_deleted_at,
        )

        build_with_deploys.additional_properties = d
        return build_with_deploys

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
