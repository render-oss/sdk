from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.existing_resource_mode import ExistingResourceMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.blueprint_source import BlueprintSource


T = TypeVar("T", bound="CreateBlueprintRequest")


@_attrs_define
class CreateBlueprintRequest:
    """
    Attributes:
        owner_id (str): ID of the workspace in which to create the Blueprint. Example: tea-cjnxpkdhshc73d12t9i0.
        source (BlueprintSource):
        name (Union[Unset, str]): Name for the Blueprint. Defaults to an empty name. Default: ''.
        auto_sync (Union[Unset, bool]): Configuration value that controls whether or not this blueprint will be re-
            synced on each git push to the configured branch.
            Even when true, autoSync will not apply when the blueprint has the Created status, which indicates its first
            sync has not yet been approved.
            Other conditions, such as a locked workspace, can also prevent automatic syncing even when this is true.
             Default: True.
        existing_resources (Union[Unset, ExistingResourceMode]): How Sync planning should handle existing resources.
            `adopt` brings matching existing resources under this Blueprint's management
            and updates their configuration to match the Blueprint file.
            `create_new` creates a separate set of resources, leaving existing resources unchanged.
    """

    owner_id: str
    source: "BlueprintSource"
    name: Union[Unset, str] = ""
    auto_sync: Union[Unset, bool] = True
    existing_resources: Union[Unset, ExistingResourceMode] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        source = self.source.to_dict()

        name = self.name

        auto_sync = self.auto_sync

        existing_resources: Union[Unset, str] = UNSET
        if not isinstance(self.existing_resources, Unset):
            existing_resources = self.existing_resources.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "source": source,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if auto_sync is not UNSET:
            field_dict["autoSync"] = auto_sync
        if existing_resources is not UNSET:
            field_dict["existingResources"] = existing_resources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.blueprint_source import BlueprintSource

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        source = BlueprintSource.from_dict(d.pop("source"))

        name = d.pop("name", UNSET)

        auto_sync = d.pop("autoSync", UNSET)

        _existing_resources = d.pop("existingResources", UNSET)
        existing_resources: Union[Unset, ExistingResourceMode]
        if isinstance(_existing_resources, Unset):
            existing_resources = UNSET
        else:
            existing_resources = ExistingResourceMode(_existing_resources)

        create_blueprint_request = cls(
            owner_id=owner_id,
            source=source,
            name=name,
            auto_sync=auto_sync,
            existing_resources=existing_resources,
        )

        create_blueprint_request.additional_properties = d
        return create_blueprint_request

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
