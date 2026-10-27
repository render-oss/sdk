#!/usr/bin/env python3
"""Unit tests for the request builders shared by the workflows clients."""

import pytest

from render.client._requests import (
    list_flow_runs_query,
    run_task_body,
    start_flow_run_body,
)
from render.client.types import ListFlowRunsParams
from render.public_api.models.flow_run_status import FlowRunStatus
from render.public_api.types import UNSET

# Each case is (input_data, idempotency_key, expected "input"/"idempotencyKey"
# fields of the serialized body). Tasks and flows share the cases so their
# request bodies stay in step.
_RUN_BODY_CASES = [
    ([1, 2], None, {"input": [1, 2]}),
    ({"a": 1}, None, {"input": {"a": 1}}),
    ([1], "order-42", {"input": [1], "idempotencyKey": "order-42"}),
]


@pytest.mark.parametrize("input_data,idempotency_key,expected", _RUN_BODY_CASES)
def test_run_task_body(input_data, idempotency_key, expected):
    body = run_task_body("wf/task", input_data, idempotency_key)
    assert body.to_dict() == {"task": "wf/task", **expected}


@pytest.mark.parametrize("input_data,idempotency_key,expected", _RUN_BODY_CASES)
def test_start_flow_run_body(input_data, idempotency_key, expected):
    body = start_flow_run_body("wf/flow", input_data, idempotency_key)
    assert body.to_dict() == {"flow": "wf/flow", **expected}


_ALL_UNSET_QUERY = {
    "limit": UNSET,
    "cursor": UNSET,
    "flow_slug": UNSET,
    "flow_id": UNSET,
    "status": UNSET,
    "owner_id": UNSET,
    "workflow_version_id": UNSET,
    "workflow_id": UNSET,
}


@pytest.mark.parametrize(
    "params,expected_overrides",
    [
        (None, {}),
        (ListFlowRunsParams(), {}),
        (ListFlowRunsParams(limit=5, cursor="c1"), {"limit": 5, "cursor": "c1"}),
        (
            ListFlowRunsParams(status=["running", FlowRunStatus.PAUSED]),
            {"status": [FlowRunStatus.RUNNING, FlowRunStatus.PAUSED]},
        ),
        (
            ListFlowRunsParams(
                flow_slug=["wf/flow"],
                flow_id=["flw-1"],
                owner_id=["tea-1"],
                workflow_version_id=["wfv-1"],
                workflow_id=["wfl-1"],
            ),
            {
                "flow_slug": ["wf/flow"],
                "flow_id": ["flw-1"],
                "owner_id": ["tea-1"],
                "workflow_version_id": ["wfv-1"],
                "workflow_id": ["wfl-1"],
            },
        ),
    ],
)
def test_list_flow_runs_query(params, expected_overrides):
    assert list_flow_runs_query(params) == {**_ALL_UNSET_QUERY, **expected_overrides}
