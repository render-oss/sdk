from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.audit_log_actor_type import AuditLogActorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditLogActor")


@_attrs_define
class AuditLogActor:
    """
    Attributes:
        type_ (AuditLogActorType): The type of actor that performed the action Example: user.
        email (Union[Unset, str]): Email address of the actor (if applicable) Example: user@example.com.
        id (Union[Unset, str]): Unique identifier of the actor (if applicable) Example: usr-123456789.
    """

    type_: AuditLogActorType
    email: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        email = self.email

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = AuditLogActorType(d.pop("type"))

        email = d.pop("email", UNSET)

        id = d.pop("id", UNSET)

        audit_log_actor = cls(
            type_=type_,
            email=email,
            id=id,
        )

        audit_log_actor.additional_properties = d
        return audit_log_actor

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
