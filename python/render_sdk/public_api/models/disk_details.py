import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskDetails")


@_attrs_define
class DiskDetails:
    """
    Attributes:
        id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        name (str):
        size_gb (int):
        mount_path (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        service_id (Union[Unset, str]):
    """

    id: str
    name: str
    size_gb: int
    mount_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    service_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size_gb = self.size_gb

        mount_path = self.mount_path

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        service_id = self.service_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "sizeGB": size_gb,
                "mountPath": mount_path,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if service_id is not UNSET:
            field_dict["serviceId"] = service_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size_gb = d.pop("sizeGB")

        mount_path = d.pop("mountPath")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        service_id = d.pop("serviceId", UNSET)

        disk_details = cls(
            id=id,
            name=name,
            size_gb=size_gb,
            mount_path=mount_path,
            created_at=created_at,
            updated_at=updated_at,
            service_id=service_id,
        )

        disk_details.additional_properties = d
        return disk_details

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
