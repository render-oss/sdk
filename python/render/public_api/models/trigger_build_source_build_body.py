from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_clear_cache import BuildClearCache
from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerBuildSourceBuildBody")


@_attrs_define
class TriggerBuildSourceBuildBody:
    """
    Attributes:
        clear_cache (Union[Unset, BuildClearCache]): If `clear`, Render clears the build source's build cache before
            building. This can be useful if you're experiencing issues with your build.
    """

    clear_cache: Union[Unset, BuildClearCache] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clear_cache: Union[Unset, str] = UNSET
        if not isinstance(self.clear_cache, Unset):
            clear_cache = self.clear_cache.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clear_cache is not UNSET:
            field_dict["clearCache"] = clear_cache

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _clear_cache = d.pop("clearCache", UNSET)
        clear_cache: Union[Unset, BuildClearCache]
        if isinstance(_clear_cache, Unset):
            clear_cache = UNSET
        else:
            clear_cache = BuildClearCache(_clear_cache)

        trigger_build_source_build_body = cls(
            clear_cache=clear_cache,
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
