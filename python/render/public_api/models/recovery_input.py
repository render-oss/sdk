from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecoveryInput")


@_attrs_define
class RecoveryInput:
    """
    Attributes:
        restore_name (str | Unset): Name of the new database.
        restore_time (datetime.datetime | Unset): The point in time to restore the database to. See `/recovery-info` for
            restore availability
        datadog_api_key (str | Unset): Datadog API key to use for monitoring the new database. Defaults to the API key
            of the original database. Use an empty string to prevent copying of the API key to the new database.
        datadog_site (str | Unset): Datadog region code to use for monitoring the new database. Defaults to the region
            code of the original database. Use an empty string to prevent copying of the region code to the new database.
        plan (str | Unset): The plan to use for the new database. Defaults to the same plan as the original database.
            Cannot be a lower tier plan than the original database.
        environment_id (str | Unset): The environment to create the new database in. Defaults to the environment of the
            original database.
    """

    restore_name: str | Unset = UNSET
    restore_time: datetime.datetime | Unset = UNSET
    datadog_api_key: str | Unset = UNSET
    datadog_site: str | Unset = UNSET
    plan: str | Unset = UNSET
    environment_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        restore_name = self.restore_name

        restore_time: str | Unset = UNSET
        if not isinstance(self.restore_time, Unset):
            restore_time = self.restore_time.isoformat()

        datadog_api_key = self.datadog_api_key

        datadog_site = self.datadog_site

        plan = self.plan

        environment_id = self.environment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if restore_name is not UNSET:
            field_dict["restoreName"] = restore_name
        if restore_time is not UNSET:
            field_dict["restoreTime"] = restore_time
        if datadog_api_key is not UNSET:
            field_dict["datadogApiKey"] = datadog_api_key
        if datadog_site is not UNSET:
            field_dict["datadogSite"] = datadog_site
        if plan is not UNSET:
            field_dict["plan"] = plan
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        restore_name = d.pop("restoreName", UNSET)

        _restore_time = d.pop("restoreTime", UNSET)
        restore_time: datetime.datetime | Unset
        if isinstance(_restore_time, Unset):
            restore_time = UNSET
        else:
            restore_time = datetime.datetime.fromisoformat(_restore_time)

        datadog_api_key = d.pop("datadogApiKey", UNSET)

        datadog_site = d.pop("datadogSite", UNSET)

        plan = d.pop("plan", UNSET)

        environment_id = d.pop("environmentId", UNSET)

        recovery_input = cls(
            restore_name=restore_name,
            restore_time=restore_time,
            datadog_api_key=datadog_api_key,
            datadog_site=datadog_site,
            plan=plan,
            environment_id=environment_id,
        )

        recovery_input.additional_properties = d
        return recovery_input

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
