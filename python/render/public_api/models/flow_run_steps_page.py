from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_run_step import FlowRunStep


T = TypeVar("T", bound="FlowRunStepsPage")


@_attrs_define
class FlowRunStepsPage:
    """
    Attributes:
        steps (list['FlowRunStep']):
        has_more (bool): Whether another page of steps follows this one.
        cursor (Union[Unset, str]): Pass as the `cursor` query parameter to fetch the next page. Absent on the last
            page.
    """

    steps: list["FlowRunStep"]
    has_more: bool
    cursor: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        has_more = self.has_more

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "steps": steps,
                "hasMore": has_more,
            }
        )
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_run_step import FlowRunStep

        d = dict(src_dict)
        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = FlowRunStep.from_dict(steps_item_data)

            steps.append(steps_item)

        has_more = d.pop("hasMore")

        cursor = d.pop("cursor", UNSET)

        flow_run_steps_page = cls(
            steps=steps,
            has_more=has_more,
            cursor=cursor,
        )

        flow_run_steps_page.additional_properties = d
        return flow_run_steps_page

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
