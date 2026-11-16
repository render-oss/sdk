from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostgresProcess")


@_attrs_define
class PostgresProcess:
    """A single live process from pg_stat_activity.

    Attributes:
        pid (int | Unset):
        database_name (str | Unset):
        username (str | Unset):
        application_name (str | Unset):
        client_addr (str | Unset):
        backend_start (datetime.datetime | Unset):
        query_start (datetime.datetime | Unset):
        state (str | Unset):
        wait_event (str | Unset):
        wait_event_type (str | Unset):
        query (str | Unset):
        duration (float | Unset): Duration of the query, in seconds.
        is_leader (bool | Unset): Whether this process is running against the primary instance of a highly available
            database.
    """

    pid: int | Unset = UNSET
    database_name: str | Unset = UNSET
    username: str | Unset = UNSET
    application_name: str | Unset = UNSET
    client_addr: str | Unset = UNSET
    backend_start: datetime.datetime | Unset = UNSET
    query_start: datetime.datetime | Unset = UNSET
    state: str | Unset = UNSET
    wait_event: str | Unset = UNSET
    wait_event_type: str | Unset = UNSET
    query: str | Unset = UNSET
    duration: float | Unset = UNSET
    is_leader: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pid = self.pid

        database_name = self.database_name

        username = self.username

        application_name = self.application_name

        client_addr = self.client_addr

        backend_start: str | Unset = UNSET
        if not isinstance(self.backend_start, Unset):
            backend_start = self.backend_start.isoformat()

        query_start: str | Unset = UNSET
        if not isinstance(self.query_start, Unset):
            query_start = self.query_start.isoformat()

        state = self.state

        wait_event = self.wait_event

        wait_event_type = self.wait_event_type

        query = self.query

        duration = self.duration

        is_leader = self.is_leader

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pid is not UNSET:
            field_dict["pid"] = pid
        if database_name is not UNSET:
            field_dict["databaseName"] = database_name
        if username is not UNSET:
            field_dict["username"] = username
        if application_name is not UNSET:
            field_dict["applicationName"] = application_name
        if client_addr is not UNSET:
            field_dict["clientAddr"] = client_addr
        if backend_start is not UNSET:
            field_dict["backendStart"] = backend_start
        if query_start is not UNSET:
            field_dict["queryStart"] = query_start
        if state is not UNSET:
            field_dict["state"] = state
        if wait_event is not UNSET:
            field_dict["waitEvent"] = wait_event
        if wait_event_type is not UNSET:
            field_dict["waitEventType"] = wait_event_type
        if query is not UNSET:
            field_dict["query"] = query
        if duration is not UNSET:
            field_dict["duration"] = duration
        if is_leader is not UNSET:
            field_dict["isLeader"] = is_leader

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pid = d.pop("pid", UNSET)

        database_name = d.pop("databaseName", UNSET)

        username = d.pop("username", UNSET)

        application_name = d.pop("applicationName", UNSET)

        client_addr = d.pop("clientAddr", UNSET)

        _backend_start = d.pop("backendStart", UNSET)
        backend_start: datetime.datetime | Unset
        if isinstance(_backend_start, Unset):
            backend_start = UNSET
        else:
            backend_start = datetime.datetime.fromisoformat(_backend_start)

        _query_start = d.pop("queryStart", UNSET)
        query_start: datetime.datetime | Unset
        if isinstance(_query_start, Unset):
            query_start = UNSET
        else:
            query_start = datetime.datetime.fromisoformat(_query_start)

        state = d.pop("state", UNSET)

        wait_event = d.pop("waitEvent", UNSET)

        wait_event_type = d.pop("waitEventType", UNSET)

        query = d.pop("query", UNSET)

        duration = d.pop("duration", UNSET)

        is_leader = d.pop("isLeader", UNSET)

        postgres_process = cls(
            pid=pid,
            database_name=database_name,
            username=username,
            application_name=application_name,
            client_addr=client_addr,
            backend_start=backend_start,
            query_start=query_start,
            state=state,
            wait_event=wait_event,
            wait_event_type=wait_event_type,
            query=query,
            duration=duration,
            is_leader=is_leader,
        )

        postgres_process.additional_properties = d
        return postgres_process

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
