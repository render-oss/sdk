from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.persistence_mode import PersistenceMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="KeyValueOptions")


@_attrs_define
class KeyValueOptions:
    """Options for a Key Value instance

    Attributes:
        maxmemory_policy (Union[Unset, str]):
        persistence_mode (Union[Unset, PersistenceMode]): The persistence mode for the Key Value instance. The default
            for paid instances is journal_snapshot (both journaling and snapshots). Only turn off persistence if you're
            using this Key Value instance as a cache and are okay with losing data. Free instances do not have persistence.
    """

    maxmemory_policy: Union[Unset, str] = UNSET
    persistence_mode: Union[Unset, PersistenceMode] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        maxmemory_policy = self.maxmemory_policy

        persistence_mode: Union[Unset, str] = UNSET
        if not isinstance(self.persistence_mode, Unset):
            persistence_mode = self.persistence_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if maxmemory_policy is not UNSET:
            field_dict["maxmemoryPolicy"] = maxmemory_policy
        if persistence_mode is not UNSET:
            field_dict["persistenceMode"] = persistence_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        maxmemory_policy = d.pop("maxmemoryPolicy", UNSET)

        _persistence_mode = d.pop("persistenceMode", UNSET)
        persistence_mode: Union[Unset, PersistenceMode]
        if isinstance(_persistence_mode, Unset):
            persistence_mode = UNSET
        else:
            persistence_mode = PersistenceMode(_persistence_mode)

        key_value_options = cls(
            maxmemory_policy=maxmemory_policy,
            persistence_mode=persistence_mode,
        )

        key_value_options.additional_properties = d
        return key_value_options

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
