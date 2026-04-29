"""Tests for compare_instance_configuration."""

import pytest

from render_sdk.experimental.key_value.compare import compare_instance_configuration
from render_sdk.experimental.key_value.types import (
    InstanceConfiguration,
    KeyValueInstance,
    Plan,
)
from render_sdk.public_api.models.cidr_block_and_description import (
    CidrBlockAndDescription,
)
from render_sdk.public_api.models.database_status import DatabaseStatus
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.maxmemory_policy import MaxmemoryPolicy
from render_sdk.public_api.types import UNSET


def make_current(
    plan: Plan = "free",
    maxmemory_policy: MaxmemoryPolicy = MaxmemoryPolicy.ALLKEYS_LRU,
    ip_allow_list: list[CidrBlockAndDescription] | None = None,
):
    """Create a minimal mock current instance for comparison tests."""
    return KeyValueInstance(
        id="red-abc",
        status=DatabaseStatus.AVAILABLE,
        plan=KeyValuePlan(plan),
        maxmemory_policy=maxmemory_policy,
        ip_allow_list=(
            ip_allow_list
            if ip_allow_list is not None
            else [
                CidrBlockAndDescription(
                    cidr_block="0.0.0.0/0", description="Allow all traffic"
                )
            ]
        ),
    )


@pytest.fixture
def current():
    return make_current()


class TestCompareInstanceConfiguration:
    def test_returns_none_if_no_desired_values_set_explicitly(self, current):
        desired = InstanceConfiguration()

        assert compare_instance_configuration(desired, current) is None

    def test_returns_none_if_desired_values_match_exactly(self, current):
        desired = InstanceConfiguration(
            plan="free",
            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU,
            ip_allow_list=[
                CidrBlockAndDescription(
                    cidr_block="0.0.0.0/0", description="Allow all traffic"
                )
            ],
        )

        assert compare_instance_configuration(desired, current) is None

    def test_returns_diff_if_changes_are_needed(self, current):
        desired = InstanceConfiguration(
            plan="starter",
            maxmemory_policy=MaxmemoryPolicy.NOEVICTION,
            ip_allow_list=[],
        )

        result = compare_instance_configuration(desired, current)

        assert result is not None
        assert result.plan == KeyValuePlan.STARTER
        assert result.maxmemory_policy == MaxmemoryPolicy.NOEVICTION
        assert result.ip_allow_list == []

    def test_returns_partial_diff_if_only_some_options_changed(self, current):
        desired = InstanceConfiguration(
            plan="free",
            maxmemory_policy=MaxmemoryPolicy.NOEVICTION,
        )

        result = compare_instance_configuration(desired, current)

        assert result is not None
        assert result.maxmemory_policy == MaxmemoryPolicy.NOEVICTION
        # plan is unchanged so should not be in the patch
        assert result.plan is UNSET

    def test_only_compares_cidr_block_and_ignores_description_for_ip_allow_list(
        self, current
    ):
        desired = InstanceConfiguration(
            ip_allow_list=[
                CidrBlockAndDescription(
                    cidr_block="0.0.0.0/0",
                    description="Different description shouldn't be a diff",
                )
            ],
        )

        assert compare_instance_configuration(desired, current) is None

    def test_handles_net_new_entry_in_ip_allowlist(self, current):
        new_list = [
            CidrBlockAndDescription(
                cidr_block="0.0.0.0/0", description="Allow all traffic"
            ),
            CidrBlockAndDescription(cidr_block="127.0.0.0/0", description="localhost"),
        ]
        desired = InstanceConfiguration(ip_allow_list=new_list)

        result = compare_instance_configuration(desired, current)

        assert result is not None
        assert result.ip_allow_list == new_list

    def test_empty_desired_ip_allow_list_triggers_update_when_current_is_non_empty(
        self, current
    ):
        desired = InstanceConfiguration(ip_allow_list=[])

        result = compare_instance_configuration(desired, current)

        assert result is not None
        assert result.ip_allow_list == []

    def test_no_update_when_both_ip_allow_lists_are_empty(self):
        current = make_current(ip_allow_list=[])
        desired = InstanceConfiguration(ip_allow_list=[])

        assert compare_instance_configuration(desired, current) is None
