from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.autoscaling_criteria_percentage import AutoscalingCriteriaPercentage


T = TypeVar("T", bound="AutoscalingCriteria")


@_attrs_define
class AutoscalingCriteria:
    """
    Attributes:
        cpu (AutoscalingCriteriaPercentage):
        memory (AutoscalingCriteriaPercentage):
    """

    cpu: "AutoscalingCriteriaPercentage"
    memory: "AutoscalingCriteriaPercentage"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu = self.cpu.to_dict()

        memory = self.memory.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu": cpu,
                "memory": memory,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_criteria_percentage import AutoscalingCriteriaPercentage

        d = dict(src_dict)
        cpu = AutoscalingCriteriaPercentage.from_dict(d.pop("cpu"))

        memory = AutoscalingCriteriaPercentage.from_dict(d.pop("memory"))

        autoscaling_criteria = cls(
            cpu=cpu,
            memory=memory,
        )

        autoscaling_criteria.additional_properties = d
        return autoscaling_criteria

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
