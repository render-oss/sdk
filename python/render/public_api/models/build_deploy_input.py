from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_deploy_service_scope import BuildDeployServiceScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildDeployInput")


@_attrs_define
class BuildDeployInput:
    """
    Attributes:
        service_scope (BuildDeployServiceScope): Which linked services the build deploys to:

            - `autodeploy_only`: every linked service with autodeploy on, including services set to deploy after CI checks
            pass. Services with autodeploy off do not get a deploy.
            - `none`: no services. The build runs and deploys nothing.
            - `custom`: the linked services in `serviceIds`, regardless of their autodeploy setting.
        service_ids (list[str] | Unset): IDs of the linked services to deploy to. Required when `serviceScope` is
            `custom`, and not allowed with the other scopes. You must be authorized to trigger a deploy for each service
            that you include in this list.
    """

    service_scope: BuildDeployServiceScope
    service_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_scope = self.service_scope.value

        service_ids: list[str] | Unset = UNSET
        if not isinstance(self.service_ids, Unset):
            service_ids = self.service_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serviceScope": service_scope,
            }
        )
        if service_ids is not UNSET:
            field_dict["serviceIds"] = service_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_scope = BuildDeployServiceScope(d.pop("serviceScope"))

        service_ids = cast(list[str], d.pop("serviceIds", UNSET))

        build_deploy_input = cls(
            service_scope=service_scope,
            service_ids=service_ids,
        )

        build_deploy_input.additional_properties = d
        return build_deploy_input

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
