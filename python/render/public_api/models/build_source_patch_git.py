from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.build_source_patch_git_region import BuildSourcePATCHGitRegion
from ..models.build_source_patch_git_runtime import BuildSourcePATCHGitRuntime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_build_filter import SchemasBuildFilter


T = TypeVar("T", bound="BuildSourcePATCHGit")


@_attrs_define
class BuildSourcePATCHGit:
    """
    Attributes:
        branch (str | Unset):
        build_command (str | Unset):
        build_filter (SchemasBuildFilter | Unset): Glob patterns matched against files changed by a commit. When set, a
            commit only triggers a build when at least one changed file matches `paths` and none match `ignoredPaths`.
            Useful for monorepos where a single repo backs many services.
        docker_context (str | Unset): Directory passed to `docker build` as the build context, relative to the
            repository root. Only valid for the `docker` runtime.
        dockerfile_path (str | Unset):
        runtime (BuildSourcePATCHGitRuntime | Unset): Build runtime for the build source. Static sites are not supported
            for build sources.
        registry_credential_id (str | Unset): Optional reference to the registry credential for this build. Omit the
            field to leave the stored credential unchanged; send an empty string to clear it.
        region (BuildSourcePATCHGitRegion | Unset): Region for the build. Honored only when this PATCH performs an
            image→build transition; rejected on a pure build patch (the cluster is pinned for an existing build), and must
            match the prior build region when switching back to build after time as an external image. Defaults to "oregon"
            for first-time builds.
        repo_url (str | Unset):
        root_dir (str | Unset):
    """

    branch: str | Unset = UNSET
    build_command: str | Unset = UNSET
    build_filter: SchemasBuildFilter | Unset = UNSET
    docker_context: str | Unset = UNSET
    dockerfile_path: str | Unset = UNSET
    runtime: BuildSourcePATCHGitRuntime | Unset = UNSET
    registry_credential_id: str | Unset = UNSET
    region: BuildSourcePATCHGitRegion | Unset = UNSET
    repo_url: str | Unset = UNSET
    root_dir: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        branch = self.branch

        build_command = self.build_command

        build_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        docker_context = self.docker_context

        dockerfile_path = self.dockerfile_path

        runtime: str | Unset = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.value

        registry_credential_id = self.registry_credential_id

        region: str | Unset = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        repo_url = self.repo_url

        root_dir = self.root_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
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

        _runtime = d.pop("runtime", UNSET)
        runtime: BuildSourcePATCHGitRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = BuildSourcePATCHGitRuntime(_runtime)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        _region = d.pop("region", UNSET)
        region: BuildSourcePATCHGitRegion | Unset
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = BuildSourcePATCHGitRegion(_region)

        repo_url = d.pop("repoUrl", UNSET)

        root_dir = d.pop("rootDir", UNSET)

        build_source_patch_git = cls(
            branch=branch,
            build_command=build_command,
            build_filter=build_filter,
            docker_context=docker_context,
            dockerfile_path=dockerfile_path,
            runtime=runtime,
            registry_credential_id=registry_credential_id,
            region=region,
            repo_url=repo_url,
            root_dir=root_dir,
        )

        build_source_patch_git.additional_properties = d
        return build_source_patch_git

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
