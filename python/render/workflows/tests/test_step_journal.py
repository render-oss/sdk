"""Tests for the step journal a flow attempt writes through."""

from datetime import timedelta

import pytest

from render.client.errors import (
    ClientError,
    FlowBadRequestError,
    FlowCancelledError,
    FlowLimitError,
    FlowUnreachableError,
    ServerError,
    TerminalFlowError,
)
from render.workflows._models.history import History
from render.workflows._models.step import StepError, StepKey
from render.workflows._utils import clock
from render.workflows._utils.step_journal import RunFailure, StepJournal
from render.workflows.client import UDSClient
from render.workflows.durable_context import RunningStep

STEP = RunningStep(step_key=StepKey(seq=0), name="charge", retry=None)
ERROR = StepError(name="ValueError", message="boom", stack="")


@pytest.fixture
def client(mocker):
    return mocker.create_autospec(UDSClient, spec_set=True)


@pytest.fixture
def failure():
    return RunFailure()


@pytest.fixture
def journal(client, failure):
    return StepJournal(client, History(), session_id="trn-1", failure=failure)


def test_a_write_is_recorded_before_it_is_sent(journal, client):
    recorded_when_sent = []
    client.step_start.side_effect = lambda _: recorded_when_sent.append(
        journal.step_state(STEP.step_key)[0] is not None
    )

    journal.start(STEP, "[]")

    assert recorded_when_sent == [True]


def test_a_failed_write_fails_the_run(journal, client, failure):
    client.step_start.side_effect = ServerError("down")

    with pytest.raises(FlowUnreachableError) as raised:
        journal.start(STEP)

    assert failure.error is raised.value


def test_cancelled_failure_completion_stops_the_run(journal, client, failure):
    journal.start(STEP)
    client.step_complete.side_effect = ClientError(
        "record step failed with status 409",
        status_code=409,
        json_body={"code": "run_cancelled"},
    )

    with pytest.raises(FlowCancelledError) as raised:
        journal.finish_attempt(
            journal.create_failed_attempt(
                STEP, ERROR, started_at=clock.now(), workflow_attempt=0
            )
        )

    assert failure.error is raised.value


@pytest.mark.parametrize(
    "status, code", [(409, "missing_start"), (400, None)], ids=["409", "400"]
)
def test_a_rejected_write_fails_the_run_with_a_terminal_error(
    journal, client, failure, status, code
):
    client.step_start.side_effect = ClientError(
        "record step failed", status_code=status, json_body={"code": code}
    )

    with pytest.raises(FlowBadRequestError) as raised:
        journal.start(STEP)

    assert type(raised.value) is FlowBadRequestError
    assert isinstance(raised.value, TerminalFlowError)
    assert raised.value.code == code
    assert failure.error is raised.value


def test_a_write_over_a_limit_fails_the_run_with_a_limit_error(
    journal, client, failure
):
    client.step_start.side_effect = ClientError(
        "record step failed with status 422",
        status_code=422,
        json_body={
            "code": "workflow_payload_too_large",
            "message": "too large",
            "limit": 1024,
            "value": 2048,
        },
    )

    with pytest.raises(FlowLimitError) as raised:
        journal.start(STEP)

    assert (raised.value.code, raised.value.limit, raised.value.value) == (
        "flow_payload_too_large",
        1024,
        2048,
    )
    assert failure.error is raised.value


def test_a_step_never_completes_before_its_recorded_start(journal, client, mocker):
    started_at = journal.start(STEP)
    # This worker's clock runs behind the one that started the step.
    mocker.patch.object(clock, "now", return_value=started_at - timedelta(seconds=5))

    journal.complete(STEP, "1")

    (step,) = journal._history.steps
    assert step.completed_at == started_at


def test_the_first_run_failure_wins():
    failure = RunFailure()
    first = FlowUnreachableError("first")

    assert failure.stop(first) is first
    assert failure.stop(FlowUnreachableError("second")) is first
    with pytest.raises(FlowUnreachableError) as raised:
        failure.raise_if_set()
    assert raised.value is first


def test_a_higher_priority_run_failure_overrides_an_earlier_one():
    failure = RunFailure()
    failure.stop(FlowUnreachableError("write lost"))
    terminal = TerminalFlowError("step failed")

    assert failure.stop(terminal) is terminal
    assert failure.stop(TerminalFlowError("again")) is terminal
    assert failure.stop(FlowUnreachableError("later")) is terminal

    cancel = FlowCancelledError("cancelled")
    assert failure.stop(cancel) is cancel
    assert failure.stop(FlowCancelledError("again")) is cancel
    assert failure.stop(TerminalFlowError("later")) is cancel
