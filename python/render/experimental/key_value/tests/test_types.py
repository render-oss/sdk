"""Tests for the handwritten Key Value type aliases."""

from typing import get_args

from render.experimental.key_value.types import Plan
from render.public_api.models.key_value_plan import KeyValuePlan

# "custom" is a managed plan that cannot be requested when provisioning.
UNPROVISIONABLE_PLANS = {"custom"}


def test_plan_covers_every_provisionable_generated_plan():
    """Plan is handwritten, so a schema-side plan addition can silently omit it.

    Without this, a new plan name accepted by the API is rejected by mypy at
    every InstanceConfiguration(plan=...) call site.
    """
    generated = {plan.value for plan in KeyValuePlan} - UNPROVISIONABLE_PLANS
    assert set(get_args(Plan)) == generated


def test_plan_values_construct_the_generated_enum():
    """compare.py and provider.py pass a Plan straight to KeyValuePlan()."""
    for value in get_args(Plan):
        assert KeyValuePlan(value).value == value
