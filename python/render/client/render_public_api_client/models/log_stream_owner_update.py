from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_stream_preview_setting import LogStreamPreviewSetting
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogStreamOwnerUpdate")


@_attrs_define
class LogStreamOwnerUpdate:
    """
    Attributes:
        preview (LogStreamPreviewSetting): Whether to send logs or drop them.
        endpoint (Union[Unset, str]): The endpoint to stream logs to.
        token (Union[Unset, str]): The optional token to authenticate the log stream.
    """

    preview: LogStreamPreviewSetting
    endpoint: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        preview = self.preview.value

        endpoint = self.endpoint

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "preview": preview,
            }
        )
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        preview = LogStreamPreviewSetting(d.pop("preview"))

        endpoint = d.pop("endpoint", UNSET)

        token = d.pop("token", UNSET)

        log_stream_owner_update = cls(
            preview=preview,
            endpoint=endpoint,
            token=token,
        )

        log_stream_owner_update.additional_properties = d
        return log_stream_owner_update

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
