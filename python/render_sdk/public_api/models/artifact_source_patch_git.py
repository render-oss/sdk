from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.artifact_source_patch_git_region import ArtifactSourcePATCHGitRegion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schemas_build_filter import SchemasBuildFilter


T = TypeVar("T", bound="ArtifactSourcePATCHGit")


@_attrs_define
class ArtifactSourcePATCHGit:
    """
    Attributes:
        base_dir (Union[Unset, str]):
        branch (Union[Unset, str]):
        build_command (Union[Unset, str]):
        build_filter (Union[Unset, SchemasBuildFilter]): Glob patterns matched against files changed by a commit. When
            set, a commit only triggers a build when at least one changed file matches `paths` and none match
            `ignoredPaths`. Useful for monorepos where a single repo backs many services.
        dockerfile_path (Union[Unset, str]):
        runtime (Union[Unset, str]):
        registry_credential_id (Union[Unset, str]):
        region (Union[Unset, ArtifactSourcePATCHGitRegion]): Region for the build. Honored only when this PATCH performs
            an image→build transition; rejected on a pure build patch (the cluster is pinned for an existing build), and
            must match the prior build region when switching back to build after time as an external image. Defaults to
            "oregon" for first-time builds.
        repo_url (Union[Unset, str]):
        root_dir (Union[Unset, str]):
    """

    base_dir: Union[Unset, str] = UNSET
    branch: Union[Unset, str] = UNSET
    build_command: Union[Unset, str] = UNSET
    build_filter: Union[Unset, "SchemasBuildFilter"] = UNSET
    dockerfile_path: Union[Unset, str] = UNSET
    runtime: Union[Unset, str] = UNSET
    registry_credential_id: Union[Unset, str] = UNSET
    region: Union[Unset, ArtifactSourcePATCHGitRegion] = UNSET
    repo_url: Union[Unset, str] = UNSET
    root_dir: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_dir = self.base_dir

        branch = self.branch

        build_command = self.build_command

        build_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.build_filter, Unset):
            build_filter = self.build_filter.to_dict()

        dockerfile_path = self.dockerfile_path

        runtime = self.runtime

        registry_credential_id = self.registry_credential_id

        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.value

        repo_url = self.repo_url

        root_dir = self.root_dir

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_dir is not UNSET:
            field_dict["baseDir"] = base_dir
        if branch is not UNSET:
            field_dict["branch"] = branch
        if build_command is not UNSET:
            field_dict["buildCommand"] = build_command
        if build_filter is not UNSET:
            field_dict["buildFilter"] = build_filter
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
        from ..models.schemas_build_filter import SchemasBuildFilter

        d = dict(src_dict)
        base_dir = d.pop("baseDir", UNSET)

        branch = d.pop("branch", UNSET)

        build_command = d.pop("buildCommand", UNSET)

        _build_filter = d.pop("buildFilter", UNSET)
        build_filter: Union[Unset, SchemasBuildFilter]
        if isinstance(_build_filter, Unset):
            build_filter = UNSET
        else:
            build_filter = SchemasBuildFilter.from_dict(_build_filter)

        dockerfile_path = d.pop("dockerfilePath", UNSET)

        runtime = d.pop("runtime", UNSET)

        registry_credential_id = d.pop("registryCredentialId", UNSET)

        _region = d.pop("region", UNSET)
        region: Union[Unset, ArtifactSourcePATCHGitRegion]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = ArtifactSourcePATCHGitRegion(_region)

        repo_url = d.pop("repoUrl", UNSET)

        root_dir = d.pop("rootDir", UNSET)

        artifact_source_patch_git = cls(
            base_dir=base_dir,
            branch=branch,
            build_command=build_command,
            build_filter=build_filter,
            dockerfile_path=dockerfile_path,
            runtime=runtime,
            registry_credential_id=registry_credential_id,
            region=region,
            repo_url=repo_url,
            root_dir=root_dir,
        )

        artifact_source_patch_git.additional_properties = d
        return artifact_source_patch_git

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
