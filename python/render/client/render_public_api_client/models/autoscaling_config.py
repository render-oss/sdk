from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.autoscaling_criteria import AutoscalingCriteria


T = TypeVar("T", bound="AutoscalingConfig")


@_attrs_define
class AutoscalingConfig:
    """
    Attributes:
        enabled (bool):  Default: False.
        min_ (int): The minimum number of instances for the service
        max_ (int): The maximum number of instances for the service
        criteria (AutoscalingCriteria):
    """

    min_: int
    max_: int
    criteria: "AutoscalingCriteria"
    enabled: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        min_ = self.min_

        max_ = self.max_

        criteria = self.criteria.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "min": min_,
                "max": max_,
                "criteria": criteria,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_criteria import AutoscalingCriteria

        d = dict(src_dict)
        enabled = d.pop("enabled")

        min_ = d.pop("min")

        max_ = d.pop("max")

        criteria = AutoscalingCriteria.from_dict(d.pop("criteria"))

        autoscaling_config = cls(
            enabled=enabled,
            min_=min_,
            max_=max_,
            criteria=criteria,
        )

        autoscaling_config.additional_properties = d
        return autoscaling_config

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
