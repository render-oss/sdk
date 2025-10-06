from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.previews_generation import PreviewsGeneration
from ..types import UNSET, Unset

T = TypeVar("T", bound="Previews")


@_attrs_define
class Previews:
    """
    Attributes:
        generation (Union[Unset, PreviewsGeneration]): Defaults to "off" Default: PreviewsGeneration.OFF.
    """

    generation: Union[Unset, PreviewsGeneration] = PreviewsGeneration.OFF
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        generation: Union[Unset, str] = UNSET
        if not isinstance(self.generation, Unset):
            generation = self.generation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if generation is not UNSET:
            field_dict["generation"] = generation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _generation = d.pop("generation", UNSET)
        generation: Union[Unset, PreviewsGeneration]
        if isinstance(_generation, Unset):
            generation = UNSET
        else:
            generation = PreviewsGeneration(_generation)

        previews = cls(
            generation=generation,
        )

        previews.additional_properties = d
        return previews

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
