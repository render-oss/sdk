from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.blueprint import Blueprint
    from ..models.sync import Sync


T = TypeVar("T", bound="CreateBlueprintResponse")


@_attrs_define
class CreateBlueprintResponse:
    """The newly created Blueprint

    Attributes:
        blueprint (Blueprint):
        sync (Sync):
    """

    blueprint: "Blueprint"
    sync: "Sync"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blueprint = self.blueprint.to_dict()

        sync = self.sync.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blueprint": blueprint,
                "sync": sync,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blueprint import Blueprint
        from ..models.sync import Sync

        d = dict(src_dict)
        blueprint = Blueprint.from_dict(d.pop("blueprint"))

        sync = Sync.from_dict(d.pop("sync"))

        create_blueprint_response = cls(
            blueprint=blueprint,
            sync=sync,
        )

        create_blueprint_response.additional_properties = d
        return create_blueprint_response

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
