from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_run_error_details_code import FlowRunErrorDetailsCode
from ..models.flow_run_error_details_kind import FlowRunErrorDetailsKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowRunErrorDetails")


@_attrs_define
class FlowRunErrorDetails:
    """
    Attributes:
        code (FlowRunErrorDetailsCode):
        message (str):
        seq (int | Unset):
        sub_key (str | Unset):
        flow_attempt (int | Unset):
        kind (FlowRunErrorDetailsKind | Unset):
        expected (str | Unset):
        actual (str | Unset):
        limit (int | Unset):
        value (int | Unset):
    """

    code: FlowRunErrorDetailsCode
    message: str
    seq: int | Unset = UNSET
    sub_key: str | Unset = UNSET
    flow_attempt: int | Unset = UNSET
    kind: FlowRunErrorDetailsKind | Unset = UNSET
    expected: str | Unset = UNSET
    actual: str | Unset = UNSET
    limit: int | Unset = UNSET
    value: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        seq = self.seq

        sub_key = self.sub_key

        flow_attempt = self.flow_attempt

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        expected = self.expected

        actual = self.actual

        limit = self.limit

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if seq is not UNSET:
            field_dict["seq"] = seq
        if sub_key is not UNSET:
            field_dict["subKey"] = sub_key
        if flow_attempt is not UNSET:
            field_dict["flowAttempt"] = flow_attempt
        if kind is not UNSET:
            field_dict["kind"] = kind
        if expected is not UNSET:
            field_dict["expected"] = expected
        if actual is not UNSET:
            field_dict["actual"] = actual
        if limit is not UNSET:
            field_dict["limit"] = limit
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = FlowRunErrorDetailsCode(d.pop("code"))

        message = d.pop("message")

        seq = d.pop("seq", UNSET)

        sub_key = d.pop("subKey", UNSET)

        flow_attempt = d.pop("flowAttempt", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: FlowRunErrorDetailsKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = FlowRunErrorDetailsKind(_kind)

        expected = d.pop("expected", UNSET)

        actual = d.pop("actual", UNSET)

        limit = d.pop("limit", UNSET)

        value = d.pop("value", UNSET)

        flow_run_error_details = cls(
            code=code,
            message=message,
            seq=seq,
            sub_key=sub_key,
            flow_attempt=flow_attempt,
            kind=kind,
            expected=expected,
            actual=actual,
            limit=limit,
            value=value,
        )

        flow_run_error_details.additional_properties = d
        return flow_run_error_details

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
