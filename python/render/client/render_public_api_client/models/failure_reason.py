from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.oom_killed import OomKilled


T = TypeVar("T", bound="FailureReason")


@_attrs_define
class FailureReason:
    """
    Attributes:
        evicted (bool):
        non_zero_exit (Union[Unset, int]): If present, the application exited with the specified non-zero status.
        early_exit (Union[Unset, bool]): If true, the application exited early. Services besides cron jobs should not
            exit unless receiving a `SIGTERM` signal from Render.
        oom_killed (Union[Unset, OomKilled]):
        timed_out_seconds (Union[Unset, int]):
        unhealthy (Union[Unset, str]):
        timed_out_reason (Union[Unset, str]):
    """

    evicted: bool
    non_zero_exit: Union[Unset, int] = UNSET
    early_exit: Union[Unset, bool] = UNSET
    oom_killed: Union[Unset, "OomKilled"] = UNSET
    timed_out_seconds: Union[Unset, int] = UNSET
    unhealthy: Union[Unset, str] = UNSET
    timed_out_reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        evicted = self.evicted

        non_zero_exit = self.non_zero_exit

        early_exit = self.early_exit

        oom_killed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.oom_killed, Unset):
            oom_killed = self.oom_killed.to_dict()

        timed_out_seconds = self.timed_out_seconds

        unhealthy = self.unhealthy

        timed_out_reason = self.timed_out_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evicted": evicted,
            }
        )
        if non_zero_exit is not UNSET:
            field_dict["nonZeroExit"] = non_zero_exit
        if early_exit is not UNSET:
            field_dict["earlyExit"] = early_exit
        if oom_killed is not UNSET:
            field_dict["oomKilled"] = oom_killed
        if timed_out_seconds is not UNSET:
            field_dict["timedOutSeconds"] = timed_out_seconds
        if unhealthy is not UNSET:
            field_dict["unhealthy"] = unhealthy
        if timed_out_reason is not UNSET:
            field_dict["timedOutReason"] = timed_out_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.oom_killed import OomKilled

        d = dict(src_dict)
        evicted = d.pop("evicted")

        non_zero_exit = d.pop("nonZeroExit", UNSET)

        early_exit = d.pop("earlyExit", UNSET)

        _oom_killed = d.pop("oomKilled", UNSET)
        oom_killed: Union[Unset, OomKilled]
        if isinstance(_oom_killed, Unset):
            oom_killed = UNSET
        else:
            oom_killed = OomKilled.from_dict(_oom_killed)

        timed_out_seconds = d.pop("timedOutSeconds", UNSET)

        unhealthy = d.pop("unhealthy", UNSET)

        timed_out_reason = d.pop("timedOutReason", UNSET)

        failure_reason = cls(
            evicted=evicted,
            non_zero_exit=non_zero_exit,
            early_exit=early_exit,
            oom_killed=oom_killed,
            timed_out_seconds=timed_out_seconds,
            unhealthy=unhealthy,
            timed_out_reason=timed_out_reason,
        )

        failure_reason.additional_properties = d
        return failure_reason

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
