from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresQueryStatistic")


@_attrs_define
class PostgresQueryStatistic:
    """A single query from pg_stat_statements.

    Attributes:
        query_id (Union[Unset, str]):
        query (Union[Unset, str]):
        calls (Union[Unset, int]):
        total_time_ms (Union[Unset, float]):
        min_time_ms (Union[Unset, float]):
        max_time_ms (Union[Unset, float]):
        mean_time_ms (Union[Unset, float]):
        stddev_time_ms (Union[Unset, float]):
        rows (Union[Unset, int]):
        shared_blocks_hit (Union[Unset, int]):
        shared_blocks_read (Union[Unset, int]):
        shared_blocks_dirtied (Union[Unset, int]):
        shared_blocks_written (Union[Unset, int]):
        local_blocks_hit (Union[Unset, int]):
        local_blocks_read (Union[Unset, int]):
        local_blocks_dirtied (Union[Unset, int]):
        local_blocks_written (Union[Unset, int]):
        temp_blocks_read (Union[Unset, int]):
        temp_blocks_written (Union[Unset, int]):
    """

    query_id: Union[Unset, str] = UNSET
    query: Union[Unset, str] = UNSET
    calls: Union[Unset, int] = UNSET
    total_time_ms: Union[Unset, float] = UNSET
    min_time_ms: Union[Unset, float] = UNSET
    max_time_ms: Union[Unset, float] = UNSET
    mean_time_ms: Union[Unset, float] = UNSET
    stddev_time_ms: Union[Unset, float] = UNSET
    rows: Union[Unset, int] = UNSET
    shared_blocks_hit: Union[Unset, int] = UNSET
    shared_blocks_read: Union[Unset, int] = UNSET
    shared_blocks_dirtied: Union[Unset, int] = UNSET
    shared_blocks_written: Union[Unset, int] = UNSET
    local_blocks_hit: Union[Unset, int] = UNSET
    local_blocks_read: Union[Unset, int] = UNSET
    local_blocks_dirtied: Union[Unset, int] = UNSET
    local_blocks_written: Union[Unset, int] = UNSET
    temp_blocks_read: Union[Unset, int] = UNSET
    temp_blocks_written: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_id = self.query_id

        query = self.query

        calls = self.calls

        total_time_ms = self.total_time_ms

        min_time_ms = self.min_time_ms

        max_time_ms = self.max_time_ms

        mean_time_ms = self.mean_time_ms

        stddev_time_ms = self.stddev_time_ms

        rows = self.rows

        shared_blocks_hit = self.shared_blocks_hit

        shared_blocks_read = self.shared_blocks_read

        shared_blocks_dirtied = self.shared_blocks_dirtied

        shared_blocks_written = self.shared_blocks_written

        local_blocks_hit = self.local_blocks_hit

        local_blocks_read = self.local_blocks_read

        local_blocks_dirtied = self.local_blocks_dirtied

        local_blocks_written = self.local_blocks_written

        temp_blocks_read = self.temp_blocks_read

        temp_blocks_written = self.temp_blocks_written

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_id is not UNSET:
            field_dict["queryId"] = query_id
        if query is not UNSET:
            field_dict["query"] = query
        if calls is not UNSET:
            field_dict["calls"] = calls
        if total_time_ms is not UNSET:
            field_dict["totalTimeMs"] = total_time_ms
        if min_time_ms is not UNSET:
            field_dict["minTimeMs"] = min_time_ms
        if max_time_ms is not UNSET:
            field_dict["maxTimeMs"] = max_time_ms
        if mean_time_ms is not UNSET:
            field_dict["meanTimeMs"] = mean_time_ms
        if stddev_time_ms is not UNSET:
            field_dict["stddevTimeMs"] = stddev_time_ms
        if rows is not UNSET:
            field_dict["rows"] = rows
        if shared_blocks_hit is not UNSET:
            field_dict["sharedBlocksHit"] = shared_blocks_hit
        if shared_blocks_read is not UNSET:
            field_dict["sharedBlocksRead"] = shared_blocks_read
        if shared_blocks_dirtied is not UNSET:
            field_dict["sharedBlocksDirtied"] = shared_blocks_dirtied
        if shared_blocks_written is not UNSET:
            field_dict["sharedBlocksWritten"] = shared_blocks_written
        if local_blocks_hit is not UNSET:
            field_dict["localBlocksHit"] = local_blocks_hit
        if local_blocks_read is not UNSET:
            field_dict["localBlocksRead"] = local_blocks_read
        if local_blocks_dirtied is not UNSET:
            field_dict["localBlocksDirtied"] = local_blocks_dirtied
        if local_blocks_written is not UNSET:
            field_dict["localBlocksWritten"] = local_blocks_written
        if temp_blocks_read is not UNSET:
            field_dict["tempBlocksRead"] = temp_blocks_read
        if temp_blocks_written is not UNSET:
            field_dict["tempBlocksWritten"] = temp_blocks_written

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query_id = d.pop("queryId", UNSET)

        query = d.pop("query", UNSET)

        calls = d.pop("calls", UNSET)

        total_time_ms = d.pop("totalTimeMs", UNSET)

        min_time_ms = d.pop("minTimeMs", UNSET)

        max_time_ms = d.pop("maxTimeMs", UNSET)

        mean_time_ms = d.pop("meanTimeMs", UNSET)

        stddev_time_ms = d.pop("stddevTimeMs", UNSET)

        rows = d.pop("rows", UNSET)

        shared_blocks_hit = d.pop("sharedBlocksHit", UNSET)

        shared_blocks_read = d.pop("sharedBlocksRead", UNSET)

        shared_blocks_dirtied = d.pop("sharedBlocksDirtied", UNSET)

        shared_blocks_written = d.pop("sharedBlocksWritten", UNSET)

        local_blocks_hit = d.pop("localBlocksHit", UNSET)

        local_blocks_read = d.pop("localBlocksRead", UNSET)

        local_blocks_dirtied = d.pop("localBlocksDirtied", UNSET)

        local_blocks_written = d.pop("localBlocksWritten", UNSET)

        temp_blocks_read = d.pop("tempBlocksRead", UNSET)

        temp_blocks_written = d.pop("tempBlocksWritten", UNSET)

        postgres_query_statistic = cls(
            query_id=query_id,
            query=query,
            calls=calls,
            total_time_ms=total_time_ms,
            min_time_ms=min_time_ms,
            max_time_ms=max_time_ms,
            mean_time_ms=mean_time_ms,
            stddev_time_ms=stddev_time_ms,
            rows=rows,
            shared_blocks_hit=shared_blocks_hit,
            shared_blocks_read=shared_blocks_read,
            shared_blocks_dirtied=shared_blocks_dirtied,
            shared_blocks_written=shared_blocks_written,
            local_blocks_hit=local_blocks_hit,
            local_blocks_read=local_blocks_read,
            local_blocks_dirtied=local_blocks_dirtied,
            local_blocks_written=local_blocks_written,
            temp_blocks_read=temp_blocks_read,
            temp_blocks_written=temp_blocks_written,
        )

        postgres_query_statistic.additional_properties = d
        return postgres_query_statistic

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
