from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NativeEnvironmentDetailsPATCH")


@_attrs_define
class NativeEnvironmentDetailsPATCH:
    """
    Attributes:
        build_command (Union[Unset, str]):
        start_command (Union[Unset, str]):
    """

    build_command: Union[Unset, str] = UNSET
    start_command: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        start_command = self.start_command

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if build_command is not UNSET:
            field_dict["buildCommand"] = build_command
        if start_command is not UNSET:
            field_dict["startCommand"] = start_command

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        build_command = d.pop("buildCommand", UNSET)

        start_command = d.pop("startCommand", UNSET)

        native_environment_details_patch = cls(
            build_command=build_command,
            start_command=start_command,
        )

        native_environment_details_patch.additional_properties = d
        return native_environment_details_patch

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
