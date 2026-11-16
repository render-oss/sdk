from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.render_subdomain_policy import RenderSubdomainPolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.previews import Previews


T = TypeVar("T", bound="StaticSiteDetailsPATCH")


@_attrs_define
class StaticSiteDetailsPATCH:
    """
    Attributes:
        build_command (str | Unset):
        publish_path (str | Unset):
        pull_request_previews_enabled (PullRequestPreviewsEnabled | Unset): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Previews | Unset):
        render_subdomain_policy (RenderSubdomainPolicy | Unset): Controls whether render.com subdomains are available
            for the service
        ip_allow_list (list[CidrBlockAndDescription] | Unset):
    """

    build_command: str | Unset = UNSET
    publish_path: str | Unset = UNSET
    pull_request_previews_enabled: PullRequestPreviewsEnabled | Unset = UNSET
    previews: Previews | Unset = UNSET
    render_subdomain_policy: RenderSubdomainPolicy | Unset = UNSET
    ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        publish_path = self.publish_path

        pull_request_previews_enabled: str | Unset = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: dict[str, Any] | Unset = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        render_subdomain_policy: str | Unset = UNSET
        if not isinstance(self.render_subdomain_policy, Unset):
            render_subdomain_policy = self.render_subdomain_policy.value

        ip_allow_list: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if build_command is not UNSET:
            field_dict["buildCommand"] = build_command
        if publish_path is not UNSET:
            field_dict["publishPath"] = publish_path
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if render_subdomain_policy is not UNSET:
            field_dict["renderSubdomainPolicy"] = render_subdomain_policy
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription  # noqa: PLC0415
        from ..models.previews import Previews  # noqa: PLC0415

        d = dict(src_dict)
        build_command = d.pop("buildCommand", UNSET)

        publish_path = d.pop("publishPath", UNSET)

        _pull_request_previews_enabled = d.pop("pullRequestPreviewsEnabled", UNSET)
        pull_request_previews_enabled: PullRequestPreviewsEnabled | Unset
        if isinstance(_pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = UNSET
        else:
            pull_request_previews_enabled = PullRequestPreviewsEnabled(_pull_request_previews_enabled)

        _previews = d.pop("previews", UNSET)
        previews: Previews | Unset
        if isinstance(_previews, Unset):
            previews = UNSET
        else:
            previews = Previews.from_dict(_previews)

        _render_subdomain_policy = d.pop("renderSubdomainPolicy", UNSET)
        render_subdomain_policy: RenderSubdomainPolicy | Unset
        if isinstance(_render_subdomain_policy, Unset):
            render_subdomain_policy = UNSET
        else:
            render_subdomain_policy = RenderSubdomainPolicy(_render_subdomain_policy)

        _ip_allow_list = d.pop("ipAllowList", UNSET)
        ip_allow_list: list[CidrBlockAndDescription] | Unset = UNSET
        if _ip_allow_list is not UNSET:
            ip_allow_list = []
            for ip_allow_list_item_data in _ip_allow_list:
                ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

                ip_allow_list.append(ip_allow_list_item)

        static_site_details_patch = cls(
            build_command=build_command,
            publish_path=publish_path,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            render_subdomain_policy=render_subdomain_policy,
            ip_allow_list=ip_allow_list,
        )

        static_site_details_patch.additional_properties = d
        return static_site_details_patch

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
