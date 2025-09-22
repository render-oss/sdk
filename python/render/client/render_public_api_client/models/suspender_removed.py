from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="SuspenderRemoved")


@_attrs_define
class SuspenderRemoved:
    """
    Attributes:
        actor (str):
        resumed_by_user (Union[Unset, SchemasUser]): User who triggered the action
    """

    actor: str
    resumed_by_user: Union[Unset, "SchemasUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actor = self.actor

        resumed_by_user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resumed_by_user, Unset):
            resumed_by_user = self.resumed_by_user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actor": actor,
            }
        )
        if resumed_by_user is not UNSET:
            field_dict["resumedByUser"] = resumed_by_user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_user import SchemasUser

        d = dict(src_dict)
        actor = d.pop("actor")

        _resumed_by_user = d.pop("resumedByUser", UNSET)
        resumed_by_user: Union[Unset, SchemasUser]
        if isinstance(_resumed_by_user, Unset):
            resumed_by_user = UNSET
        else:
            resumed_by_user = SchemasUser.from_dict(_resumed_by_user)

        suspender_removed = cls(
            actor=actor,
            resumed_by_user=resumed_by_user,
        )

        suspender_removed.additional_properties = d
        return suspender_removed

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
