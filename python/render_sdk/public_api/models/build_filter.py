from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BuildFilter")


@_attrs_define
class BuildFilter:
    """
    Attributes:
        paths (list[str]):
        ignored_paths (list[str]):
    """

    paths: list[str]
    ignored_paths: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        paths = self.paths

        ignored_paths = self.ignored_paths

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paths": paths,
                "ignoredPaths": ignored_paths,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        paths = cast(list[str], d.pop("paths"))

        ignored_paths = cast(list[str], d.pop("ignoredPaths"))

        build_filter = cls(
            paths=paths,
            ignored_paths=ignored_paths,
        )

        build_filter.additional_properties = d
        return build_filter

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
