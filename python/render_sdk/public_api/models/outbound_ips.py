from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.outbound_ips_type import OutboundIpsType
from ..types import UNSET, Unset

T = TypeVar("T", bound="OutboundIps")


@_attrs_define
class OutboundIps:
    """
    Attributes:
        type_ (OutboundIpsType): `dedicated` if a dedicated IP set applies to the resource, `shared` if its traffic
            originates from the shared Render IPs for its region.
        ips (list[str]): The IP addresses the resource's outbound traffic originates from.
        dedicated_ip_id (Union[Unset, str]): The dedicated IP set the traffic originates from. Only present when `type`
            is `dedicated`. Example: egs-abc123.
    """

    type_: OutboundIpsType
    ips: list[str]
    dedicated_ip_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        ips = self.ips

        dedicated_ip_id = self.dedicated_ip_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "ips": ips,
            }
        )
        if dedicated_ip_id is not UNSET:
            field_dict["dedicatedIpId"] = dedicated_ip_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = OutboundIpsType(d.pop("type"))

        ips = cast(list[str], d.pop("ips"))

        dedicated_ip_id = d.pop("dedicatedIpId", UNSET)

        outbound_ips = cls(
            type_=type_,
            ips=ips,
            dedicated_ip_id=dedicated_ip_id,
        )

        outbound_ips.additional_properties = d
        return outbound_ips

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
