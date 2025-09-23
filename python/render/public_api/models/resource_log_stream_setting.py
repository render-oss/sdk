from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_stream_setting import LogStreamSetting
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceLogStreamSetting")


@_attrs_define
class ResourceLogStreamSetting:
    """Resource log stream overrides

    Attributes:
        resource_id (Union[Unset, str]): The ID of the resource.
        endpoint (Union[Unset, str]): The endpoint to stream logs to. Must be present if setting is send. Cannot be
            present if setting is drop.
        setting (Union[Unset, LogStreamSetting]): Whether to send logs or drop them.
    """

    resource_id: Union[Unset, str] = UNSET
    endpoint: Union[Unset, str] = UNSET
    setting: Union[Unset, LogStreamSetting] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_id = self.resource_id

        endpoint = self.endpoint

        setting: Union[Unset, str] = UNSET
        if not isinstance(self.setting, Unset):
            setting = self.setting.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if setting is not UNSET:
            field_dict["setting"] = setting

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_id = d.pop("resourceId", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        _setting = d.pop("setting", UNSET)
        setting: Union[Unset, LogStreamSetting]
        if isinstance(_setting, Unset):
            setting = UNSET
        else:
            setting = LogStreamSetting(_setting)

        resource_log_stream_setting = cls(
            resource_id=resource_id,
            endpoint=endpoint,
            setting=setting,
        )

        resource_log_stream_setting.additional_properties = d
        return resource_log_stream_setting

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
