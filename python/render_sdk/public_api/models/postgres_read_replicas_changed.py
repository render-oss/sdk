from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostgresReadReplicasChanged")


@_attrs_define
class PostgresReadReplicasChanged:
    """
    Attributes:
        from_replicas (int):
        to_replicas (int):
    """

    from_replicas: int
    to_replicas: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_replicas = self.from_replicas

        to_replicas = self.to_replicas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromReplicas": from_replicas,
                "toReplicas": to_replicas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_replicas = d.pop("fromReplicas")

        to_replicas = d.pop("toReplicas")

        postgres_read_replicas_changed = cls(
            from_replicas=from_replicas,
            to_replicas=to_replicas,
        )

        postgres_read_replicas_changed.additional_properties = d
        return postgres_read_replicas_changed

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
