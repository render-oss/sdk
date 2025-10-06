from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_application_values_collection_item_filter import FilterApplicationValuesCollectionItemFilter
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterApplicationValuesCollectionItem")


@_attrs_define
class FilterApplicationValuesCollectionItem:
    """
    Attributes:
        filter_ (Union[Unset, FilterApplicationValuesCollectionItemFilter]):
        values (Union[Unset, list[str]]):
    """

    filter_: Union[Unset, FilterApplicationValuesCollectionItemFilter] = UNSET
    values: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_: Union[Unset, str] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.value

        values: Union[Unset, list[str]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, FilterApplicationValuesCollectionItemFilter]
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = FilterApplicationValuesCollectionItemFilter(_filter_)

        values = cast(list[str], d.pop("values", UNSET))

        filter_application_values_collection_item = cls(
            filter_=filter_,
            values=values,
        )

        filter_application_values_collection_item.additional_properties = d
        return filter_application_values_collection_item

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
