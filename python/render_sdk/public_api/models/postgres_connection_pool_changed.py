from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="PostgresConnectionPoolChanged")


@_attrs_define
class PostgresConnectionPoolChanged:
    """
    Attributes:
        from_ (str):
        to (str):
        user (Union[Unset, SchemasUser]): User who triggered the action
    """

    from_: str
    to: str
    user: Union[Unset, "SchemasUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_

        to = self.to

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_user import SchemasUser

        d = dict(src_dict)
        from_ = d.pop("from")

        to = d.pop("to")

        _user = d.pop("user", UNSET)
        user: Union[Unset, SchemasUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = SchemasUser.from_dict(_user)

        postgres_connection_pool_changed = cls(
            from_=from_,
            to=to,
            user=user,
        )

        postgres_connection_pool_changed.additional_properties = d
        return postgres_connection_pool_changed

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
