from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresClusterLeaderChanged")


@_attrs_define
class PostgresClusterLeaderChanged:
    """
    Attributes:
        leader_id (Union[Unset, str]):
    """

    leader_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        leader_id = self.leader_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if leader_id is not UNSET:
            field_dict["leaderId"] = leader_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        leader_id = d.pop("leaderId", UNSET)

        postgres_cluster_leader_changed = cls(
            leader_id=leader_id,
        )

        postgres_cluster_leader_changed.additional_properties = d
        return postgres_cluster_leader_changed

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
