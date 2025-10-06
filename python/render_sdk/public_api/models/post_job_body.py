from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostJobBody")


@_attrs_define
class PostJobBody:
    """
    Attributes:
        start_command (str):
        plan_id (Union[Unset, str]):
    """

    start_command: str
    plan_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_command = self.start_command

        plan_id = self.plan_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "startCommand": start_command,
            }
        )
        if plan_id is not UNSET:
            field_dict["planId"] = plan_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_command = d.pop("startCommand")

        plan_id = d.pop("planId", UNSET)

        post_job_body = cls(
            start_command=start_command,
            plan_id=plan_id,
        )

        post_job_body.additional_properties = d
        return post_job_body

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
