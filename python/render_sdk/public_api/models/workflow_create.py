from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.region import Region

if TYPE_CHECKING:
    from ..models.build_config import BuildConfig


T = TypeVar("T", bound="WorkflowCreate")


@_attrs_define
class WorkflowCreate:
    """
    Attributes:
        name (str):
        owner_id (str):
        build_config (BuildConfig):
        run_command (str): The command to run the workflow
        region (Region): Defaults to "oregon"
    """

    name: str
    owner_id: str
    build_config: "BuildConfig"
    run_command: str
    region: Region
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        owner_id = self.owner_id

        build_config = self.build_config.to_dict()

        run_command = self.run_command

        region = self.region.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "buildConfig": build_config,
                "runCommand": run_command,
                "region": region,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_config import BuildConfig

        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        build_config = BuildConfig.from_dict(d.pop("buildConfig"))

        run_command = d.pop("runCommand")

        region = Region(d.pop("region"))

        workflow_create = cls(
            name=name,
            owner_id=owner_id,
            build_config=build_config,
            run_command=run_command,
            region=region,
        )

        workflow_create.additional_properties = d
        return workflow_create

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
