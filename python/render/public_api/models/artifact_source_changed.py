from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactSourceChanged")


@_attrs_define
class ArtifactSourceChanged:
    """
    Attributes:
        from_build_source_id (Union[Unset, str]): The previously linked build source. Absent when the service was newly
            attached.
        to_build_source_id (Union[Unset, str]): The newly linked build source. Absent when the service was detached.
    """

    from_build_source_id: Union[Unset, str] = UNSET
    to_build_source_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_build_source_id = self.from_build_source_id

        to_build_source_id = self.to_build_source_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if from_build_source_id is not UNSET:
            field_dict["fromBuildSourceId"] = from_build_source_id
        if to_build_source_id is not UNSET:
            field_dict["toBuildSourceId"] = to_build_source_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_build_source_id = d.pop("fromBuildSourceId", UNSET)

        to_build_source_id = d.pop("toBuildSourceId", UNSET)

        artifact_source_changed = cls(
            from_build_source_id=from_build_source_id,
            to_build_source_id=to_build_source_id,
        )

        artifact_source_changed.additional_properties = d
        return artifact_source_changed

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
