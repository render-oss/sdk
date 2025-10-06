from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan import Plan
from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewInput")


@_attrs_define
class PreviewInput:
    """
    Attributes:
        image_path (str): Must be either a full URL or the relative path to an image. If a relative path, Render uses
            the base service's image URL as its root. For example, if the base service's image URL is
            `docker.io/library/nginx:latest`, then valid values are: `docker.io/library/nginx:<any tag or SHA>`,
            `library/nginx:<any tag or SHA>`, or `nginx:<any tag or SHA>`. Note that the path must match (only the tag or
            SHA can vary). Example: docker.io/library/nginx:latest.
        name (Union[Unset, str]): A name for the service preview instance. If not specified, Render generates the name
            using the base service's name and the specified tag or SHA. Example: preview.
        plan (Union[Unset, Plan]): The instance type to use for the preview instance. Note that base services with any
            paid instance type can't create preview instances with the `free` instance type. Example: starter.
    """

    image_path: str
    name: Union[Unset, str] = UNSET
    plan: Union[Unset, Plan] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_path = self.image_path

        name = self.name

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imagePath": image_path,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_path = d.pop("imagePath")

        name = d.pop("name", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, Plan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = Plan(_plan)

        preview_input = cls(
            image_path=image_path,
            name=name,
            plan=plan,
        )

        preview_input.additional_properties = d
        return preview_input

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
