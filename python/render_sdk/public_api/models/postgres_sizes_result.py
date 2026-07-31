from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_size import PostgresSize


T = TypeVar("T", bound="PostgresSizesResult")


@_attrs_define
class PostgresSizesResult:
    """
    Attributes:
        sizes (list['PostgresSize']):
    """

    sizes: list["PostgresSize"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sizes = []
        for sizes_item_data in self.sizes:
            sizes_item = sizes_item_data.to_dict()
            sizes.append(sizes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sizes": sizes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_size import PostgresSize

        d = dict(src_dict)
        sizes = []
        _sizes = d.pop("sizes")
        for sizes_item_data in _sizes:
            sizes_item = PostgresSize.from_dict(sizes_item_data)

            sizes.append(sizes_item)

        postgres_sizes_result = cls(
            sizes=sizes,
        )

        postgres_sizes_result.additional_properties = d
        return postgres_sizes_result

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
