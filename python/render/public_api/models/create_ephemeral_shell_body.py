from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateEphemeralShellBody")


@_attrs_define
class CreateEphemeralShellBody:
    """
    Attributes:
        plan (Union[Unset, str]): The plan to use when creating the ephemeral shell instance.
        size (Union[Unset, str]): The size to use when creating the ephemeral shell instance.
            Deprecated: use `plan` instead. This field will be removed in a future release.
    """

    plan: Union[Unset, str] = UNSET
    size: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan is not UNSET:
            field_dict["plan"] = plan
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan = d.pop("plan", UNSET)

        size = d.pop("size", UNSET)

        create_ephemeral_shell_body = cls(
            plan=plan,
            size=size,
        )

        create_ephemeral_shell_body.additional_properties = d
        return create_ephemeral_shell_body

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
