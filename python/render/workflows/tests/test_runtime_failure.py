"""Runtime failures stop attempts without becoming replayed step outcomes."""

import contextlib
import json
from unittest.mock import create_autospec

import pytest

from render.client.errors import FlowNestedStepError, FlowUnreachableError
from render.workflows._models.step import StepStartResponse
from render.workflows._models.task import InputResponse
from render.workflows.app import Workflows
from render.workflows.client import Status, UDSClient
from render.workflows.executor import TaskExecutor
from render.workflows.task import Retry


def flow_input(steps=(), attempt=0):
    return InputResponse.from_dict(
        {
            "task_name": "wf",
            "input": "",
            "task_run_id": "trn-1",
            "root_task_run_id": "trn-1",
            "is_workflow": True,
            "attempt": attempt,
            "history": {"steps": list(steps), "step_attempts": []},
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("callback_lost", [False, True])
async def test_recovery_can_rerun_a_step_after_its_fatal_attempt_is_superseded(
    callback_lost,
):
    # The scheduler may recover before accepting the old attempt's callback,
    # even when renderd acknowledged it into its WAL. Feed the next execution
    # only the persisted open step; scheduler arbitration is a backend concern.
    client = create_autospec(UDSClient, spec_set=True)
    client.step_start.return_value = StepStartResponse(applied=True)
    app = Workflows()
    violate = True
    calls = []

    @app.flow
    def wf(ctx):
        def work():
            calls.append("work")
            if violate:
                with contextlib.suppress(FlowNestedStepError):
                    ctx.step("illegal", lambda: None)
            return "ok"

        with contextlib.suppress(FlowNestedStepError):
            return ctx.step(
                "work", work, retry=Retry(max_retries=1, wait_duration_ms=0)
            )
        return "swallowed"

    if callback_lost:
        client.post_callback.side_effect = ConnectionError("callback lost")
    with pytest.raises(ConnectionError if callback_lost else FlowNestedStepError):
        await TaskExecutor(app._registry, client).execute(
            "wf", [], input_response=flow_input()
        )

    assert client.post_callback.call_args.args[0].status is Status.ERROR
    client.step_attempt.assert_not_called()
    client.step_complete.assert_not_called()
    started = client.step_start.call_args.args[0].to_dict()
    persisted = json.loads(
        json.dumps({**started, "type": "inline", "workflow_attempt": 0})
    )

    # Non-deterministic work belongs in steps, so it need not encounter the
    # same violation again. No terminal step record constrains this replay.
    violate = False
    client.reset_mock()
    client.post_callback.side_effect = None
    assert (
        await TaskExecutor(app._registry, client).execute(
            "wf", [], input_response=flow_input([persisted], attempt=1)
        )
        == "ok"
    )
    assert calls == ["work", "work"]
    client.step_start.assert_not_called()
    client.step_complete.assert_called_once()
    assert client.post_callback.call_args.args[0].status is Status.SUCCESS


@pytest.mark.asyncio
async def test_infrastructure_error_in_a_step_reaches_the_executor_as_system_failure():
    client = create_autospec(UDSClient, spec_set=True)
    app = Workflows()
    error = FlowUnreachableError("history service unavailable")

    @app.flow
    def wf(ctx):
        def work():
            raise error

        with contextlib.suppress(FlowUnreachableError):
            ctx.step("work", work, retry=Retry(max_retries=2, wait_duration_ms=0))
        return "swallowed"

    with pytest.raises(FlowUnreachableError) as raised:
        await TaskExecutor(app._registry, client).execute(
            "wf", [], input_response=flow_input()
        )
    assert raised.value is error
    assert client.post_callback.call_args.args[0] == error.to_callback_request()
    client.step_attempt.assert_not_called()
    client.step_complete.assert_not_called()
