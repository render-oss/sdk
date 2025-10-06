from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_deploy_body_clear_cache import CreateDeployBodyClearCache
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeployBody")


@_attrs_define
class CreateDeployBody:
    """
    Attributes:
        clear_cache (Union[Unset, CreateDeployBodyClearCache]): If `clear`, Render clears the service's build cache
            before deploying. This can be useful if you're experiencing issues with your build. Default:
            CreateDeployBodyClearCache.DO_NOT_CLEAR.
        commit_id (Union[Unset, str]): The SHA of a specific Git commit to deploy for a service. Defaults to the latest
            commit on the service's connected branch.

            Note that deploying a specific commit with this endpoint does not disable autodeploys for the service.

            You can toggle autodeploys for your service with the [Update service](https://api-
            docs.render.com/reference/update-service) endpoint or in the Render Dashboard.

            Not supported for cron jobs.
        image_url (Union[Unset, str]): The URL of the image to deploy for an image-backed service.

            The host, repository, and image name all must match the currently configured image for the service.
    """

    clear_cache: Union[Unset, CreateDeployBodyClearCache] = CreateDeployBodyClearCache.DO_NOT_CLEAR
    commit_id: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clear_cache: Union[Unset, str] = UNSET
        if not isinstance(self.clear_cache, Unset):
            clear_cache = self.clear_cache.value

        commit_id = self.commit_id

        image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clear_cache is not UNSET:
            field_dict["clearCache"] = clear_cache
        if commit_id is not UNSET:
            field_dict["commitId"] = commit_id
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _clear_cache = d.pop("clearCache", UNSET)
        clear_cache: Union[Unset, CreateDeployBodyClearCache]
        if isinstance(_clear_cache, Unset):
            clear_cache = UNSET
        else:
            clear_cache = CreateDeployBodyClearCache(_clear_cache)

        commit_id = d.pop("commitId", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        create_deploy_body = cls(
            clear_cache=clear_cache,
            commit_id=commit_id,
            image_url=image_url,
        )

        create_deploy_body.additional_properties = d
        return create_deploy_body

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
