from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.team_member_status import TeamMemberStatus

T = TypeVar("T", bound="TeamMember")


@_attrs_define
class TeamMember:
    """
    Attributes:
        user_id (str):
        name (str):
        email (str):
        status (TeamMemberStatus):
        role (str):
        mfa_enabled (bool):
    """

    user_id: str
    name: str
    email: str
    status: TeamMemberStatus
    role: str
    mfa_enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        name = self.name

        email = self.email

        status = self.status.value

        role = self.role

        mfa_enabled = self.mfa_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userId": user_id,
                "name": name,
                "email": email,
                "status": status,
                "role": role,
                "mfaEnabled": mfa_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("userId")

        name = d.pop("name")

        email = d.pop("email")

        status = TeamMemberStatus(d.pop("status"))

        role = d.pop("role")

        mfa_enabled = d.pop("mfaEnabled")

        team_member = cls(
            user_id=user_id,
            name=name,
            email=email,
            status=status,
            role=role,
            mfa_enabled=mfa_enabled,
        )

        team_member.additional_properties = d
        return team_member

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
