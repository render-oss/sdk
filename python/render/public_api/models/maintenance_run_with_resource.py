import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_state import MaintenanceState
from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceRunWithResource")


@_attrs_define
class MaintenanceRunWithResource:
    """
    Attributes:
        id (str):  Example: mrn-cph1rs3idesc73a2b2mg.
        type_ (str):
        scheduled_at (datetime.datetime):
        state (MaintenanceState):
        resource_id (str): The Id of a resource that can undergo maintenance (Id of a service, a Postgres instance, or a
            Redis instance)
        pending_maintenance_by (Union[Unset, datetime.datetime]): If present, the maintenance run cannot be scheduled
            for later than this date-time.
    """

    id: str
    type_: str
    scheduled_at: datetime.datetime
    state: MaintenanceState
    resource_id: str
    pending_maintenance_by: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        scheduled_at = self.scheduled_at.isoformat()

        state = self.state.value

        resource_id = self.resource_id

        pending_maintenance_by: Union[Unset, str] = UNSET
        if not isinstance(self.pending_maintenance_by, Unset):
            pending_maintenance_by = self.pending_maintenance_by.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "scheduledAt": scheduled_at,
                "state": state,
                "resourceId": resource_id,
            }
        )
        if pending_maintenance_by is not UNSET:
            field_dict["pendingMaintenanceBy"] = pending_maintenance_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        scheduled_at = isoparse(d.pop("scheduledAt"))

        state = MaintenanceState(d.pop("state"))

        resource_id = d.pop("resourceId")

        _pending_maintenance_by = d.pop("pendingMaintenanceBy", UNSET)
        pending_maintenance_by: Union[Unset, datetime.datetime]
        if isinstance(_pending_maintenance_by, Unset):
            pending_maintenance_by = UNSET
        else:
            pending_maintenance_by = isoparse(_pending_maintenance_by)

        maintenance_run_with_resource = cls(
            id=id,
            type_=type_,
            scheduled_at=scheduled_at,
            state=state,
            resource_id=resource_id,
            pending_maintenance_by=pending_maintenance_by,
        )

        maintenance_run_with_resource.additional_properties = d
        return maintenance_run_with_resource

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
