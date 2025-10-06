from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlueprintPATCH")


@_attrs_define
class BlueprintPATCH:
    """
    Attributes:
        name (Union[Unset, str]):
        auto_sync (Union[Unset, bool]): Automatically sync changes to render.yaml
    """

    name: Union[Unset, str] = UNSET
    auto_sync: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        auto_sync = self.auto_sync

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if auto_sync is not UNSET:
            field_dict["autoSync"] = auto_sync

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        auto_sync = d.pop("autoSync", UNSET)

        blueprint_patch = cls(
            name=name,
            auto_sync=auto_sync,
        )

        blueprint_patch.additional_properties = d
        return blueprint_patch

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
