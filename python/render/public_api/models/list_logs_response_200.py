import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.log import Log


T = TypeVar("T", bound="ListLogsResponse200")


@_attrs_define
class ListLogsResponse200:
    """A run of a cron job

    Attributes:
        has_more (bool): Ture if there are more logs to fetch
        next_start_time (datetime.datetime): The start time to use in the next query to fetch the next set of logs
            Example: 2021-07-15T07:20:05.777035-07:00.
        next_end_time (datetime.datetime): The end time to use in the next query to fetch the next set of logs Example:
            2021-07-15T07:20:05.777035-07:00.
        logs (list['Log']):
    """

    has_more: bool
    next_start_time: datetime.datetime
    next_end_time: datetime.datetime
    logs: list["Log"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_more = self.has_more

        next_start_time = self.next_start_time.isoformat()

        next_end_time = self.next_end_time.isoformat()

        logs = []
        for logs_item_data in self.logs:
            logs_item = logs_item_data.to_dict()
            logs.append(logs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hasMore": has_more,
                "nextStartTime": next_start_time,
                "nextEndTime": next_end_time,
                "logs": logs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log import Log

        d = dict(src_dict)
        has_more = d.pop("hasMore")

        next_start_time = isoparse(d.pop("nextStartTime"))

        next_end_time = isoparse(d.pop("nextEndTime"))

        logs = []
        _logs = d.pop("logs")
        for logs_item_data in _logs:
            logs_item = Log.from_dict(logs_item_data)

            logs.append(logs_item)

        list_logs_response_200 = cls(
            has_more=has_more,
            next_start_time=next_start_time,
            next_end_time=next_end_time,
            logs=logs,
        )

        list_logs_response_200.additional_properties = d
        return list_logs_response_200

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
