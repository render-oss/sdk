from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AutoscalingCriteriaPercentage")


@_attrs_define
class AutoscalingCriteriaPercentage:
    """
    Attributes:
        enabled (bool):  Default: False.
        percentage (int): Determines when your service will be scaled. If the average resource utilization is
            significantly above/below the target, we will increase/decrease the number of instances.
    """

    percentage: int
    enabled: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        percentage = self.percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "percentage": percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        percentage = d.pop("percentage")

        autoscaling_criteria_percentage = cls(
            enabled=enabled,
            percentage=percentage,
        )

        autoscaling_criteria_percentage.additional_properties = d
        return autoscaling_criteria_percentage

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
