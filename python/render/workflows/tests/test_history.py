from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from render.client.errors import FlowHistoryError, FlowHistoryErrorCode
from render.workflows._models.history import (
    History,
    validate_attempts,
    validate_steps,
)
from render.workflows._models.step import (
    StepAttemptRecord,
    StepError,
    StepKey,
    StepRecord,
    StepType,
)
from render.workflows._models.task import InputResponse

STARTED = datetime(2026, 10, 12, 10, 0, 0, tzinfo=timezone.utc)
ENDED = datetime(2026, 10, 12, 10, 0, 1, tzinfo=timezone.utc)
Code = FlowHistoryErrorCode


def step(seq, *, done=True, sub_key="", workflow_attempt=0):
    return StepRecord(
        step_key=StepKey(seq=seq, sub_key=sub_key),
        type_=StepType.INLINE,
        workflow_attempt=workflow_attempt,
        started_at=STARTED,
        task_name="effect",
        completed_at=ENDED if done else None,
    )


def failed(seq):
    """A step that finished with an error, which ends the run."""
    return replace(step(seq), error=StepError(name="ValueError", message="declined"))


def attempt(seq, number, *, workflow_attempt=0, ended_at=ENDED):
    return StepAttemptRecord(
        step_key=StepKey(seq=seq),
        attempt=number,
        workflow_attempt=workflow_attempt,
        error=StepError(name="ConnectionError", message="timeout"),
        ended_at=ended_at,
    )


def step_dict(seq, *, done=True):
    d = {
        "step_key": {"seq": seq},
        "type": "inline",
        "workflow_attempt": 0,
        "started_at": "2026-10-12T10:00:00Z",
    }
    if done:
        d["completed_at"] = "2026-10-12T10:00:01Z"
    return d


def attempt_dict(seq, number, *, ended_at="2026-10-12T10:00:01Z"):
    return {
        "step_key": {"seq": seq},
        "attempt": number,
        "workflow_attempt": 0,
        "error": {"name": "ConnectionError", "message": "timeout"},
        "ended_at": ended_at,
    }


def test_input_response_parses_history():
    response = InputResponse.from_dict(
        {
            "task_name": "wf",
            "input": "",
            "history": {
                "steps": [step_dict(0), step_dict(1, done=False)],
                "step_attempts": [attempt_dict(1, 0)],
            },
        }
    )
    history = response.history
    assert isinstance(history, History)
    assert history.steps[0].completed_at == ENDED
    assert history.steps[1].completed_at is None
    assert history.attempts(StepKey(seq=1))[0].ended_at == ENDED


def test_history_sorts_steps_and_groups_attempts_by_step():
    history = History.from_dict(
        {
            "steps": [step_dict(2, done=False), step_dict(0), step_dict(1)],
            "step_attempts": [attempt_dict(2, 1), attempt_dict(2, 0)],
        }
    )

    assert [s.step_key.seq for s in history.steps] == [0, 1, 2]
    assert list(history.step_attempts) == [StepKey(seq=2)]
    assert [a.attempt for a in history.attempts(StepKey(seq=2))] == [0, 1]
    history.validate()


def test_history_lookups():
    history = History(
        steps=[step(0), step(1, sub_key="b", done=False)],
        step_attempts={StepKey(seq=1, sub_key="b"): [attempt(1, 0)]},
    )

    assert history.step(StepKey(seq=1, sub_key="b")) is history.steps[1]
    assert history.step(StepKey(seq=1)) is None
    assert history.step(StepKey(seq=2)) is None
    assert history.attempts(StepKey(seq=0)) == []


def test_history_lookup_fails_when_a_seq_has_several_steps():
    history = History(
        steps=[step(0), step(1, sub_key="a"), step(1, sub_key="b", done=False)],
        step_attempts={StepKey(seq=1, sub_key="b"): [attempt(1, 0)]},
    )
    history.validate()

    with pytest.raises(FlowHistoryError) as raised:
        history.step(StepKey(seq=1, sub_key="b"))
    assert (raised.value.code, raised.value.step_key) == (
        Code.SEQ_SUB_KEYS,
        StepKey(seq=1, sub_key="b"),
    )


@pytest.mark.parametrize(
    "steps, attempts, expected",
    [
        ([], [], 0),
        ([step(0)], [], 1),
        ([step(0, workflow_attempt=2)], [], 3),
        ([step(0, done=False)], [], 1),
        ([step(0, done=False)], [0, 1], 2),
        ([step(0, done=False)], [1], 2),
    ],
    ids=["new", "finished", "finished-later", "cut-off", "after-failures", "gap"],
)
def test_get_step_state_finds_the_attempt_a_replay_is_on(steps, attempts, expected):
    history = History(
        steps=steps,
        step_attempts={StepKey(seq=0): [attempt(0, n) for n in attempts]},
    )
    recorded_step, current_attempt = history.get_step_state(StepKey(seq=0))
    assert recorded_step is (steps[0] if steps else None)
    assert current_attempt == expected


def test_empty_history_is_valid():
    History().validate()


@pytest.mark.parametrize(
    "steps, code, step_key",
    [
        ([step(1)], Code.STEP_SEQ, StepKey(seq=1)),
        ([step(0), step(2)], Code.STEP_SEQ, StepKey(seq=2)),
        ([step(0, done=False), step(1)], Code.AFTER_OPEN, StepKey(seq=0)),
        ([failed(0), step(1)], Code.AFTER_TERMINAL, StepKey(seq=0)),
        ([step(0), failed(1)], Code.TERMINAL, StepKey(seq=1)),
    ],
)
def test_validate_steps_rejects_bad_sequencing(steps, code, step_key):
    with pytest.raises(FlowHistoryError, match=f"^{code.value} ") as raised:
        validate_steps(steps, {})
    assert (raised.value.code, raised.value.step_key) == (code, step_key)


def test_validate_steps_allows_steps_that_share_a_seq():
    validate_steps([step(0), step(1, sub_key="a"), step(1, sub_key="b"), step(2)], {})


@pytest.mark.parametrize(
    "attempts", [[], [attempt(1, 0)]], ids=["no-attempts", "attempts"]
)
def test_validate_steps_checks_the_last_steps_attempts(mocker, attempts):
    check = mocker.patch("render.workflows._models.history.validate_attempts")
    steps = [step(0), step(1, done=False)]

    validate_steps(steps, {StepKey(seq=1): attempts} if attempts else {})

    check.assert_called_once_with(steps[1], attempts)


@pytest.mark.parametrize(
    "steps",
    [[], [step(0)], [step(0), step(1, done=False)]],
    ids=["no-steps", "finished", "other-step-open"],
)
def test_validate_steps_ignores_attempts_of_other_steps(steps):
    validate_steps(steps, {StepKey(seq=0): [attempt(0, 1)]})


@pytest.mark.parametrize(
    "numbers", [[0, 0], [1, 0], [-1]], ids=["repeat", "backwards", "negative"]
)
def test_validate_attempts_rejects_misnumbered_attempts(numbers):
    with pytest.raises(FlowHistoryError) as raised:
        validate_attempts(step(0, done=False), [attempt(0, n) for n in numbers])
    assert (raised.value.code, raised.value.step_key) == (
        Code.ATTEMPT_SEQ,
        StepKey(seq=0),
    )


@pytest.mark.parametrize(
    "made",
    [
        attempt(0, 0, workflow_attempt=0),
        attempt(0, 0, ended_at=STARTED - timedelta(seconds=1)),
    ],
    ids=["earlier-flow-attempt", "ended-before-start"],
)
def test_validate_attempts_rejects_attempts_made_before_the_step(made):
    with pytest.raises(FlowHistoryError) as raised:
        validate_attempts(step(0, done=False, workflow_attempt=1), [made])
    assert (raised.value.code, raised.value.step_key) == (
        Code.ATTEMPT_STEP,
        StepKey(seq=0),
    )


def test_validate_attempts_allows_retries_of_an_open_step():
    validate_attempts(
        step(0, done=False),
        [attempt(0, 0), attempt(0, 1, workflow_attempt=1)],
    )


@pytest.mark.parametrize("numbers", [[1], [0, 2]], ids=["late-start", "gap"])
def test_validate_attempts_allows_attempts_cut_off_by_a_crash(numbers):
    validate_attempts(step(0, done=False), [attempt(0, n) for n in numbers])


def test_validate_attempts_ignores_a_finished_steps_attempts():
    validate_attempts(step(0), [attempt(0, 1)])


@pytest.mark.parametrize(
    "wire_type, parsed",
    [
        ("inline", StepType.INLINE),
        ("sleep", StepType.SLEEP),
        ("later", StepType.UNKNOWN),
    ],
)
def test_step_record_maps_unknown_types_to_unknown(wire_type, parsed):
    record = StepRecord.from_dict({**step_dict(0, done=False), "type": wire_type})
    assert record.type_ is parsed
    assert (record.task_name, record.completed_at) == (None, None)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2026-10-12T10:00:00Z", STARTED),
        ("2026-10-12T10:00:00.5+00:00", STARTED.replace(microsecond=500000)),
        ("2026-10-12T10:00:00.123456789Z", STARTED.replace(microsecond=123456)),
    ],
)
def test_attempt_record_parses_rfc3339_times(value, expected):
    record = StepAttemptRecord.from_dict(attempt_dict(0, 0, ended_at=value))
    assert record.ended_at == expected


@pytest.mark.parametrize("value", ["soon", "2026-10-12T10:00:00"])
def test_bad_times_fail_to_parse(value):
    with pytest.raises(ValueError):
        StepAttemptRecord.from_dict(attempt_dict(0, 0, ended_at=value))


def test_step_record_decodes_its_base64_input_and_output():
    record = StepRecord.from_dict(
        {**step_dict(0, done=True), "input": "WyJvLTEiXQ==", "output": "eyJpZCI6IDF9"}
    )
    assert (record.input_, record.output) == ('["o-1"]', '{"id": 1}')


@pytest.mark.parametrize("field", ["input", "output"])
def test_bad_base64_fails_to_parse(field):
    with pytest.raises(ValueError):
        StepRecord.from_dict({**step_dict(0, done=True), field: "not base64!"})


@pytest.mark.parametrize(
    "step_key, message",
    [
        (None, "WFL-HIST-STEP-SEQ: bad"),
        (StepKey(seq=3), "WFL-HIST-STEP-SEQ [seq=3]: bad"),
        (StepKey(seq=3, sub_key="a"), "WFL-HIST-STEP-SEQ [seq=3 sub_key='a']: bad"),
    ],
)
def test_history_error_message_leads_with_its_code_and_step(step_key, message):
    assert str(FlowHistoryError(Code.STEP_SEQ, "bad", step_key)) == message


def started():
    history = History()
    history.record_start(
        StepKey(seq=0), task_name="effect", started_at=STARTED, encoded_input="[]"
    )
    return history


def test_history_records_a_step_as_the_sdk_server_does():
    history = started()
    assert history.steps == [replace(step(0, done=False), input_="[]")]
    history.record_attempt(attempt(0, 0))
    assert history.get_step_state(StepKey(seq=0)) == (history.steps[0], 1)

    history.record_complete(StepKey(seq=0), completed_at=ENDED, output='"ok"')

    (finished,) = history.steps
    assert (finished.completed_at, finished.output) == (ENDED, '"ok"')
    assert history.attempts(StepKey(seq=0)) == []
    history.validate()


def test_history_keeps_the_first_record_of_each_write():
    history = started()
    history.record_start(StepKey(seq=0), task_name="other", started_at=ENDED)
    history.record_attempt(attempt(0, 0))
    history.record_attempt(replace(attempt(0, 0), workflow_attempt=1))
    history.record_complete(StepKey(seq=0), completed_at=ENDED)
    history.record_complete(StepKey(seq=0), completed_at=ENDED, output='"late"')

    (recorded,) = history.steps
    assert (recorded.task_name, recorded.output) == ("effect", None)


@pytest.mark.parametrize("write", ["attempt", "complete"])
def test_history_rejects_a_write_to_a_step_without_a_start(write):
    with pytest.raises(ValueError, match="has no recorded start"):
        if write == "attempt":
            History().record_attempt(attempt(0, 0))
        else:
            History().record_complete(StepKey(seq=0), completed_at=ENDED)


def test_history_rejects_a_completion_before_the_start():
    history = started()
    with pytest.raises(ValueError, match="before it started"):
        history.record_complete(
            StepKey(seq=0),
            completed_at=STARTED - timedelta(seconds=1),
        )
