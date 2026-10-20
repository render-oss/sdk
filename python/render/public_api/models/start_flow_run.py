from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_input_type_1 import FlowInputType1


T = TypeVar("T", bound="StartFlowRun")


@_attrs_define
class StartFlowRun:
    """
    Attributes:
        flow (str): A flow slug in the format workflow-slug/flow-name. An optional version can be appended (workflow-
            slug/flow-name:version). If no version is provided, the latest version is used. Cannot be blank. Example: my-
            workflow-slug/my-flow.
        input_ (Union['FlowInputType1', list[Any]]): Input data for a flow. Can be either an array (for positional
            arguments) or an object (for named parameters).
        idempotency_key (Union[Unset, str]): A client-generated key that makes starting a task run safe to retry.
            Repeating a request with the same key within 24 hours returns the task run that the first request started
            instead of starting another one; the repeated request's input is ignored. Keys are scoped to a workflow. Omit
            the key to always start a new run. Example: 6b2f1f7a-6a0e-4f6f-9d1a-2b1d0d5f6c11.
    """

    flow: str
    input_: Union["FlowInputType1", list[Any]]
    idempotency_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flow = self.flow

        input_: Union[dict[str, Any], list[Any]]
        if isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_.to_dict()

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow": flow,
                "input": input_,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotencyKey"] = idempotency_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flow_input_type_1 import FlowInputType1

        d = dict(src_dict)
        flow = d.pop("flow")

        def _parse_input_(data: object) -> Union["FlowInputType1", list[Any]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_flow_input_type_0 = cast(list[Any], data)

                return componentsschemas_flow_input_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_flow_input_type_1 = FlowInputType1.from_dict(data)

            return componentsschemas_flow_input_type_1

        input_ = _parse_input_(d.pop("input"))

        idempotency_key = d.pop("idempotencyKey", UNSET)

        start_flow_run = cls(
            flow=flow,
            input_=input_,
            idempotency_key=idempotency_key,
        )

        start_flow_run.additional_properties = d
        return start_flow_run

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
