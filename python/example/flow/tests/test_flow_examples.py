"""Keep the public examples executable against the durability SDK."""

import copy

import pytest

from example.flow import main
from render.workflows._models.history import History
from render.workflows._models.task import InputResponse
from render.workflows.client import UDSClient
from render.workflows.durable_context import DurableFlowContext


def context(client, history=None, attempt=0):
    return DurableFlowContext(
        client,
        InputResponse(
            task_name="example",
            input_="",
            task_run_id="trn-example",
            is_workflow=True,
            attempt=attempt,
            history=history if history is not None else History(),
        ),
    )


@pytest.fixture
def client(mocker):
    return mocker.create_autospec(UDSClient, spec_set=True)


def test_inline_retry_stays_in_one_flow_attempt(client, mocker):
    sleep = mocker.patch("render.workflows.durable_context.time.sleep")
    with context(client) as ctx:
        assert main.inline_retry.func(ctx) == 3

    assert client.step_start.call_count == 1
    assert client.step_complete.call_count == 1
    assert [c.args[0].attempt for c in client.step_attempt.call_args_list] == [0, 1]
    assert [c.args[0] for c in sleep.call_args_list] == [0.1, 0.2]


def test_replay_reuses_completed_step(client, mocker):
    history = History()
    sleep = mocker.patch("render.workflows.durable_context.time.sleep")
    log_attempt = mocker.spy(main.logger, "info")

    with context(client, history) as ctx:
        assert main.inline_retry.func(ctx) == 3

    assert log_attempt.call_count == 3
    assert len(history.steps) == 1
    assert history.steps[0].completed_at is not None
    client.reset_mock()
    sleep.reset_mock()
    log_attempt.reset_mock()

    # Supply recorded history directly; this doesn't exercise backend recovery.
    with context(client, copy.deepcopy(history), attempt=1) as recovered:
        assert main.inline_retry.func(recovered) == 3

    log_attempt.assert_not_called()
    sleep.assert_not_called()
    client.step_start.assert_not_called()
    client.step_attempt.assert_not_called()
    client.step_complete.assert_not_called()


def test_retry_counter_resets_for_each_flow_run(client, mocker):
    mocker.patch("render.workflows.durable_context.time.sleep")
    for _ in range(2):
        client.reset_mock()
        with context(client) as ctx:
            assert main.inline_retry.func(ctx) == 3
        assert [c.args[0].attempt for c in client.step_attempt.call_args_list] == [0, 1]
