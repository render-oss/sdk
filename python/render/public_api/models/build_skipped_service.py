from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_skipped_service_reason import BuildSkippedServiceReason

T = TypeVar("T", bound="BuildSkippedService")


@_attrs_define
class BuildSkippedService:
    """
    Attributes:
        service_id (str):
        reason (BuildSkippedServiceReason): Why the service did not get a deploy:

            - `suspended`: the service is suspended.
            - `deploys_shut_off`: Render has temporarily paused deploys for the service's plan tier.
    """

    service_id: str
    reason: BuildSkippedServiceReason
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        reason = self.reason.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serviceId": service_id,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("serviceId")

        reason = BuildSkippedServiceReason(d.pop("reason"))

        build_skipped_service = cls(
            service_id=service_id,
            reason=reason,
        )

        build_skipped_service.additional_properties = d
        return build_skipped_service

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
