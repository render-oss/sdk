from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.build_source import BuildSource


T = TypeVar("T", bound="BuildSourceWithCursor")


@_attrs_define
class BuildSourceWithCursor:
    """
    Attributes:
        build_source (BuildSource):
        cursor (str):
    """

    build_source: "BuildSource"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_source = self.build_source.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buildSource": build_source,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_source import BuildSource

        d = dict(src_dict)
        build_source = BuildSource.from_dict(d.pop("buildSource"))

        cursor = d.pop("cursor")

        build_source_with_cursor = cls(
            build_source=build_source,
            cursor=cursor,
        )

        build_source_with_cursor.additional_properties = d
        return build_source_with_cursor

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
