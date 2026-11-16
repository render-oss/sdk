from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue
    from ..models.env_var_key_value import EnvVarKeyValue
    from ..models.secret_file_input import SecretFileInput


T = TypeVar("T", bound="EnvGroupPOSTInput")


@_attrs_define
class EnvGroupPOSTInput:
    """
    Attributes:
        name (str):
        owner_id (str):
        env_vars (list[EnvVarKeyGenerateValue | EnvVarKeyValue]):
        secret_files (list[SecretFileInput] | Unset):
        service_ids (list[str] | Unset):
        environment_id (str | Unset):
    """

    name: str
    owner_id: str
    env_vars: list[EnvVarKeyGenerateValue | EnvVarKeyValue]
    secret_files: list[SecretFileInput] | Unset = UNSET
    service_ids: list[str] | Unset = UNSET
    environment_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415

        name = self.name

        owner_id = self.owner_id

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

        service_ids: list[str] | Unset = UNSET
        if not isinstance(self.service_ids, Unset):
            service_ids = self.service_ids

        environment_id = self.environment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ownerId": owner_id,
                "envVars": env_vars,
            }
        )
        if secret_files is not UNSET:
            field_dict["secretFiles"] = secret_files
        if service_ids is not UNSET:
            field_dict["serviceIds"] = service_ids
        if environment_id is not UNSET:
            field_dict["environmentId"] = environment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.env_var_key_generate_value import EnvVarKeyGenerateValue  # noqa: PLC0415
        from ..models.env_var_key_value import EnvVarKeyValue  # noqa: PLC0415
        from ..models.secret_file_input import SecretFileInput  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        owner_id = d.pop("ownerId")

        env_vars = []
        _env_vars = d.pop("envVars")
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

        service_ids = cast(list[str], d.pop("serviceIds", UNSET))

        environment_id = d.pop("environmentId", UNSET)

        env_group_post_input = cls(
            name=name,
            owner_id=owner_id,
            env_vars=env_vars,
            secret_files=secret_files,
            service_ids=service_ids,
            environment_id=environment_id,
        )

        env_group_post_input.additional_properties = d
        return env_group_post_input

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
