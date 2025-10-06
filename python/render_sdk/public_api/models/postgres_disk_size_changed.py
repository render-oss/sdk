from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_user import SchemasUser


T = TypeVar("T", bound="PostgresDiskSizeChanged")


@_attrs_define
class PostgresDiskSizeChanged:
    """
    Attributes:
        from_disk_size (int):
        to_disk_size (int):
        user (Union[Unset, SchemasUser]): User who triggered the action
    """

    from_disk_size: int
    to_disk_size: int
    user: Union[Unset, "SchemasUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_disk_size = self.from_disk_size

        to_disk_size = self.to_disk_size

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fromDiskSize": from_disk_size,
                "toDiskSize": to_disk_size,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_user import SchemasUser

        d = dict(src_dict)
        from_disk_size = d.pop("fromDiskSize")

        to_disk_size = d.pop("toDiskSize")

        _user = d.pop("user", UNSET)
        user: Union[Unset, SchemasUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = SchemasUser.from_dict(_user)

        postgres_disk_size_changed = cls(
            from_disk_size=from_disk_size,
            to_disk_size=to_disk_size,
            user=user,
        )

        postgres_disk_size_changed.additional_properties = d
        return postgres_disk_size_changed

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
