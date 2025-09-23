from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NativeEnvironmentDetailsPOST")


@_attrs_define
class NativeEnvironmentDetailsPOST:
    """Fields for native environment (runtime) services

    Attributes:
        build_command (str):
        start_command (str):
    """

    build_command: str
    start_command: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        start_command = self.start_command

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buildCommand": build_command,
                "startCommand": start_command,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        build_command = d.pop("buildCommand")

        start_command = d.pop("startCommand")

        native_environment_details_post = cls(
            build_command=build_command,
            start_command=start_command,
        )

        native_environment_details_post.additional_properties = d
        return native_environment_details_post

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
