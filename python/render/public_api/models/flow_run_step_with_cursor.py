from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.flow_run_step import FlowRunStep


T = TypeVar("T", bound="FlowRunStepWithCursor")


@_attrs_define
class FlowRunStepWithCursor:
    """
    Attributes:
        step (FlowRunStep):
        cursor (str):
    """

    step: "FlowRunStep"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step = self.step.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step": step,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_run_step import FlowRunStep

        d = dict(src_dict)
        step = FlowRunStep.from_dict(d.pop("step"))

        cursor = d.pop("cursor")

        flow_run_step_with_cursor = cls(
            step=step,
            cursor=cursor,
        )

        flow_run_step_with_cursor.additional_properties = d
        return flow_run_step_with_cursor

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
