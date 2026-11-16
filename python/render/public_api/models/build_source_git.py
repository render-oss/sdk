from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_source_git_region import BuildSourceGitRegion
from ..models.build_source_git_runtime import BuildSourceGitRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_build_filter import SchemasBuildFilter


T = TypeVar("T", bound="BuildSourceGit")


@_attrs_define
class BuildSourceGit:
    """
    Attributes:
        runtime (BuildSourceGitRuntime): Build runtime for the build source. Static sites are not supported for build
            sources.
        branch (str | Unset):
        build_command (str | Unset):
        build_filter (SchemasBuildFilter | Unset): Glob patterns matched against files changed by a commit. When set, a
            commit only triggers a build when at least one changed file matches `paths` and none match `ignoredPaths`.
            Useful for monorepos where a single repo backs many services.
        docker_context (str | Unset): Directory passed to `docker build` as the build context, relative to the
            repository root. Only valid for the `docker` runtime. Defaults to ".".
        dockerfile_path (str | Unset):
        registry_credential_id (str | Unset):
        region (BuildSourceGitRegion | Unset): Defaults to "oregon" Default: BuildSourceGitRegion.OREGON.
        repo_url (str | Unset):
        root_dir (str | Unset):
    """

    runtime: BuildSourceGitRuntime
    branch: str | Unset = UNSET
    build_command: str | Unset = UNSET
    build_filter: SchemasBuildFilter | Unset = UNSET
    docker_context: str | Unset = UNSET
    dockerfile_path: str | Unset = UNSET
    registry_credential_id: str | Unset = UNSET
    region: BuildSourceGitRegion | Unset = BuildSourceGitRegion.OREGON
    repo_url: str | Unset = UNSET
    root_dir: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        runtime = self.runtime.value

        branch = self.branch

        build_command = self.build_command

        build_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        docker_context = self.docker_context

        dockerfile_path = self.dockerfile_path

        registry_credential_id = self.registry_credential_id

        region: str | Unset = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        repo_url = self.repo_url

        root_dir = self.root_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runtime": runtime,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch
        if build_command is not UNSET:
            field_dict["buildCommand"] = build_command
        if build_filter is not UNSET:
            field_dict["buildFilter"] = build_filter
        if docker_context is not UNSET:
            field_dict["dockerContext"] = docker_context
        if dockerfile_path is not UNSET:
            field_dict["dockerfilePath"] = dockerfile_path
        if registry_credential_id is not UNSET:
            field_dict["registryCredentialId"] = registry_credential_id
        if region is not UNSET:
            field_dict["region"] = region
        if repo_url is not UNSET:
            field_dict["repoUrl"] = repo_url
        if root_dir is not UNSET:
            field_dict["rootDir"] = root_dir

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schemas_build_filter import SchemasBuildFilter  # noqa: PLC0415

        d = dict(src_dict)
        runtime = BuildSourceGitRuntime(d.pop("runtime"))

        branch = d.pop("branch", UNSET)

        build_command = d.pop("buildCommand", UNSET)

        _build_filter = d.pop("buildFilter", UNSET)
        build_filter: SchemasBuildFilter | Unset
        if isinstance(_build_filter, Unset):
            build_filter = UNSET
        else:
            build_filter = SchemasBuildFilter.from_dict(_build_filter)

        docker_context = d.pop("dockerContext", UNSET)

        dockerfile_path = d.pop("dockerfilePath", UNSET)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        _region = d.pop("region", UNSET)
        region: BuildSourceGitRegion | Unset
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = BuildSourceGitRegion(_region)

        repo_url = d.pop("repoUrl", UNSET)

        root_dir = d.pop("rootDir", UNSET)

        build_source_git = cls(
            runtime=runtime,
            branch=branch,
            build_command=build_command,
            build_filter=build_filter,
            docker_context=docker_context,
            dockerfile_path=dockerfile_path,
            registry_credential_id=registry_credential_id,
            region=region,
            repo_url=repo_url,
            root_dir=root_dir,
        )

        build_source_git.additional_properties = d
        return build_source_git

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
