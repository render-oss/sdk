from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.failure_reason import FailureReason


T = TypeVar("T", bound="ServerFailed")


@_attrs_define
class ServerFailed:
    """
    Attributes:
        instance_id (Union[Unset, str]):  Example: srv-d0cjkelq67qs70c2pugg-sbpkm.
        reason (Union[Unset, FailureReason]):
    """

    instance_id: Union[Unset, str] = UNSET
    reason: Union[Unset, "FailureReason"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instance_id = self.instance_id

        reason: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instance_id is not UNSET:
            field_dict["instanceID"] = instance_id
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.failure_reason import FailureReason

        d = dict(src_dict)
        instance_id = d.pop("instanceID", UNSET)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, FailureReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = FailureReason.from_dict(_reason)

        server_failed = cls(
            instance_id=instance_id,
            reason=reason,
        )

        server_failed.additional_properties = d
        return server_failed

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
