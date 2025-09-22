from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServerRestarted")


@_attrs_define
class ServerRestarted:
    """
    Attributes:
        triggered_by_user (Union[None, str]):
    """

    triggered_by_user: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        triggered_by_user: Union[None, str]
        triggered_by_user = self.triggered_by_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "triggeredByUser": triggered_by_user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_triggered_by_user(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        triggered_by_user = _parse_triggered_by_user(d.pop("triggeredByUser"))

        server_restarted = cls(
            triggered_by_user=triggered_by_user,
        )

        server_restarted.additional_properties = d
        return server_restarted

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
