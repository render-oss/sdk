from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_post_plan import SandboxPOSTPlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_network_policy import SandboxNetworkPolicy
    from ..models.sandbox_post_env import SandboxPOSTEnv
    from ..models.sandbox_post_files import SandboxPOSTFiles
    from ..models.sandbox_post_tags import SandboxPOSTTags


T = TypeVar("T", bound="SandboxPOST")


@_attrs_define
class SandboxPOST:
    """
    Attributes:
        base (Union[Unset, str]): Render base image: `render/sandbox-python` or `render/sandbox-node`. Example:
            render/sandbox-node.
        image (Union[Unset, str]): Docker/OCI image reference. Overrides `base`.
        setup (Union[Unset, list[str]]): Shell commands run sequentially after boot, before the sandbox is marked ready.
            Example: ['pip install flask pytest'].
        files (Union[Unset, SandboxPOSTFiles]): Seed files. Keys are absolute paths, values are file contents. Written
            after `setup` completes.
        network_policy (Union[Unset, SandboxNetworkPolicy]):
        env_group (Union[Unset, str]): Render environment group name or ID. Variables injected at runtime.
        env (Union[Unset, SandboxPOSTEnv]): Inline env vars. Merged with env group; inline wins on conflict.
        plan (Union[Unset, SandboxPOSTPlan]): Compute plan. Default: SandboxPOSTPlan.VALUE_0.
        timeout (Union[Unset, int]): Maximum sandbox lifetime in seconds. Sandbox is terminated when reached. Default:
            7200.
        idle_timeout (Union[Unset, int]): Seconds of inactivity before the sandbox is suspended. Default: 900.
        tags (Union[Unset, SandboxPOSTTags]): Key-value metadata for filtering and cost tracking.
        region (Union[Unset, str]): Render region. Defaults to the workspace default.
    """

    base: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    setup: Union[Unset, list[str]] = UNSET
    files: Union[Unset, "SandboxPOSTFiles"] = UNSET
    network_policy: Union[Unset, "SandboxNetworkPolicy"] = UNSET
    env_group: Union[Unset, str] = UNSET
    env: Union[Unset, "SandboxPOSTEnv"] = UNSET
    plan: Union[Unset, SandboxPOSTPlan] = SandboxPOSTPlan.VALUE_0
    timeout: Union[Unset, int] = 7200
    idle_timeout: Union[Unset, int] = 900
    tags: Union[Unset, "SandboxPOSTTags"] = UNSET
    region: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base = self.base

        image = self.image

        setup: Union[Unset, list[str]] = UNSET
        if not isinstance(self.setup, Unset):
            setup = self.setup

        files: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.files, Unset):
            files = self.files.to_dict()

        network_policy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.network_policy, Unset):
            network_policy = self.network_policy.to_dict()

        env_group = self.env_group

        env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.value

        timeout = self.timeout

        idle_timeout = self.idle_timeout

        tags: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base is not UNSET:
            field_dict["base"] = base
        if image is not UNSET:
            field_dict["image"] = image
        if setup is not UNSET:
            field_dict["setup"] = setup
        if files is not UNSET:
            field_dict["files"] = files
        if network_policy is not UNSET:
            field_dict["networkPolicy"] = network_policy
        if env_group is not UNSET:
            field_dict["envGroup"] = env_group
        if env is not UNSET:
            field_dict["env"] = env
        if plan is not UNSET:
            field_dict["plan"] = plan
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if idle_timeout is not UNSET:
            field_dict["idleTimeout"] = idle_timeout
        if tags is not UNSET:
            field_dict["tags"] = tags
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sandbox_network_policy import SandboxNetworkPolicy
        from ..models.sandbox_post_env import SandboxPOSTEnv
        from ..models.sandbox_post_files import SandboxPOSTFiles
        from ..models.sandbox_post_tags import SandboxPOSTTags

        d = dict(src_dict)
        base = d.pop("base", UNSET)

        image = d.pop("image", UNSET)

        setup = cast(list[str], d.pop("setup", UNSET))

        _files = d.pop("files", UNSET)
        files: Union[Unset, SandboxPOSTFiles]
        if isinstance(_files, Unset):
            files = UNSET
        else:
            files = SandboxPOSTFiles.from_dict(_files)

        _network_policy = d.pop("networkPolicy", UNSET)
        network_policy: Union[Unset, SandboxNetworkPolicy]
        if isinstance(_network_policy, Unset):
            network_policy = UNSET
        else:
            network_policy = SandboxNetworkPolicy.from_dict(_network_policy)

        env_group = d.pop("envGroup", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, SandboxPOSTEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = SandboxPOSTEnv.from_dict(_env)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, SandboxPOSTPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = SandboxPOSTPlan(_plan)

        timeout = d.pop("timeout", UNSET)

        idle_timeout = d.pop("idleTimeout", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, SandboxPOSTTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = SandboxPOSTTags.from_dict(_tags)

        region = d.pop("region", UNSET)

        sandbox_post = cls(
            base=base,
            image=image,
            setup=setup,
            files=files,
            network_policy=network_policy,
            env_group=env_group,
            env=env,
            plan=plan,
            timeout=timeout,
            idle_timeout=idle_timeout,
            tags=tags,
            region=region,
        )

        sandbox_post.additional_properties = d
        return sandbox_post

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
