import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.log_label import LogLabel


T = TypeVar("T", bound="Log")


@_attrs_define
class Log:
    """A log entry with metadata

    Attributes:
        id (str): A unique ID of the log entry
        message (str): The message of the log entry
        timestamp (datetime.datetime): The timestamp of the log entry
        labels (list['LogLabel']):
    """

    id: str
    message: str
    timestamp: datetime.datetime
    labels: list["LogLabel"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        message = self.message

        timestamp = self.timestamp.isoformat()

        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "message": message,
                "timestamp": timestamp,
                "labels": labels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_label import LogLabel

        d = dict(src_dict)
        id = d.pop("id")

        message = d.pop("message")

        timestamp = isoparse(d.pop("timestamp"))

        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:
            labels_item = LogLabel.from_dict(labels_item_data)

            labels.append(labels_item)

        log = cls(
            id=id,
            message=message,
            timestamp=timestamp,
            labels=labels,
        )

        log.additional_properties = d
        return log

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
