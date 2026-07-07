from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.artifact_source import ArtifactSource


T = TypeVar("T", bound="ArtifactSourceWithCursor")


@_attrs_define
class ArtifactSourceWithCursor:
    """
    Attributes:
        artifact_source (ArtifactSource):
        cursor (str):
    """

    artifact_source: "ArtifactSource"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        artifact_source = self.artifact_source.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifactSource": artifact_source,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_source import ArtifactSource

        d = dict(src_dict)
        artifact_source = ArtifactSource.from_dict(d.pop("artifactSource"))

        cursor = d.pop("cursor")

        artifact_source_with_cursor = cls(
            artifact_source=artifact_source,
            cursor=cursor,
        )

        artifact_source_with_cursor.additional_properties = d
        return artifact_source_with_cursor

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
