import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.dedicated_ip_status import DedicatedIPStatus
from ..models.region import Region
from ..types import UNSET, Unset

T = TypeVar("T", bound="DedicatedIP")


@_attrs_define
class DedicatedIP:
    """
    Attributes:
        id (str): Unique identifier for this dedicated IP set.
        name (str): Descriptive name for this dedicated IP set.
        description (str): Free-form description for this dedicated IP set.
        owner_id (str): The ID of the workspace that owns this dedicated IP set.
        region (Region): Defaults to "oregon"
        environment_ids (list[str]): Environments this dedicated IP set applies to. If empty, it applies to all services
            in the workspace within its region.
        ips (list[str]): The IPv4 addresses assigned to this dedicated IP set.
        status (DedicatedIPStatus): Current status of a dedicated IP set.
        created_at (datetime.datetime): Time the dedicated IP set was created.
        updated_at (Union[Unset, datetime.datetime]): Time the dedicated IP set was last updated.
    """

    id: str
    name: str
    description: str
    owner_id: str
    region: Region
    environment_ids: list[str]
    ips: list[str]
    status: DedicatedIPStatus
    created_at: datetime.datetime
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        owner_id = self.owner_id

        region = self.region.value

        environment_ids = self.environment_ids

        ips = self.ips

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "ownerId": owner_id,
                "region": region,
                "environmentIds": environment_ids,
                "ips": ips,
                "status": status,
                "createdAt": created_at,
            }
        )
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        owner_id = d.pop("ownerId")

        region = Region(d.pop("region"))

        environment_ids = cast(list[str], d.pop("environmentIds"))

        ips = cast(list[str], d.pop("ips"))

        status = DedicatedIPStatus(d.pop("status"))

        created_at = isoparse(d.pop("createdAt"))

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        dedicated_ip = cls(
            id=id,
            name=name,
            description=description,
            owner_id=owner_id,
            region=region,
            environment_ids=environment_ids,
            ips=ips,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        dedicated_ip.additional_properties = d
        return dedicated_ip

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
