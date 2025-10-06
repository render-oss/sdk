from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_stream_preview_setting import LogStreamPreviewSetting
from ..types import UNSET, Unset

T = TypeVar("T", bound="OwnerLogStreamSetting")


@_attrs_define
class OwnerLogStreamSetting:
    """Owner log stream settings

    Attributes:
        owner_id (Union[Unset, str]): The ID of the owner.
        endpoint (Union[Unset, str]): The endpoint to stream logs to.
        preview (Union[Unset, LogStreamPreviewSetting]): Whether to send logs or drop them.
    """

    owner_id: Union[Unset, str] = UNSET
    endpoint: Union[Unset, str] = UNSET
    preview: Union[Unset, LogStreamPreviewSetting] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        endpoint = self.endpoint

        preview: Union[Unset, str] = UNSET
        if not isinstance(self.preview, Unset):
            preview = self.preview.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if owner_id is not UNSET:
            field_dict["ownerId"] = owner_id
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if preview is not UNSET:
            field_dict["preview"] = preview

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        _preview = d.pop("preview", UNSET)
        preview: Union[Unset, LogStreamPreviewSetting]
        if isinstance(_preview, Unset):
            preview = UNSET
        else:
            preview = LogStreamPreviewSetting(_preview)

        owner_log_stream_setting = cls(
            owner_id=owner_id,
            endpoint=endpoint,
            preview=preview,
        )

        owner_log_stream_setting.additional_properties = d
        return owner_log_stream_setting

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
