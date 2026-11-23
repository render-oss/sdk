from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_clear_cache import BuildClearCache
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_deploy_input import BuildDeployInput


T = TypeVar("T", bound="TriggerBuildSourceBuildBody")


@_attrs_define
class TriggerBuildSourceBuildBody:
    """
    Attributes:
        clear_cache (BuildClearCache | Unset): If `clear`, Render clears the build source's build cache before building.
            This can be useful if you're experiencing issues with your build.
        deploy (BuildDeployInput | Unset):
    """

    clear_cache: BuildClearCache | Unset = UNSET
    deploy: BuildDeployInput | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clear_cache: str | Unset = UNSET
        if not isinstance(self.clear_cache, Unset):
            clear_cache = self.clear_cache.value

        deploy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deploy, Unset):
            deploy = self.deploy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clear_cache is not UNSET:
            field_dict["clearCache"] = clear_cache
        if deploy is not UNSET:
            field_dict["deploy"] = deploy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_deploy_input import BuildDeployInput  # noqa: PLC0415

        d = dict(src_dict)
        _clear_cache = d.pop("clearCache", UNSET)
        clear_cache: BuildClearCache | Unset
        if isinstance(_clear_cache, Unset):
            clear_cache = UNSET
        else:
            clear_cache = BuildClearCache(_clear_cache)

        _deploy = d.pop("deploy", UNSET)
        deploy: BuildDeployInput | Unset
        if isinstance(_deploy, Unset):
            deploy = UNSET
        else:
            deploy = BuildDeployInput.from_dict(_deploy)

        trigger_build_source_build_body = cls(
            clear_cache=clear_cache,
            deploy=deploy,
        )

        trigger_build_source_build_body.additional_properties = d
        return trigger_build_source_build_body

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
