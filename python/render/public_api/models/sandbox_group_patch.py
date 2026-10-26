from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SandboxGroupPATCH")


@_attrs_define
class SandboxGroupPATCH:
    """
    Attributes:
        concurrency_limit (int): Maximum active sandboxes in the group. The configured value is capped
            by Render's limit for this workspace. Responses return the effective limit.
            Lowering the limit does not stop existing sandboxes.
             Example: 10.
    """

    concurrency_limit: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concurrency_limit = self.concurrency_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "concurrencyLimit": concurrency_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        concurrency_limit = d.pop("concurrencyLimit")

        sandbox_group_patch = cls(
            concurrency_limit=concurrency_limit,
        )

        sandbox_group_patch.additional_properties = d
        return sandbox_group_patch

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
