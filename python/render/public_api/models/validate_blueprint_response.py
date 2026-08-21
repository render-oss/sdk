from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validation_error import ValidationError
    from ..models.validation_plan_summary import ValidationPlanSummary


T = TypeVar("T", bound="ValidateBlueprintResponse")


@_attrs_define
class ValidateBlueprintResponse:
    """
    Attributes:
        valid (bool): If `true`, the Blueprint validated successfully. If `false`, at least one validation error
            occurred.
        errors (Union[Unset, list['ValidationError']]): A list of validation errors. Only present if `valid` is `false`.
        plan (Union[Unset, ValidationPlanSummary]):
    """

    valid: bool
    errors: Union[Unset, list["ValidationError"]] = UNSET
    plan: Union[Unset, "ValidationPlanSummary"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        valid = self.valid

        errors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        plan: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "valid": valid,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.validation_error import ValidationError
        from ..models.validation_plan_summary import ValidationPlanSummary

        d = dict(src_dict)
        valid = d.pop("valid")

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = ValidationError.from_dict(errors_item_data)

            errors.append(errors_item)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, ValidationPlanSummary]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = ValidationPlanSummary.from_dict(_plan)

        validate_blueprint_response = cls(
            valid=valid,
            errors=errors,
            plan=plan,
        )

        validate_blueprint_response.additional_properties = d
        return validate_blueprint_response

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
