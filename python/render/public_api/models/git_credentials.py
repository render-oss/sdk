import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="GitCredentials")


@_attrs_define
class GitCredentials:
    """
    Attributes:
        username (str): The HTTP Basic username to send with the token Example: x-access-token.
        token (str): A short-lived token for this repo only
        expires_at (datetime.datetime):
        write (bool): Whether the token can push
        remote_url (str):  Example: https://code.render.com/tea-cph1rs3idesc73a2b2mg/bookmarks.git.
    """

    username: str
    token: str
    expires_at: datetime.datetime
    write: bool
    remote_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        token = self.token

        expires_at = self.expires_at.isoformat()

        write = self.write

        remote_url = self.remote_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "token": token,
                "expiresAt": expires_at,
                "write": write,
                "remoteUrl": remote_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        token = d.pop("token")

        expires_at = isoparse(d.pop("expiresAt"))

        write = d.pop("write")

        remote_url = d.pop("remoteUrl")

        git_credentials = cls(
            username=username,
            token=token,
            expires_at=expires_at,
            write=write,
            remote_url=remote_url,
        )

        git_credentials.additional_properties = d
        return git_credentials

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
