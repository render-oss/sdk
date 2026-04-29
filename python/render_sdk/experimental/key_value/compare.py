"""Configuration comparison for Key Value instances."""

from render_sdk.public_api.models.cidr_block_and_description import (
    CidrBlockAndDescription,
)
from render_sdk.public_api.models.key_value_patch_input import KeyValuePATCHInput
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.maxmemory_policy import MaxmemoryPolicy
from render_sdk.public_api.types import UNSET

from .types import InstanceConfiguration, KeyValueInstance


def compare_instance_configuration(
    desired: InstanceConfiguration,
    current: KeyValueInstance,
) -> KeyValuePATCHInput | None:
    """Compare desired configuration against current state.

    Returns a patch payload containing only the fields that differ, or None if
    the current configuration already matches the desired configuration.

    Note: Only values that are explicitly set in desired are compared. If a desired
    value is None, then no change will be made to that value regardless of the current
    state.
    """
    new_plan: KeyValuePlan | None = None
    if desired.plan is not None and desired.plan != current.plan:
        new_plan = KeyValuePlan(desired.plan)

    new_maxmemory_policy: MaxmemoryPolicy | None = None
    if (
        desired.maxmemory_policy is not None
        and desired.maxmemory_policy != current.maxmemory_policy
    ):
        new_maxmemory_policy = desired.maxmemory_policy

    # None means "caller didn't specify"; an empty list means "clear the allowlist"
    new_ip_allow_list: list[CidrBlockAndDescription] | None = None
    if desired.ip_allow_list is not None:
        new_ip_allow_list = _compare_ip_allow_lists(
            desired.ip_allow_list, current.ip_allow_list
        )

    # Use explicit None checks so that an empty ip_allow_list (falsy) still
    # triggers an update when it differs from the current non-empty list.
    if (
        new_plan is not None
        or new_maxmemory_policy is not None
        or new_ip_allow_list is not None
    ):
        return KeyValuePATCHInput(
            plan=new_plan if new_plan is not None else UNSET,
            maxmemory_policy=(
                new_maxmemory_policy if new_maxmemory_policy is not None else UNSET
            ),
            ip_allow_list=new_ip_allow_list if new_ip_allow_list is not None else UNSET,
        )

    return None


def _compare_ip_allow_lists(
    desired: list[CidrBlockAndDescription],
    current: list[CidrBlockAndDescription],
) -> list[CidrBlockAndDescription] | None:
    """Compare two IP allow lists by CIDR block (descriptions are ignored).

    Returns None if the lists are equivalent, or the desired list if they differ.
    """
    if len(desired) != len(current):
        return desired

    desired_sorted = sorted(desired, key=lambda e: e.cidr_block)
    current_sorted = sorted(current, key=lambda e: e.cidr_block)

    if any(
        a.cidr_block != b.cidr_block
        for a, b in zip(desired_sorted, current_sorted, strict=False)
    ):
        return desired

    return None
