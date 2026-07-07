import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sandbox_file_entry_type import SandboxFileEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxFileEntry")


@_attrs_define
class SandboxFileEntry:
    """A file or directory entry in a sandbox filesystem listing.

    Attributes:
        name (str): File or directory name (basename, not full path). Example: main.py.
        type_ (SandboxFileEntryType): Entry type.
        size (int): Size in bytes. 0 for directories and symlinks. Example: 2048.
        modified_at (datetime.datetime): Last-modified timestamp.
        target (Union[Unset, str]): Symlink target path. Present only when type is `symlink`.
    """

    name: str
    type_: SandboxFileEntryType
    size: int
    modified_at: datetime.datetime
    target: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        size = self.size

        modified_at = self.modified_at.isoformat()

        target = self.target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "size": size,
                "modifiedAt": modified_at,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = SandboxFileEntryType(d.pop("type"))

        size = d.pop("size")

        modified_at = isoparse(d.pop("modifiedAt"))

        target = d.pop("target", UNSET)

        sandbox_file_entry = cls(
            name=name,
            type_=type_,
            size=size,
            modified_at=modified_at,
            target=target,
        )

        sandbox_file_entry.additional_properties = d
        return sandbox_file_entry

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
