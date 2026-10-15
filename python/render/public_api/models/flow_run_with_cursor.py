from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.flow_run import FlowRun


T = TypeVar("T", bound="FlowRunWithCursor")


@_attrs_define
class FlowRunWithCursor:
    """
    Attributes:
        flow_run (FlowRun):
        cursor (str):
    """

    flow_run: "FlowRun"
    cursor: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flow_run = self.flow_run.to_dict()

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flowRun": flow_run,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_run import FlowRun

        d = dict(src_dict)
        flow_run = FlowRun.from_dict(d.pop("flowRun"))

        cursor = d.pop("cursor")

        flow_run_with_cursor = cls(
            flow_run=flow_run,
            cursor=cursor,
        )

        flow_run_with_cursor.additional_properties = d
        return flow_run_with_cursor

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
