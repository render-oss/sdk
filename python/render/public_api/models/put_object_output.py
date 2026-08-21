import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PutObjectOutput")


@_attrs_define
class PutObjectOutput:
    """
    Attributes:
        url (str): Presigned URL for uploading the object Example: https://example-bucket.s3.amazonaws.com/presigned-
            put-url.
        expires_at (datetime.datetime): The time at which the presigned URL expires (ISO 8601 format) Example:
            2024-01-15T12:30:00Z.
        max_size_bytes (int): The maximum size of the object in bytes Example: 1048576.
    """

    url: str
    expires_at: datetime.datetime
    max_size_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        expires_at = self.expires_at.isoformat()

        max_size_bytes = self.max_size_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "expiresAt": expires_at,
                "maxSizeBytes": max_size_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        expires_at = isoparse(d.pop("expiresAt"))

        max_size_bytes = d.pop("maxSizeBytes")

        put_object_output = cls(
            url=url,
            expires_at=expires_at,
            max_size_bytes=max_size_bytes,
        )

        put_object_output.additional_properties = d
        return put_object_output

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
