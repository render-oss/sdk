import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SandboxConnectResponse")


@_attrs_define
class SandboxConnectResponse:
    """A minted connect token and the sandbox-proxy endpoint to invoke with it.
    Send the request (and body, where the operation takes one) to `uri`
    using `method`, with `token` as a bearer credential.

        Attributes:
            execution_id (str): Identifier for this execution. Example: exe-abc123.
            token (str): Short-lived bearer token authorizing exactly this operation against the sandbox.
            uri (str): The sandbox-proxy endpoint to invoke. Example: https://sbx-
                abc123.oregon.sandbox.onrender.com/runs/stream.
            method (str): HTTP method to use against `uri`. Example: POST.
            expires_at (datetime.datetime): When `token` stops being valid. Start the run before this time. Example:
                2026-07-10T12:00:00Z.
    """

    execution_id: str
    token: str
    uri: str
    method: str
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        token = self.token

        uri = self.uri

        method = self.method

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "executionId": execution_id,
                "token": token,
                "uri": uri,
                "method": method,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_id = d.pop("executionId")

        token = d.pop("token")

        uri = d.pop("uri")

        method = d.pop("method")

        expires_at = isoparse(d.pop("expiresAt"))

        sandbox_connect_response = cls(
            execution_id=execution_id,
            token=token,
            uri=uri,
            method=method,
            expires_at=expires_at,
        )

        sandbox_connect_response.additional_properties = d
        return sandbox_connect_response

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
