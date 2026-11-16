from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.build_source_git import BuildSourceGit
    from ..models.build_source_image import BuildSourceImage
    from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue
    from ..models.env_var_key_value import EnvVarKeyValue
    from ..models.secret_file_input import SecretFileInput


T = TypeVar("T", bound="BuildSourcePOSTInput")


@_attrs_define
class BuildSourcePOSTInput:
    """
    Attributes:
        owner_id (str):
        name (str):
        project_id (str | Unset):
        git (BuildSourceGit | Unset):
        image (BuildSourceImage | Unset):
        service_ids (list[str] | Unset):
        env_vars (list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset):
        secret_files (list[SecretFileInput] | Unset): Secret files for the build source's build. Only valid for `git`
            sources.
        env_group_ids (list[str] | Unset): IDs of env groups to link to the build source. Only valid for `git` sources;
            env groups must belong to the same workspace and must not be scoped to an environment.
    """

    owner_id: str
    name: str
    project_id: str | Unset = UNSET
    git: BuildSourceGit | Unset = UNSET
    image: BuildSourceImage | Unset = UNSET
    service_ids: list[str] | Unset = UNSET
    env_vars: list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset = UNSET
    secret_files: list[SecretFileInput] | Unset = UNSET
    env_group_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415

        owner_id = self.owner_id

        name = self.name

        project_id = self.project_id

        git: dict[str, Any] | Unset = UNSET
        if not isinstance(self.git, Unset):
            git = self.git.to_dict()

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        service_ids: list[str] | Unset = UNSET
        if not isinstance(self.service_ids, Unset):
            service_ids = self.service_ids

        env_vars: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.env_vars, Unset):
            env_vars = []
            for componentsschemasenv_var_input_array_item_data in self.env_vars:
                componentsschemasenv_var_input_array_item: dict[str, Any]
                if isinstance(componentsschemasenv_var_input_array_item_data, EnvVarKeyValue):
                    componentsschemasenv_var_input_array_item = componentsschemasenv_var_input_array_item_data.to_dict()
                else:
                    componentsschemasenv_var_input_array_item = componentsschemasenv_var_input_array_item_data.to_dict()

                env_vars.append(componentsschemasenv_var_input_array_item)

        secret_files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secret_files, Unset):
            secret_files = []
            for secret_files_item_data in self.secret_files:
                secret_files_item = secret_files_item_data.to_dict()
                secret_files.append(secret_files_item)

        env_group_ids: list[str] | Unset = UNSET
        if not isinstance(self.env_group_ids, Unset):
            env_group_ids = self.env_group_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "name": name,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if git is not UNSET:
            field_dict["git"] = git
        if image is not UNSET:
            field_dict["image"] = image
        if service_ids is not UNSET:
            field_dict["serviceIds"] = service_ids
        if env_vars is not UNSET:
            field_dict["envVars"] = env_vars
        if secret_files is not UNSET:
            field_dict["secretFiles"] = secret_files
        if env_group_ids is not UNSET:
            field_dict["envGroupIds"] = env_group_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.build_source_git import BuildSourceGit  # noqa: PLC0415
        from ..models.build_source_image import BuildSourceImage  # noqa: PLC0415
        from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue  # noqa: PLC0415
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415
        from ..models.secret_file_input import SecretFileInput  # noqa: PLC0415

        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        name = d.pop("name")

        project_id = d.pop("projectId", UNSET)

        _git = d.pop("git", UNSET)
        git: BuildSourceGit | Unset
        if isinstance(_git, Unset):
            git = UNSET
        else:
            git = BuildSourceGit.from_dict(_git)

        _image = d.pop("image", UNSET)
        image: BuildSourceImage | Unset
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = BuildSourceImage.from_dict(_image)

        service_ids = cast(list[str], d.pop("serviceIds", UNSET))

        _env_vars = d.pop("envVars", UNSET)
        env_vars: list[EnvVarKeyGenerateValue | EnvVarKeyValue] | Unset = UNSET
        if _env_vars is not UNSET:
            env_vars = []
            for componentsschemasenv_var_input_array_item_data in _env_vars:

                def _parse_componentsschemasenv_var_input_array_item(
                    data: object,
                ) -> EnvVarKeyGenerateValue | EnvVarKeyValue:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemasenv_var_input_type_0 = EnvVarKeyValue.from_dict(data)

                        return componentsschemasenv_var_input_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasenv_var_input_type_1 = EnvVarKeyGenerateValue.from_dict(data)

                    return componentsschemasenv_var_input_type_1

                componentsschemasenv_var_input_array_item = _parse_componentsschemasenv_var_input_array_item(
                    componentsschemasenv_var_input_array_item_data
                )

                env_vars.append(componentsschemasenv_var_input_array_item)

        _secret_files = d.pop("secretFiles", UNSET)
        secret_files: list[SecretFileInput] | Unset = UNSET
        if _secret_files is not UNSET:
            secret_files = []
            for secret_files_item_data in _secret_files:
                secret_files_item = SecretFileInput.from_dict(secret_files_item_data)

                secret_files.append(secret_files_item)

        env_group_ids = cast(list[str], d.pop("envGroupIds", UNSET))

        build_source_post_input = cls(
            owner_id=owner_id,
            name=name,
            project_id=project_id,
            git=git,
            image=image,
            service_ids=service_ids,
            env_vars=env_vars,
            secret_files=secret_files,
            env_group_ids=env_group_ids,
        )

        build_source_post_input.additional_properties = d
        return build_source_post_input

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
