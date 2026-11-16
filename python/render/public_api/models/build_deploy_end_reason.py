from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_deploy_end_reason_id import BuildDeployEndReasonID
    from ..models.failure_reason import FailureReason


T = TypeVar("T", bound="BuildDeployEndReason")


@_attrs_define
class BuildDeployEndReason:
    """
    Attributes:
        build_failed (BuildDeployEndReasonID | Unset):
        new_build (BuildDeployEndReasonID | Unset):
        new_deploy (BuildDeployEndReasonID | Unset):
        failure (FailureReason | Unset):
    """

    build_failed: BuildDeployEndReasonID | Unset = UNSET
    new_build: BuildDeployEndReasonID | Unset = UNSET
    new_deploy: BuildDeployEndReasonID | Unset = UNSET
    failure: FailureReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_failed: dict[str, Any] | Unset = UNSET
        if not isinstance(self.build_failed, Unset):
            build_failed = self.build_failed.to_dict()

        new_build: dict[str, Any] | Unset = UNSET
        if not isinstance(self.new_build, Unset):
            new_build = self.new_build.to_dict()

        new_deploy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.new_deploy, Unset):
            new_deploy = self.new_deploy.to_dict()

        failure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.failure, Unset):
            failure = self.failure.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if build_failed is not UNSET:
            field_dict["buildFailed"] = build_failed
        if new_build is not UNSET:
            field_dict["newBuild"] = new_build
        if new_deploy is not UNSET:
            field_dict["newDeploy"] = new_deploy
        if failure is not UNSET:
            field_dict["failure"] = failure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_deploy_end_reason_id import BuildDeployEndReasonID  # noqa: PLC0415
        from ..models.failure_reason import FailureReason  # noqa: PLC0415

        d = dict(src_dict)
        _build_failed = d.pop("buildFailed", UNSET)
        build_failed: BuildDeployEndReasonID | Unset
        if isinstance(_build_failed, Unset):
            build_failed = UNSET
        else:
            build_failed = BuildDeployEndReasonID.from_dict(_build_failed)

        _new_build = d.pop("newBuild", UNSET)
        new_build: BuildDeployEndReasonID | Unset
        if isinstance(_new_build, Unset):
            new_build = UNSET
        else:
            new_build = BuildDeployEndReasonID.from_dict(_new_build)

        _new_deploy = d.pop("newDeploy", UNSET)
        new_deploy: BuildDeployEndReasonID | Unset
        if isinstance(_new_deploy, Unset):
            new_deploy = UNSET
        else:
            new_deploy = BuildDeployEndReasonID.from_dict(_new_deploy)

        _failure = d.pop("failure", UNSET)
        failure: FailureReason | Unset
        if isinstance(_failure, Unset):
            failure = UNSET
        else:
            failure = FailureReason.from_dict(_failure)

        build_deploy_end_reason = cls(
            build_failed=build_failed,
            new_build=new_build,
            new_deploy=new_deploy,
            failure=failure,
        )

        build_deploy_end_reason.additional_properties = d
        return build_deploy_end_reason

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
