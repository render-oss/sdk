from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.render_subdomain_policy import RenderSubdomainPolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.header_input import HeaderInput
    from ..models.previews import Previews
    from ..models.route_post import RoutePost


T = TypeVar("T", bound="StaticSiteDetailsPOST")


@_attrs_define
class StaticSiteDetailsPOST:
    """
    Attributes:
        build_command (Union[Unset, str]):
        headers (Union[Unset, list['HeaderInput']]):
        publish_path (Union[Unset, str]): Defaults to "public"
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        routes (Union[Unset, list['RoutePost']]):
        render_subdomain_policy (Union[Unset, RenderSubdomainPolicy]): Controls whether render.com subdomains are
            available for the service
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
    """

    build_command: Union[Unset, str] = UNSET
    headers: Union[Unset, list["HeaderInput"]] = UNSET
    publish_path: Union[Unset, str] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    routes: Union[Unset, list["RoutePost"]] = UNSET
    render_subdomain_policy: Union[Unset, RenderSubdomainPolicy] = UNSET
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        headers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = []
            for headers_item_data in self.headers:
                headers_item = headers_item_data.to_dict()
                headers.append(headers_item)

        publish_path = self.publish_path

        pull_request_previews_enabled: Union[Unset, str] = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        routes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.routes, Unset):
            routes = []
            for routes_item_data in self.routes:
                routes_item = routes_item_data.to_dict()
                routes.append(routes_item)

        render_subdomain_policy: Union[Unset, str] = UNSET
        if not isinstance(self.render_subdomain_policy, Unset):
            render_subdomain_policy = self.render_subdomain_policy.value

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
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
        if headers is not UNSET:
            field_dict["headers"] = headers
        if publish_path is not UNSET:
            field_dict["publishPath"] = publish_path
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if routes is not UNSET:
            field_dict["routes"] = routes
        if render_subdomain_policy is not UNSET:
            field_dict["renderSubdomainPolicy"] = render_subdomain_policy
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.header_input import HeaderInput
        from ..models.previews import Previews
        from ..models.route_post import RoutePost

        d = dict(src_dict)
        build_command = d.pop("buildCommand", UNSET)

        headers = []
        _headers = d.pop("headers", UNSET)
        for headers_item_data in _headers or []:
            headers_item = HeaderInput.from_dict(headers_item_data)

            headers.append(headers_item)

        publish_path = d.pop("publishPath", UNSET)

        _pull_request_previews_enabled = d.pop("pullRequestPreviewsEnabled", UNSET)
        pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled]
        if isinstance(_pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = UNSET
        else:
            pull_request_previews_enabled = PullRequestPreviewsEnabled(_pull_request_previews_enabled)

        _previews = d.pop("previews", UNSET)
        previews: Union[Unset, Previews]
        if isinstance(_previews, Unset):
            previews = UNSET
        else:
            previews = Previews.from_dict(_previews)

        routes = []
        _routes = d.pop("routes", UNSET)
        for routes_item_data in _routes or []:
            routes_item = RoutePost.from_dict(routes_item_data)

            routes.append(routes_item)

        _render_subdomain_policy = d.pop("renderSubdomainPolicy", UNSET)
        render_subdomain_policy: Union[Unset, RenderSubdomainPolicy]
        if isinstance(_render_subdomain_policy, Unset):
            render_subdomain_policy = UNSET
        else:
            render_subdomain_policy = RenderSubdomainPolicy(_render_subdomain_policy)

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        static_site_details_post = cls(
            build_command=build_command,
            headers=headers,
            publish_path=publish_path,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            routes=routes,
            render_subdomain_policy=render_subdomain_policy,
            ip_allow_list=ip_allow_list,
        )

        static_site_details_post.additional_properties = d
        return static_site_details_post

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
