from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.service import Service


T = TypeVar("T", bound="ServiceAndDeploy")


@_attrs_define
class ServiceAndDeploy:
    """
    Attributes:
        service (Service | Unset):
        deploy_id (str | Unset):
    """

    service: Service | Unset = UNSET
    deploy_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service: dict[str, Any] | Unset = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.to_dict()

        deploy_id = self.deploy_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service is not UNSET:
            field_dict["service"] = service
        if deploy_id is not UNSET:
            field_dict["deployId"] = deploy_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service import Service  # noqa: PLC0415

        d = dict(src_dict)
        _service = d.pop("service", UNSET)
        service: Service | Unset
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = Service.from_dict(_service)

        deploy_id = d.pop("deployId", UNSET)

        service_and_deploy = cls(
            service=service,
            deploy_id=deploy_id,
        )

        service_and_deploy.additional_properties = d
        return service_and_deploy

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
