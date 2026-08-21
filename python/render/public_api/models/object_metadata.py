import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ObjectMetadata")


@_attrs_define
class ObjectMetadata:
    """
    Attributes:
        key (str): The object's key Example: workflow-data/task-output.json.
        size_bytes (int): Size of the object in bytes Example: 1048576.
        last_modified (datetime.datetime): When the object was last modified (ISO 8601) Example: 2026-01-15T12:30:00Z.
    """

    key: str
    size_bytes: int
    last_modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        size_bytes = self.size_bytes

        last_modified = self.last_modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "sizeBytes": size_bytes,
                "lastModified": last_modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        size_bytes = d.pop("sizeBytes")

        last_modified = isoparse(d.pop("lastModified"))

        object_metadata = cls(
            key=key,
            size_bytes=size_bytes,
            last_modified=last_modified,
        )

        object_metadata.additional_properties = d
        return object_metadata

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
