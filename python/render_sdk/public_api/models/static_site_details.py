from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_plan import BuildPlan
from ..models.pull_request_previews_enabled import PullRequestPreviewsEnabled
from ..models.render_subdomain_policy import RenderSubdomainPolicy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cidr_block_and_description import CidrBlockAndDescription
    from ..models.previews import Previews
    from ..models.resource import Resource


T = TypeVar("T", bound="StaticSiteDetails")


@_attrs_define
class StaticSiteDetails:
    """
    Attributes:
        build_command (str):
        publish_path (str):
        url (str):
        build_plan (BuildPlan):
        ip_allow_list (Union[Unset, list['CidrBlockAndDescription']]):
        parent_server (Union[Unset, Resource]):
        pull_request_previews_enabled (Union[Unset, PullRequestPreviewsEnabled]): This field has been deprecated.
            previews.generation should be used in its place.
        previews (Union[Unset, Previews]):
        render_subdomain_policy (Union[Unset, RenderSubdomainPolicy]): Controls whether render.com subdomains are
            available for the service
    """

    build_command: str
    publish_path: str
    url: str
    build_plan: BuildPlan
    ip_allow_list: Union[Unset, list["CidrBlockAndDescription"]] = UNSET
    parent_server: Union[Unset, "Resource"] = UNSET
    pull_request_previews_enabled: Union[Unset, PullRequestPreviewsEnabled] = UNSET
    previews: Union[Unset, "Previews"] = UNSET
    render_subdomain_policy: Union[Unset, RenderSubdomainPolicy] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        build_command = self.build_command

        publish_path = self.publish_path

        url = self.url

        build_plan = self.build_plan.value

        ip_allow_list: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ip_allow_list, Unset):
            ip_allow_list = []
            for ip_allow_list_item_data in self.ip_allow_list:
                ip_allow_list_item = ip_allow_list_item_data.to_dict()
                ip_allow_list.append(ip_allow_list_item)

        parent_server: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent_server, Unset):
            parent_server = self.parent_server.to_dict()

        pull_request_previews_enabled: Union[Unset, str] = UNSET
        if not isinstance(self.pull_request_previews_enabled, Unset):
            pull_request_previews_enabled = self.pull_request_previews_enabled.value

        previews: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previews, Unset):
            previews = self.previews.to_dict()

        render_subdomain_policy: Union[Unset, str] = UNSET
        if not isinstance(self.render_subdomain_policy, Unset):
            render_subdomain_policy = self.render_subdomain_policy.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "buildCommand": build_command,
                "publishPath": publish_path,
                "url": url,
                "buildPlan": build_plan,
            }
        )
        if ip_allow_list is not UNSET:
            field_dict["ipAllowList"] = ip_allow_list
        if parent_server is not UNSET:
            field_dict["parentServer"] = parent_server
        if pull_request_previews_enabled is not UNSET:
            field_dict["pullRequestPreviewsEnabled"] = pull_request_previews_enabled
        if previews is not UNSET:
            field_dict["previews"] = previews
        if render_subdomain_policy is not UNSET:
            field_dict["renderSubdomainPolicy"] = render_subdomain_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cidr_block_and_description import CidrBlockAndDescription
        from ..models.previews import Previews
        from ..models.resource import Resource

        d = dict(src_dict)
        build_command = d.pop("buildCommand")

        publish_path = d.pop("publishPath")

        url = d.pop("url")

        build_plan = BuildPlan(d.pop("buildPlan"))

        ip_allow_list = []
        _ip_allow_list = d.pop("ipAllowList", UNSET)
        for ip_allow_list_item_data in _ip_allow_list or []:
            ip_allow_list_item = CidrBlockAndDescription.from_dict(ip_allow_list_item_data)

            ip_allow_list.append(ip_allow_list_item)

        _parent_server = d.pop("parentServer", UNSET)
        parent_server: Union[Unset, Resource]
        if isinstance(_parent_server, Unset):
            parent_server = UNSET
        else:
            parent_server = Resource.from_dict(_parent_server)

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

        _render_subdomain_policy = d.pop("renderSubdomainPolicy", UNSET)
        render_subdomain_policy: Union[Unset, RenderSubdomainPolicy]
        if isinstance(_render_subdomain_policy, Unset):
            render_subdomain_policy = UNSET
        else:
            render_subdomain_policy = RenderSubdomainPolicy(_render_subdomain_policy)

        static_site_details = cls(
            build_command=build_command,
            publish_path=publish_path,
            url=url,
            build_plan=build_plan,
            ip_allow_list=ip_allow_list,
            parent_server=parent_server,
            pull_request_previews_enabled=pull_request_previews_enabled,
            previews=previews,
            render_subdomain_policy=render_subdomain_policy,
        )

        static_site_details.additional_properties = d
        return static_site_details

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
