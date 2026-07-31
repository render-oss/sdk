from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.postgres_query_statistic import PostgresQueryStatistic


T = TypeVar("T", bound="PostgresTopQueriesResult")


@_attrs_define
class PostgresTopQueriesResult:
    """
    Attributes:
        top_queries (list['PostgresQueryStatistic']):
    """

    top_queries: list["PostgresQueryStatistic"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        top_queries = []
        for top_queries_item_data in self.top_queries:
            top_queries_item = top_queries_item_data.to_dict()
            top_queries.append(top_queries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topQueries": top_queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.postgres_query_statistic import PostgresQueryStatistic

        d = dict(src_dict)
        top_queries = []
        _top_queries = d.pop("topQueries")
        for top_queries_item_data in _top_queries:
            top_queries_item = PostgresQueryStatistic.from_dict(top_queries_item_data)

            top_queries.append(top_queries_item)

        postgres_top_queries_result = cls(
            top_queries=top_queries,
        )

        postgres_top_queries_result.additional_properties = d
        return postgres_top_queries_result

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
