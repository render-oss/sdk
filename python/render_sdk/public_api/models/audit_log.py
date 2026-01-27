import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_log_event import AuditLogEvent
from ..models.audit_log_status import AuditLogStatus

if TYPE_CHECKING:
    from ..models.audit_log_actor import AuditLogActor
    from ..models.audit_log_metadata import AuditLogMetadata


T = TypeVar("T", bound="AuditLog")


@_attrs_define
class AuditLog:
    """
    Attributes:
        id (str): Unique identifier for the audit log entry Example: aud-123456789.
        timestamp (datetime.datetime): When the event occurred (ISO 8601 format) Example: 2023-10-01T12:00:00Z.
        event (AuditLogEvent): The type of event that occurred Example: CreateServerEvent.
        status (AuditLogStatus): The status of the event Example: success.
        actor (AuditLogActor):
        metadata (AuditLogMetadata): Additional context information about the event Example: {'service':
            'srv-123456789', 'field': 'env_vars'}.
    """

    id: str
    timestamp: datetime.datetime
    event: AuditLogEvent
    status: AuditLogStatus
    actor: "AuditLogActor"
    metadata: "AuditLogMetadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        timestamp = self.timestamp.isoformat()

        event = self.event.value

        status = self.status.value

        actor = self.actor.to_dict()

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "timestamp": timestamp,
                "event": event,
                "status": status,
                "actor": actor,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_log_actor import AuditLogActor
        from ..models.audit_log_metadata import AuditLogMetadata

        d = dict(src_dict)
        id = d.pop("id")

        timestamp = isoparse(d.pop("timestamp"))

        event = AuditLogEvent(d.pop("event"))

        status = AuditLogStatus(d.pop("status"))

        actor = AuditLogActor.from_dict(d.pop("actor"))

        metadata = AuditLogMetadata.from_dict(d.pop("metadata"))

        audit_log = cls(
            id=id,
            timestamp=timestamp,
            event=event,
            status=status,
            actor=actor,
            metadata=metadata,
        )

        audit_log.additional_properties = d
        return audit_log

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
