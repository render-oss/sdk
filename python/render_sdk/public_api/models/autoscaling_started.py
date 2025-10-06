from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoscalingStarted")


@_attrs_define
class AutoscalingStarted:
    """
    Attributes:
        from_instances (int):
        to_instances (int):
        current_cpu (Union[Unset, int]):
        target_cpu (Union[Unset, int]):
        current_memory (Union[Unset, int]):
        target_memory (Union[Unset, int]):
    """

    from_instances: int
    to_instances: int
    current_cpu: Union[Unset, int] = UNSET
    target_cpu: Union[Unset, int] = UNSET
    current_memory: Union[Unset, int] = UNSET
    target_memory: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_instances = self.from_instances

        to_instances = self.to_instances

        current_cpu = self.current_cpu

        target_cpu = self.target_cpu

        current_memory = self.current_memory

        target_memory = self.target_memory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromInstances": from_instances,
                "toInstances": to_instances,
            }
        )
        if current_cpu is not UNSET:
            field_dict["currentCPU"] = current_cpu
        if target_cpu is not UNSET:
            field_dict["targetCPU"] = target_cpu
        if current_memory is not UNSET:
            field_dict["currentMemory"] = current_memory
        if target_memory is not UNSET:
            field_dict["targetMemory"] = target_memory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_instances = d.pop("fromInstances")

        to_instances = d.pop("toInstances")

        current_cpu = d.pop("currentCPU", UNSET)

        target_cpu = d.pop("targetCPU", UNSET)

        current_memory = d.pop("currentMemory", UNSET)

        target_memory = d.pop("targetMemory", UNSET)

        autoscaling_started = cls(
            from_instances=from_instances,
            to_instances=to_instances,
            current_cpu=current_cpu,
            target_cpu=target_cpu,
            current_memory=current_memory,
            target_memory=target_memory,
        )

        autoscaling_started.additional_properties = d
        return autoscaling_started

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
