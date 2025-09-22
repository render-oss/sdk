from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autoscaling_config import AutoscalingConfig


T = TypeVar("T", bound="AutoscalingConfigChanged")


@_attrs_define
class AutoscalingConfigChanged:
    """
    Attributes:
        to_config (AutoscalingConfig):
        from_config (Union[Unset, AutoscalingConfig]):
    """

    to_config: "AutoscalingConfig"
    from_config: Union[Unset, "AutoscalingConfig"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        to_config = self.to_config.to_dict()

        from_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.from_config, Unset):
            from_config = self.from_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "toConfig": to_config,
            }
        )
        if from_config is not UNSET:
            field_dict["fromConfig"] = from_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_config import AutoscalingConfig

        d = dict(src_dict)
        to_config = AutoscalingConfig.from_dict(d.pop("toConfig"))

        _from_config = d.pop("fromConfig", UNSET)
        from_config: Union[Unset, AutoscalingConfig]
        if isinstance(_from_config, Unset):
            from_config = UNSET
        else:
            from_config = AutoscalingConfig.from_dict(_from_config)

        autoscaling_config_changed = cls(
            to_config=to_config,
            from_config=from_config,
        )

        autoscaling_config_changed.additional_properties = d
        return autoscaling_config_changed

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
