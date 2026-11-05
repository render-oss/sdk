"""Tests for flow registration and the flow context."""

import base64
import contextlib
import json
from datetime import datetime, timedelta
from typing import Any

import pytest

from render.client.errors import (
    ClientError,
    DeterminismError,
    ExecutionError,
    FlowBadRequestError,
    FlowCancelledError,
    FlowLimitError,
    FlowNestedStepError,
    FlowUnreachableError,
    RateLimitError,
    RenderError,
    ServerError,
    StepError,
    TerminalFlowError,
)
from render.client.errors import TimeoutError as SdkTimeoutError
from render.workflows._models.step import (
    StepAttemptResponse,
    StepKey,
    StepOutcome,
    StepSuccess,
    StepType,
)
from render.workflows._models.task import (
    DeterminismDetails,
    DeterminismKind,
    InputResponse,
    TaskErrorReason,
)
from render.workflows._models.wire import parse_time
from render.workflows.app import Workflows
from render.workflows.client import CallbackRequest, Status, UDSClient
from render.workflows.context import FlowRunMetadata
from render.workflows.durable_context import DurableFlowContext
from render.workflows.executor import TaskExecutor
from render.workflows.flow import FlowDefinition
from render.workflows.runner import register_async
from render.workflows.task import Retry


@pytest.fixture
def app():
    return Workflows(
        default_retry=Retry(max_retries=3, wait_duration_ms=1000),
        default_timeout=300,
    )


@pytest.fixture
def mock_client(mocker):
    mock = mocker.create_autospec(UDSClient, spec_set=True)
    mock.post_callback = mocker.AsyncMock()
    return mock


def flow_input(**overrides) -> InputResponse:
    fields: dict[str, Any] = {
        "task_name": "wf",
        "input_": "",
        "task_run_id": "trn-1",
        "root_task_run_id": "trn-1",
        "is_workflow": True,
        "attempt": 2,
    }
    fields.update(overrides)
    return InputResponse(**fields)


@pytest.fixture
def ctx(mock_client):
    return DurableFlowContext(mock_client, flow_input())


# Registration


def test_flow_registers_with_the_workflow_flag(app):
    @app.flow
    def wf(ctx, order_id: str) -> str:
        return order_id

    assert isinstance(wf, FlowDefinition)
    info = app._registry.get_task("wf")
    assert info.workflow is True
    assert [p.name for p in info.parameters] == ["order_id"]


def test_flow_ignores_the_default_retry(app):
    @app.flow
    def wf(ctx) -> None:
        pass

    options = app._registry.get_task("wf").options
    assert options.retry is None
    assert options.timeout_seconds == 300


def test_flow_rejects_a_retry_policy(app):
    with pytest.raises(ValueError, match="retry policy is not allowed"):
        app.flow(retry=Retry(max_retries=1, wait_duration_ms=10))


def test_flow_must_be_sync(app):
    with pytest.raises(ValueError, match="must be a sync function"):

        @app.flow
        async def wf(ctx) -> None:
            pass


def test_input_response_parses_workflow_fields():
    parsed = InputResponse.from_dict(
        {"task_name": "wf", "input": "", "is_workflow": True, "attempt": 3}
    )
    assert parsed.is_workflow is True
    assert parsed.attempt == 3


@pytest.mark.asyncio
async def test_registration_sends_the_workflow_flag(mocker, app):
    @app.task
    def plain(ctx) -> None:
        pass

    @app.flow
    def wf(ctx) -> None:
        pass

    mocker.patch(
        "render.workflows.runner.get_task_registry", return_value=app._registry
    )
    client = mocker.patch("render.workflows.runner.UDSClient").return_value
    client.register_tasks = mocker.AsyncMock()

    await register_async("unused.sock")

    tasks = {
        t["name"]: t for t in client.register_tasks.call_args[0][0].to_dict()["tasks"]
    }
    assert tasks["wf"]["workflow"] is True
    assert "retry" not in tasks["wf"]["options"]
    assert "workflow" not in tasks["plain"]


# The flow context


def test_invoking_a_registered_task_is_not_supported_yet(app, ctx):
    @app.task
    def charge(ctx, order_id: str) -> str:
        return order_id

    with pytest.raises(NotImplementedError, match="registered task"):
        ctx.invoke(charge, "o-1")
    assert ctx._next_seq == 0


def test_sleeping_is_not_supported_yet(ctx):
    with pytest.raises(NotImplementedError, match="ctx.sleep: .* isn't supported yet"):
        ctx.sleep(timedelta(seconds=1))
    assert ctx._next_seq == 0


def test_invoke_takes_a_registered_task(ctx):
    def charge(order_id: str) -> str:
        return order_id

    with pytest.raises(TypeError, match="Use ctx.step"):
        ctx.invoke(charge, "o-1")


def test_step_takes_a_plain_function(app, ctx):
    @app.task
    def charge(ctx, order_id: str) -> str:
        return order_id

    with pytest.raises(TypeError, match="Use ctx.invoke to run it"):
        ctx.step("charge", charge, "o-1")


def test_an_async_step_is_not_supported_yet(ctx):
    async def charge(order_id: str) -> str:
        return order_id

    with pytest.raises(TypeError, match="Async steps aren't supported yet"):
        ctx.step("charge", charge, "o-1")


def test_a_flow_cannot_run_a_flow(app, ctx):
    @app.flow
    def other(ctx) -> None:
        pass

    with pytest.raises(TypeError, match="can't invoke another flow"):
        ctx.invoke(other)
    with pytest.raises(TypeError, match="can't run another flow"):
        ctx.step("other", other)


def test_a_step_takes_its_name_first(ctx):
    def charge(order_id: str) -> str:
        return order_id

    with pytest.raises(TypeError, match="takes the step's name first"):
        ctx.step(charge, "o-1")


def test_a_step_name_cannot_be_empty(ctx):
    with pytest.raises(ValueError, match="non-empty step name"):
        ctx.step("", lambda: 1)


def test_a_step_is_recorded_under_its_given_name(ctx, mock_client):
    def charge() -> str:
        return "ok"

    ctx.step("charge_card", charge)

    start = requests(mock_client)[0]
    assert start["task_name"] == "charge_card"


def test_function_arguments_must_be_positional(ctx):
    def charge(order_id: str) -> str:
        return order_id

    with pytest.raises(TypeError, match="positionally"):
        ctx.step("charge", charge, order_id="o-1")


STEP_WRITES = ("step_start", "step_attempt", "step_complete")


def requests(mock_client):
    """The /step-inline/* writes, in order, as wire dicts tagged with their route."""
    return [
        {"kind": name.removeprefix("step_"), **args[0].to_dict()}
        for name, args, _ in mock_client.method_calls
        if name in STEP_WRITES
    ]


def decode(value):
    """A base64 JSON value from the wire."""
    return json.loads(base64.b64decode(value))


def final_error(complete):
    """The StepError of a completion's final attempt."""
    return decode(complete["outcome"]["final_attempt"]["error"]["data"])


@pytest.mark.parametrize("circular", [False, True], ids=["datetime", "circular"])
def test_invalid_step_arguments_are_recorded_as_a_catchable_failure(
    ctx, mock_client, mocker, circular
):
    value = []
    if circular:
        value.append(value)
    else:
        value.append(datetime(2026, 10, 20))
    error_name = "ValueError" if circular else "TypeError"
    calls = 0
    sleep = mocker.patch("render.workflows.durable_context.time").sleep

    def charge(arg: Any) -> Any:
        nonlocal calls
        calls += 1
        return arg

    with pytest.raises(
        StepError, match=f"Step 'charge' failed with {error_name}"
    ) as raised:
        ctx.step(
            "charge",
            charge,
            value,
            retry=Retry(max_retries=3, wait_duration_ms=10),
        )

    assert calls == 0
    sleep.assert_not_called()
    assert ctx._next_seq == 1
    assert ctx._in_flight is False
    assert (raised.value.step_name, raised.value.error_name) == ("charge", error_name)
    assert (raised.value.session_id, raised.value.step_key) == (
        "trn-1",
        StepKey(seq=0),
    )

    start, complete = requests(mock_client)
    assert start["kind"] == "start"
    assert start["step_key"] == {"seq": 0, "sub_key": ""}
    assert start["task_name"] == "charge"
    assert "input" not in start
    assert complete["kind"] == "complete"
    assert complete["session_id"] == "trn-1"
    assert complete["key"] == {"seq": 0, "sub_key": ""}
    final = complete["outcome"]["final_attempt"]
    assert (final["session_id"], final["key"], final["attempt"]) == (
        "trn-1",
        {"seq": 0, "sub_key": ""},
        0,
    )
    assert final["ended_at"] == complete["outcome"]["completed_at"]
    assert final["data"]["workflow_attempt"] == 2
    assert final_error(complete)["name"] == error_name
    assert final_error(complete)["message"] in str(raised.value)
    assert error_name in final_error(complete)["stack"]

    # Once recorded, the failure is catchable and a later step can run.
    assert ctx.step("next", lambda: "ok") == "ok"
    assert ctx.run_failure is None
    assert len(requests(mock_client)) == 4


def test_steps_run_in_the_order_the_flow_calls_them(ctx, mock_client):
    def wf() -> list[str]:
        return [
            ctx.step("first", lambda: "a"),
            ctx.step("second", lambda: "b"),
        ]

    assert wf() == ["a", "b"]
    assert [
        (r["kind"], r.get("step_key", r.get("key"))["seq"])
        for r in requests(mock_client)
    ] == [
        ("start", 0),
        ("complete", 0),
        ("start", 1),
        ("complete", 1),
    ]


def test_steps_are_numbered_in_the_order_they_start(ctx):
    with ctx.start_step("first", None) as (first, _):
        pass
    with ctx.start_step("second", None) as (second, _):
        pass
    assert (first.step_key.seq, second.step_key.seq) == (0, 1)


# Inline steps


@pytest.fixture
def sleeps(mocker):
    return mocker.patch("render.workflows.durable_context.time").sleep


def test_inline_step_records_its_start_and_outcome(ctx, mock_client):
    def charge(order_id: str, total: int) -> dict:
        return {"id": f"ch-{order_id}", "total": total}

    result = ctx.step("charge", charge, "o-1", 30)

    assert result == {"id": "ch-o-1", "total": 30}
    start, complete = requests(mock_client)
    assert start["kind"] == "start"
    assert start["task_name"] == "charge"
    assert decode(start["input"]) == ["o-1", 30]
    assert "started_at" in start
    assert complete["kind"] == "complete"
    assert complete["outcome"]["output"]["serializer"] == 1
    assert decode(complete["outcome"]["output"]["data"]) == {
        "id": "ch-o-1",
        "total": 30,
    }
    assert "final_attempt" not in complete["outcome"]


def test_success_without_an_output_sends_only_its_completion_time():
    outcome = StepOutcome(completed_at="2026-10-12T10:00:01Z", result=StepSuccess())
    assert outcome.to_dict() == {"completed_at": "2026-10-12T10:00:01Z"}


def test_lambda_step_uses_its_name(ctx, mock_client):
    ctx.step("receipt_id", lambda: "r-1")
    assert requests(mock_client)[0]["task_name"] == "receipt_id"


@pytest.mark.parametrize("value", [None, "YWJj", {"items": [None, "caf\u00e9", 3]}])
def test_inline_step_sends_base64_payloads(monkeypatch, tmp_path, value):
    client = UDSClient(str(tmp_path / "test.sock"))
    writes = []

    def request(*, method, path, body, **_):
        writes.append((method, path, json.loads(json.dumps(body))))
        return {"applied": True}

    monkeypatch.setattr("render.workflows.client.request_json_sync", request)
    ctx = DurableFlowContext(client, flow_input())
    assert ctx.step("echo", lambda item: item, value) == value

    start, complete = writes
    assert start[:2] == ("POST", "/step-inline/start")
    assert decode(start[2]["input"]) == [value]
    completed_at = complete[2]["outcome"]["completed_at"]
    assert complete == (
        "POST",
        "/step-inline/complete",
        {
            "session_id": "trn-1",
            "key": {"seq": 0, "sub_key": ""},
            "outcome": {
                "completed_at": completed_at,
                "output": {
                    "serializer": 1,
                    "data": base64.b64encode(json.dumps(value).encode()).decode(),
                },
            },
        },
    )


def test_result_is_returned_as_a_replay_would_see_it(ctx):
    def pair() -> tuple:
        return (1, 2)

    assert ctx.step("pair", pair) == [1, 2]


@pytest.mark.asyncio
async def test_a_failed_step_fails_the_flow_run(app, mock_client):
    def declined() -> None:
        raise ValueError("card declined")

    @app.flow
    def wf(ctx) -> None:
        ctx.step("declined", declined)

    with pytest.raises(RuntimeError, match="card declined"):
        await TaskExecutor(app._registry, mock_client).execute(
            "wf", [], input_response=flow_input()
        )

    callback = mock_client.post_callback.call_args.args[0]
    assert callback.status == Status.ERROR
    assert "Step 'declined' failed with ValueError: card declined" in callback.error


@pytest.mark.parametrize("applied", [None, 0, 1, "true"])
def test_step_attempt_response_requires_a_strict_boolean_applied(applied):
    with pytest.raises(TypeError, match="must be a boolean"):
        StepAttemptResponse.from_dict({"applied": applied})


def test_step_attempt_response_requires_applied():
    with pytest.raises(KeyError, match="applied"):
        StepAttemptResponse.from_dict({})


@pytest.mark.parametrize("applied", [True, False], ids=["applied", "duplicate"])
def test_retry_records_each_failure_before_retrying(ctx, mock_client, sleeps, applied):
    received = []

    def flaky(values):
        received.append(values)
        values.append(len(received))
        if len(received) < 3:
            raise ConnectionError(f"timeout {len(received) - 1}")
        return values

    mock_client.step_attempt.return_value = StepAttemptResponse(applied=applied)

    result = ctx.step(
        "flaky",
        flaky,
        [],
        retry=Retry(max_retries=2, wait_duration_ms=100, backoff_scaling=2),
    )

    assert result == [3]
    assert received == [[1], [2], [3]]
    attempts = [
        request for request in requests(mock_client) if request["kind"] == "attempt"
    ]
    assert [a["attempt"] for a in attempts] == [0, 1]
    assert [call.args[0] for call in sleeps.call_args_list] == [0.1, 0.2]


def unencodable_arg(arg):
    return "ok"


def out_of_retries():
    raise ConnectionError("timeout")


def terminal():
    raise TerminalFlowError("card declined")


def unencodable_result():
    return object()


@pytest.mark.parametrize(
    "fn, args, error_name",
    [
        (unencodable_arg, (object(),), "TypeError"),
        (out_of_retries, (), "ConnectionError"),
        (unencodable_result, (), "TypeError"),
    ],
    ids=["unencodable-arg", "out-of-retries", "unencodable-result"],
)
def test_unacknowledged_failure_stops_the_attempt(
    ctx, mock_client, sleeps, fn, args, error_name
):
    lost = ServerError("write was not acknowledged")
    mock_client.step_complete.side_effect = lost

    # Workflow code cannot catch the step failure until it is durable.
    with pytest.raises(
        FlowUnreachableError, match="write was not acknowledged"
    ) as raised:
        ctx.step("charge", fn, *args)
    assert raised.value.__cause__ is lost

    with pytest.raises(FlowUnreachableError) as later:
        ctx.step("later", must_not_run)
    assert later.value is raised.value


@pytest.mark.parametrize(
    "fn, args",
    [(out_of_retries, ()), (unencodable_arg, (object(),)), (unencodable_result, ())],
)
def test_step_failure_becomes_catchable_only_after_completion_ack(
    ctx, mock_client, fn, args
):
    pending = []

    def acknowledge(request):
        pending.append(ctx.run_failure)

    mock_client.step_complete.side_effect = acknowledge
    with pytest.raises(StepError):
        ctx.step("fn", fn, *args)

    assert pending == [None]
    assert ctx.run_failure is None
    assert ctx.step("fallback", lambda: "fallback") == "fallback"


@pytest.mark.parametrize("error_type", [TerminalFlowError, FlowUnreachableError])
def test_runtime_failure_stops_without_recording(ctx, mock_client, sleeps, error_type):
    error = error_type("runtime stopped")

    def fail():
        raise error

    with pytest.raises(error_type) as raised:
        ctx.step("fail", fail, retry=Retry(max_retries=3, wait_duration_ms=10))

    assert raised.value is error
    assert ctx.run_failure is error
    assert [r["kind"] for r in requests(mock_client)] == ["start"]
    sleeps.assert_not_called()
    with pytest.raises(error_type) as later:
        ctx.step("later", must_not_run)
    assert later.value is error


def flaky_once():
    calls = 0

    def flaky():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise ConnectionError("timeout")
        return "ok"

    return flaky


@pytest.mark.parametrize("write", ["step_start", "step_attempt", "step_complete"])
def test_failed_step_write_fails_the_run(ctx, mock_client, sleeps, write):
    getattr(mock_client, write).side_effect = ServerError("write was not acknowledged")
    retry = Retry(max_retries=1, wait_duration_ms=0)

    with pytest.raises(FlowUnreachableError, match="not acknowledged") as raised:
        ctx.step("charge", flaky_once(), retry=retry)
    assert isinstance(raised.value.__cause__, ServerError)
    sent = len(requests(mock_client))

    # The flow caught the error, but the run can't go on past the write.
    with pytest.raises(FlowUnreachableError) as later:
        ctx.step("later", must_not_run)
    assert later.value is raised.value
    assert len(requests(mock_client)) == sent


def test_failed_attempt_write_does_not_retry(ctx, mock_client, sleeps):
    calls = 0

    def flaky():
        nonlocal calls
        calls += 1
        raise ConnectionError("timeout")

    mock_client.step_attempt.side_effect = ServerError("write was not acknowledged")

    with pytest.raises(FlowUnreachableError, match="not acknowledged"):
        ctx.step("flaky", flaky, retry=Retry(max_retries=2, wait_duration_ms=100))

    assert calls == 1
    assert [request["kind"] for request in requests(mock_client)] == [
        "start",
        "attempt",
    ]
    sleeps.assert_not_called()


@pytest.mark.parametrize("max_retries", [0, -1])
def test_inline_step_raises_step_error_after_its_last_attempt(
    ctx, mock_client, sleeps, max_retries
):
    def declined() -> None:
        raise ValueError("card declined")

    with pytest.raises(StepError, match="card declined") as raised:
        ctx.step(
            "declined",
            declined,
            retry=Retry(max_retries=max_retries, wait_duration_ms=10),
        )
    error = raised.value
    assert str(error) == "Step 'declined' failed with ValueError: card declined"
    assert (error.type, error.err_type, error.step_name, error.error_name) == (
        "flow",
        "runtime",
        "declined",
        "ValueError",
    )
    assert (error.session_id, error.step_key) == ("trn-1", StepKey(seq=0))
    assert type(error) is StepError
    assert isinstance(error, ExecutionError)
    assert not isinstance(error, TerminalFlowError)

    writes = requests(mock_client)
    assert [w["kind"] for w in writes] == ["start", "complete"]
    assert final_error(writes[-1])["message"] == "card declined"
    assert writes[-1]["outcome"]["final_attempt"]["attempt"] == max(max_retries, 0)
    assert "output" not in writes[-1]["outcome"]


@pytest.mark.parametrize("character", ["x", "界"])
def test_failed_step_records_the_end_of_a_long_stack(ctx, mock_client, character):
    message = "card declined " + character * 20_000

    def charge() -> None:
        raise ValueError(message)

    with pytest.raises(ExecutionError):
        ctx.step("charge", charge)

    (_, complete) = requests(mock_client)
    stack = final_error(complete)["stack"]
    assert 15_997 <= len(stack.encode("utf-8")) <= 16_000
    assert stack.startswith("…")
    assert stack.endswith(character * 5_000 + "\n")
    assert final_error(complete)["message"] == message


class CardDeclined(Exception):
    def __init__(self, code, retry_after=None):
        super().__init__(f"card declined: {code}")
        self.code = code
        self.retry_after = retry_after


def test_failed_step_records_the_fields_its_error_set(ctx, mock_client):
    def charge() -> None:
        error = CardDeclined("insufficient_funds")
        # What add_note sets, on Pythons that have it.
        vars(error)["__notes__"] = ["not recorded"]
        raise error

    with pytest.raises(StepError) as raised:
        ctx.step("charge", charge)

    assert raised.value.error_data == {
        "code": "insufficient_funds",
        "retry_after": None,
    }
    (_, complete) = requests(mock_client)
    assert json.loads(final_error(complete)["data"]) == raised.value.error_data


@pytest.mark.parametrize(
    "error",
    [ValueError("plain"), CardDeclined(object(), retry_after=datetime(2026, 10, 30))],
    ids=["no-fields", "unencodable"],
)
def test_failed_step_without_encodable_fields_records_no_data(ctx, mock_client, error):
    def charge() -> None:
        raise error

    with pytest.raises(StepError) as raised:
        ctx.step("charge", charge)

    assert raised.value.error_data is None
    (_, complete) = requests(mock_client)
    assert "data" not in final_error(complete)


@pytest.mark.parametrize(
    "fields, expected",
    [
        (
            {"code": "expired", "bad": object(), "retry": 2},
            {"code": "expired", "retry": 2},
        ),
        ({"large": "x" * 16_000, "code": "expired"}, {"code": "expired"}),
        (
            {"first": "x" * 10_000, "second": "y" * 10_000, "code": "expired"},
            {"first": "x" * 10_000, "code": "expired"},
        ),
        ({"unicode": "界" * 4_000, "code": "expired"}, {"code": "expired"}),
    ],
    ids=["mixed-fields", "oversized-field", "total-budget", "unicode-budget"],
)
def test_failed_step_preserves_fields_that_encode_and_fit(
    ctx, mock_client, fields, expected
):
    def charge() -> None:
        error = ValueError("declined")
        vars(error).update(fields)
        raise error

    with pytest.raises(StepError) as raised:
        ctx.step("charge", charge)

    assert raised.value.error_data == expected
    (_, complete) = requests(mock_client)
    data = final_error(complete)["data"]
    assert len(data.encode("utf-8")) <= 16_000
    assert json.loads(data) == expected


def test_missing_validated_step_input_is_terminal(ctx, mock_client, monkeypatch):
    monkeypatch.setattr(ctx, "_checked_args", lambda *args: None)

    with pytest.raises(TerminalFlowError, match="step input is missing") as raised:
        ctx.step("charge", must_not_run)

    assert ctx.run_failure is raised.value
    assert [w["kind"] for w in requests(mock_client)] == ["start"]


@pytest.mark.parametrize(
    "data, expected",
    [('{"code": "expired"}', {"code": "expired"}), ("not json", "not json")],
    ids=["json", "raw"],
)
def test_replayed_step_failure_carries_its_recorded_data(mock_client, data, expected):
    step = recorded_step(0, "charge", [], error=("CardDeclined", "card declined"))
    step["error"]["data"] = data

    with pytest.raises(StepError) as raised:
        replay_ctx(mock_client, [step]).step("charge", must_not_run)

    assert raised.value.error_data == expected
    assert requests(mock_client) == []


def test_inline_step_fails_once_its_retries_max_out(ctx, mock_client, sleeps):
    calls = 0

    def flaky():
        nonlocal calls
        calls += 1
        raise ConnectionError(f"timeout {calls - 1}")

    with pytest.raises(StepError, match="timeout 2"):
        ctx.step("flaky", flaky, retry=Retry(max_retries=2, wait_duration_ms=100))

    assert calls == 3
    assert sleeps.call_count == 2
    # Each retried failure writes an attempt entry, and the last one completes
    # the step instead.
    writes = requests(mock_client)
    assert [w["kind"] for w in writes] == ["start", "attempt", "attempt", "complete"]
    assert [(w["attempt"], w["error"]["message"]) for w in writes[1:3]] == [
        (0, "timeout 0"),
        (1, "timeout 1"),
    ]
    assert writes[-1]["outcome"]["final_attempt"]["attempt"] == 2
    assert final_error(writes[-1])["message"] == "timeout 2"


def test_terminal_flow_error_is_an_execution_error():
    error = TerminalFlowError("card declined")
    assert isinstance(error, ExecutionError)
    assert (error.type, error.step_name, error.step_key, str(error)) == (
        "flow",
        None,
        None,
        "card declined",
    )


def test_task_run_error_is_an_execution_error():
    from render.client.errors import TaskRunError

    error = TaskRunError("Subtask failed: boom")
    assert isinstance(error, ExecutionError)
    assert (error.type, error.err_type, str(error)) == (
        "task",
        None,
        "Subtask failed: boom",
    )


def test_inline_step_without_retry_runs_once(ctx, mock_client, sleeps):
    def declined() -> None:
        raise ValueError("card declined")

    with pytest.raises(StepError):
        ctx.step("declined", declined)

    assert [w["kind"] for w in requests(mock_client)] == ["start", "complete"]
    sleeps.assert_not_called()


def test_inline_step_with_an_unencodable_result_is_not_retried(
    ctx, mock_client, sleeps
):
    calls = 0

    def charge() -> object:
        nonlocal calls
        calls += 1
        return object()

    with pytest.raises(StepError) as raised:
        ctx.step("charge", charge, retry=Retry(max_retries=3, wait_duration_ms=10))
    assert raised.value.error_name == "TypeError"

    assert calls == 1
    writes = requests(mock_client)
    assert [w["kind"] for w in writes] == ["start", "complete"]
    assert final_error(writes[-1])["name"] == "TypeError"
    sleeps.assert_not_called()


def test_inline_step_gets_its_arguments_through_the_wire_encoding(ctx):
    items = ["a"]
    received = []

    def mutate(values: list, pair: list) -> None:
        values.append("b")
        received.append(pair)

    ctx.step("mutate", mutate, items, (1, 2))
    assert items == ["a"]
    assert received == [[1, 2]]


def test_ctx_call_inside_a_step_fails_without_retrying(ctx, mock_client, sleeps):
    calls = 0
    inner_calls = 0

    def inner() -> None:
        nonlocal inner_calls
        inner_calls += 1

    def nested() -> None:
        nonlocal calls
        calls += 1
        ctx.step("inner", inner)

    with pytest.raises(
        FlowNestedStepError, match="can't be called within a step: step 'nested'"
    ) as raised:
        ctx.step("nested", nested, retry=Retry(max_retries=3, wait_duration_ms=10))

    assert calls == 1
    assert inner_calls == 0
    assert ctx._in_flight is False
    assert ctx.run_failure is raised.value
    writes = requests(mock_client)
    assert [w["kind"] for w in writes] == ["start"]
    sleeps.assert_not_called()


def test_a_step_that_replaces_a_terminal_error_fails_without_retrying(
    ctx, mock_client, sleeps
):
    calls = 0

    def nested() -> None:
        nonlocal calls
        calls += 1
        try:
            ctx.step("inner", lambda: None)
        except FlowNestedStepError:
            raise RuntimeError("wrapped") from None

    with pytest.raises(FlowNestedStepError, match="within a step") as raised:
        ctx.step("nested", nested, retry=Retry(max_retries=3, wait_duration_ms=10))

    assert calls == 1
    assert ctx.run_failure is raised.value
    writes = requests(mock_client)
    assert [w["kind"] for w in writes] == ["start"]
    sleeps.assert_not_called()


def test_ctx_call_inside_a_step_fails_the_run_even_if_the_step_catches_it(
    ctx, mock_client, sleeps
):
    def nested() -> str:
        try:
            ctx.step("inner", lambda: None)
        except FlowNestedStepError:
            return "caught"
        return "ran"

    with pytest.raises(FlowNestedStepError, match="within a step") as raised:
        ctx.step("nested", nested, retry=Retry(max_retries=3, wait_duration_ms=10))
    assert ctx.run_failure is raised.value
    assert [w["kind"] for w in requests(mock_client)] == ["start"]
    sleeps.assert_not_called()
    with pytest.raises(FlowNestedStepError, match="within a step") as later:
        ctx.step("after", lambda: None)
    assert later.value is raised.value


def test_terminal_error_fails_without_retrying(ctx, mock_client, sleeps):
    calls = 0
    fatal = TerminalFlowError("card declined")

    def charge() -> None:
        nonlocal calls
        calls += 1
        raise fatal

    with pytest.raises(TerminalFlowError, match="card declined") as raised:
        ctx.step("charge", charge, retry=Retry(max_retries=3, wait_duration_ms=10))

    assert raised.value is fatal
    assert ctx.run_failure is fatal
    assert calls == 1
    assert [w["kind"] for w in requests(mock_client)] == ["start"]
    sleeps.assert_not_called()


@pytest.mark.parametrize("fn", [out_of_retries, unencodable_result])
@pytest.mark.asyncio
async def test_caught_step_failure_succeeds(app, mock_client, sleeps, fn):
    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)
    later_ran = catch_all_flow(app, fn)

    assert await execute_flow(app, mock_client) == "carried on"
    assert later_ran == [True]
    assert step_seqs(mock_client) == {0, 1}
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status is Status.SUCCESS


@pytest.mark.parametrize("retries", [None, 0, 2])
def test_caught_exhausted_step_runs_fallback_and_replays(
    ctx, mock_client, sleeps, retries
):
    calls = []

    def declined():
        calls.append("declined")
        raise ValueError("card declined")

    def fallback():
        calls.append("fallback")
        return "recovered"

    options = (
        {}
        if retries is None
        else {"retry": Retry(max_retries=retries, wait_duration_ms=0)}
    )

    def run(context):
        with context:
            try:
                context.step("declined", declined, **options)
            except StepError as error:
                assert error.step_name == "declined"
                assert error.error_name == "ValueError"
                return context.step("fallback", fallback)
        pytest.fail("expected the failed step to raise")

    assert run(ctx) == "recovered"
    assert calls == ["declined"] * ((retries or 0) + 1) + ["fallback"]
    assert ctx.run_failure is None
    history = [
        recorded_step(0, "declined", [], error=("ValueError", "card declined")),
        recorded_step(1, "fallback", [], output="recovered"),
    ]
    mock_client.reset_mock()
    calls.clear()
    assert run(replay_ctx(mock_client, history)) == "recovered"
    assert calls == []
    assert requests(mock_client) == []


@pytest.mark.parametrize("encoding", ["input", "output"])
def test_caught_encoding_failure_replays_without_reexecuting(
    ctx, mock_client, encoding
):
    calls = []

    def invalid(value=None):
        calls.append("invalid")
        return object()

    args = (object(),) if encoding == "input" else ()

    def run(context):
        with context:
            with pytest.raises(StepError) as error:
                context.step("invalid", invalid, *args)
            assert error.value.error_name == "TypeError"
            return context.step("fallback", lambda: "recovered")

    assert run(ctx) == "recovered"
    assert calls == ([] if encoding == "input" else ["invalid"])
    # Replay the history this execution actually recorded, including its error.
    response = flow_input(history=ctx._journal._history)
    mock_client.reset_mock()
    calls.clear()
    assert run(DurableFlowContext(mock_client, response)) == "recovered"
    assert calls == []
    assert requests(mock_client) == []


@pytest.mark.parametrize(
    "error_name",
    [
        "DeterminismError",
        "FlowCancelledError",
        "FlowUnreachableError",
        "TerminalFlowError",
    ],
)
def test_user_step_error_names_are_catchable_on_first_run_and_replay(
    ctx, mock_client, error_name
):
    error_type = type(error_name, (Exception,), {})

    def fails():
        raise error_type("user failure")

    def run(context, fn):
        with context:
            with pytest.raises(StepError) as error:
                context.step("fails", fn)
            assert error.value.error_name == error_name
            assert context.run_failure is None

    run(ctx, fails)
    mock_client.reset_mock()
    replay = DurableFlowContext(mock_client, flow_input(history=ctx._journal._history))
    run(replay, must_not_run)
    assert requests(mock_client) == []


def test_raising_a_caught_step_error_records_the_current_step(ctx, mock_client, sleeps):
    with pytest.raises(StepError) as first:
        ctx.step("first", out_of_retries)
    original = first.value
    original_fields = vars(original).copy()
    calls = []

    def raise_again():
        calls.append(True)
        raise original

    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)
    with pytest.raises(StepError) as second:
        ctx.step("second", raise_again, retry=Retry(max_retries=1, wait_duration_ms=0))

    assert calls == [True, True]
    assert vars(original) == original_fields
    assert original.step_key == StepKey(seq=0)
    assert second.value is not original
    assert second.value.step_name == "second"
    assert second.value.step_key == StepKey(seq=1)
    assert second.value.error_name == "StepError"
    writes = requests(mock_client)
    assert [r["kind"] for r in writes] == [
        "start",
        "complete",
        "start",
        "attempt",
        "complete",
    ]
    assert writes[-1]["key"] == {"seq": 1, "sub_key": ""}
    assert writes[-1]["outcome"]["final_attempt"]["attempt"] == 1
    assert final_error(writes[-1])["message"] == str(original)
    assert ctx.run_failure is None
    assert ctx.step("fallback", lambda: "fallback") == "fallback"


def test_replay_after_failed_step_ack_runs_caught_fallback(mock_client):
    history = [recorded_step(0, "declined", [], error=("ValueError", "card declined"))]
    with replay_ctx(mock_client, history) as context:
        with pytest.raises(StepError, match="card declined"):
            context.step("declined", must_not_run)
        assert context.step("fallback", lambda: "recovered") == "recovered"
    assert step_seqs(mock_client) == {1}


def test_failed_write_stops_the_step(ctx, mock_client):
    lost = ServerError("record step failed to connect")
    mock_client.step_start.side_effect = lost
    ran = False

    def charge() -> None:
        nonlocal ran
        ran = True

    with pytest.raises(FlowUnreachableError) as raised:
        ctx.step("charge", charge)
    assert raised.value.__cause__ is lost
    # The client already retried it, so the context doesn't again.
    assert mock_client.step_start.call_count == 1
    assert not ran


def succeeds():
    return "ok"


def catch_all_flow(app, fn):
    """Register a flow that swallows every ctx error, carries on to a
    later step, and returns normally. Returns a list the later step appends to
    if it runs."""
    later_ran = []

    def later() -> None:
        later_ran.append(True)

    @app.flow
    def wf(ctx) -> str:
        with contextlib.suppress(Exception):
            ctx.step("first", fn, retry=Retry(max_retries=1, wait_duration_ms=0))
        with contextlib.suppress(Exception):
            ctx.step("later", later)
        return "carried on"

    return later_ran


async def execute_flow(app, mock_client):
    return await TaskExecutor(app._registry, mock_client).execute(
        "wf", [], input_response=flow_input()
    )


def step_seqs(mock_client):
    return {r.get("step_key", r.get("key"))["seq"] for r in requests(mock_client)}


@pytest.mark.parametrize(
    "fn, mock_config, error, match",
    [
        (terminal, {}, TerminalFlowError, "card declined"),
        (
            terminal,
            {"step_complete.side_effect": ServerError("complete not acknowledged")},
            TerminalFlowError,
            "card declined",
        ),
        (
            out_of_retries,
            {"step_complete.side_effect": ServerError("complete not acknowledged")},
            FlowUnreachableError,
            "complete not acknowledged",
        ),
        (
            succeeds,
            {
                "step_start.side_effect": ClientError(
                    "record step failed with status 409",
                    status_code=409,
                    json_body={"code": "missing_start"},
                )
            },
            FlowBadRequestError,
            "status 409",
        ),
        (
            succeeds,
            {
                "step_complete.side_effect": ClientError(
                    "record step failed with status 400"
                )
            },
            FlowBadRequestError,
            "status 400",
        ),
        (
            # Runtime failures do not attempt a step completion.
            terminal,
            {
                "step_complete.side_effect": ClientError(
                    "record step failed with status 422", status_code=422
                )
            },
            TerminalFlowError,
            "card declined",
        ),
        (
            out_of_retries,
            {
                "step_complete.side_effect": ClientError(
                    "record step failed with status 409",
                    status_code=409,
                    json_body={"code": "run_cancelled"},
                )
            },
            FlowCancelledError,
            "status 409",
        ),
    ],
    ids=[
        "terminal-acknowledged",
        "terminal-then-unreachable",
        "ordinary-then-unreachable",
        "rejected-write",
        "bad-request",
        "terminal-then-rejected",
        "ordinary-then-cancelled",
    ],
)
@pytest.mark.asyncio
async def test_a_failure_the_flow_catches_still_fails_the_run(
    app, mock_client, sleeps, fn, mock_config, error, match
):
    mock_client.configure_mock(**mock_config)
    later_ran = catch_all_flow(app, fn)

    with pytest.raises(error, match=match) as raised:
        await execute_flow(app, mock_client)

    # Exactly this error, not a subclass: e.g. a rejected write isn't a cancel.
    assert type(raised.value) is error
    assert not later_ran
    assert step_seqs(mock_client) == {0}
    if error is FlowCancelledError:
        # The run's outcome is the user's cancel, not this attempt's to report.
        mock_client.post_callback.assert_not_awaited()
        return
    mock_client.post_callback.assert_awaited_once()
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.error == str(raised.value)
    assert callback.reason == (
        TaskErrorReason.SYSTEM if error is FlowUnreachableError else None
    )


@pytest.mark.parametrize(
    "code, write",
    [
        (TaskErrorReason.WORKFLOW_PAYLOAD_TOO_LARGE, "step_complete"),
        (TaskErrorReason.WORKFLOW_STEP_LIMIT_EXCEEDED, "step_start"),
    ],
    ids=["payload", "steps"],
)
@pytest.mark.asyncio
async def test_a_flow_limit_fails_the_run_with_its_reason(
    app, mock_client, code, write
):
    getattr(mock_client, write).side_effect = ClientError(
        "record step failed with status 422",
        status_code=422,
        json_body={"code": code.value, "message": "over", "limit": 10, "value": 11},
    )
    later_ran = catch_all_flow(app, succeeds)

    with pytest.raises(FlowLimitError) as raised:
        await execute_flow(app, mock_client)

    assert not later_ran
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.error == str(raised.value)
    assert (callback.reason, callback.limit, callback.value) == (code, 10, 11)


@pytest.mark.parametrize(
    "fn, write, lost",
    [
        (succeeds, "step_start", ServerError("record step failed to connect")),
        (out_of_retries, "step_attempt", SdkTimeoutError("record step timed out")),
        (succeeds, "step_complete", RateLimitError("record step failed with 429")),
    ],
    ids=["start", "attempt", "complete"],
)
@pytest.mark.asyncio
async def test_an_unreachable_server_ends_the_attempt_with_a_system_error(
    app, mock_client, sleeps, fn, write, lost
):
    mock_client.configure_mock(**{f"{write}.side_effect": lost})
    later_ran = catch_all_flow(app, fn)

    with pytest.raises(FlowUnreachableError) as raised:
        await execute_flow(app, mock_client)

    assert raised.value.__cause__ is lost
    assert not later_ran
    assert step_seqs(mock_client) == {0}
    mock_client.post_callback.assert_awaited_once()
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.reason == TaskErrorReason.SYSTEM
    assert callback.error == str(raised.value)


@pytest.mark.asyncio
async def test_an_unreachable_server_still_ends_the_attempt_if_the_callback_fails(
    app, mock_client, sleeps
):
    mock_client.step_start.side_effect = ServerError("record step failed to connect")
    mock_client.post_callback.side_effect = ServerError("post callback failed")
    catch_all_flow(app, succeeds)

    with pytest.raises(FlowUnreachableError):
        await execute_flow(app, mock_client)


@pytest.mark.parametrize(
    "fn, write",
    [
        (succeeds, "step_start"),
        (out_of_retries, "step_attempt"),
        (succeeds, "step_complete"),
        (out_of_retries, "step_complete"),
    ],
    ids=["start", "attempt", "complete", "out-of-retries"],
)
@pytest.mark.asyncio
async def test_a_cancelled_run_stops_the_attempt_without_a_callback(
    app, mock_client, sleeps, fn, write
):
    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)
    getattr(mock_client, write).side_effect = ClientError(
        "record step failed with status 409",
        status_code=409,
        json_body={"code": "run_cancelled"},
    )
    later_ran = catch_all_flow(app, fn)

    with pytest.raises(FlowCancelledError):
        await execute_flow(app, mock_client)

    assert not later_ran
    assert step_seqs(mock_client) == {0}
    mock_client.post_callback.assert_not_awaited()


@pytest.mark.parametrize(
    "make_error",
    [
        lambda: FlowCancelledError("raised by user code"),
        lambda: FlowUnreachableError("raised by user code"),
        lambda: TerminalFlowError("raised by user code"),
        lambda: DeterminismError(
            DeterminismDetails(step_key=StepKey(seq=0), kind=DeterminismKind.TYPE)
        ),
    ],
    ids=["cancelled", "unreachable", "terminal", "determinism"],
)
@pytest.mark.parametrize("is_workflow", [True, False], ids=["workflow", "task"])
@pytest.mark.asyncio
async def test_an_execution_error_raised_by_user_code_is_a_plain_failure(
    app, mock_client, make_error, is_workflow
):
    own = make_error()

    def raises(ctx) -> None:
        raise own

    if is_workflow:
        app.flow(name="wf")(raises)
    else:
        app.task(name="wf")(raises)

    with pytest.raises(RuntimeError) as raised:
        await TaskExecutor(app._registry, mock_client).execute(
            "wf", [], input_response=flow_input(is_workflow=is_workflow)
        )

    assert str(raised.value) == str(own)
    assert raised.value.__cause__ is own
    mock_client.post_callback.assert_awaited_once()
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.determinism is None


@pytest.mark.asyncio
async def test_re_raised_step_failure_reports_an_ordinary_error(app, mock_client):
    @app.flow
    def wf(ctx) -> None:
        try:
            ctx.step("out_of_retries", out_of_retries)
        except StepError as e:
            raise e from None

    with pytest.raises(RuntimeError) as raised:
        await execute_flow(app, mock_client)

    assert raised.value.__cause__.step_name == "out_of_retries"
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR


@pytest.mark.asyncio
async def test_a_ctx_call_inside_a_step_fails_the_run_without_a_retry(app, mock_client):
    @app.flow
    def wf(ctx) -> str:
        try:
            ctx.step("outer", lambda: ctx.step("terminal", terminal))
        except FlowNestedStepError:
            return "caught"
        return "ran"

    with pytest.raises(FlowNestedStepError):
        await execute_flow(app, mock_client)

    mock_client.post_callback.assert_awaited_once()
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR
    # Only a system error has the run retried.
    assert callback.reason is None
    assert "within a step" in callback.error


def test_scheduled_retry_mode_is_not_supported(mock_client):
    with pytest.raises(RenderError, match="isn't supported"):
        DurableFlowContext(mock_client, flow_input(inline_retry_mode="scheduled"))


def test_input_response_parses_the_retry_mode():
    response = InputResponse.from_dict(
        {"task_name": "wf", "input": "", "inline_retry_mode": "local"}
    )
    assert response.inline_retry_mode == "local"


def test_flow_input_needs_a_task_run_id(mock_client):
    with pytest.raises(RenderError, match="task_run_id"):
        DurableFlowContext(mock_client, flow_input(task_run_id=""))


def test_flow_metadata_has_the_flow_run_id(mock_client):
    ctx = DurableFlowContext(mock_client, flow_input(task_run_id="frn-1"))
    assert ctx.metadata == FlowRunMetadata(flow_run_id="frn-1")


def test_retry_without_history_starts_from_the_first_step(ctx, mock_client):
    assert ctx.step("first", lambda: "ran") == "ran"
    assert [
        (r["kind"], r.get("step_key", r.get("key"))["seq"])
        for r in requests(mock_client)
    ] == [("start", 0), ("complete", 0)]


# Replay


def encoded(value):
    return base64.b64encode(json.dumps(value, allow_nan=False).encode()).decode()


def recorded_step(seq, name, args, *, output=None, error=None, done=True, **extra):
    step = {
        "step_key": {"seq": seq},
        "type": "inline",
        "task_name": name,
        "workflow_attempt": 0,
        "input": encoded(args),
        "started_at": "2026-10-13T21:00:00Z",
    }
    if done:
        step["completed_at"] = "2026-10-13T21:00:01Z"
        if error:
            step["error"] = {"name": error[0], "message": error[1]}
        else:
            step["output"] = encoded(output)
    step.update(extra)
    return step


def replay_input(steps, step_attempts=()):
    return InputResponse.from_dict(
        {
            "task_name": "wf",
            "input": "",
            "task_run_id": "trn-1",
            "is_workflow": True,
            "attempt": 1,
            "history": {"steps": steps, "step_attempts": list(step_attempts)},
        }
    )


def replay_ctx(mock_client, steps, step_attempts=()):
    return DurableFlowContext(mock_client, replay_input(steps, step_attempts))


def recorded_attempt(seq, attempt):
    return {
        "step_key": {"seq": seq},
        "attempt": attempt,
        "workflow_attempt": 0,
        "error": {"name": "ConnectionError", "message": "timeout"},
        "ended_at": "2026-10-13T21:00:00Z",
    }


def must_not_run(*args):
    raise AssertionError("a finished step ran again")


def test_finished_step_returns_its_recorded_output(mock_client):
    ctx = replay_ctx(
        mock_client, [recorded_step(0, "charge", ["o-1"], output={"id": 1})]
    )

    def charge(order_id):
        must_not_run()

    assert ctx.step("charge", charge, "o-1") == {"id": 1}
    assert requests(mock_client) == []


def test_failed_step_fails_the_replay_with_the_same_error(mock_client, sleeps):
    def declined(order_id):
        raise ValueError("card declined")

    first_run = DurableFlowContext(mock_client, flow_input())
    with pytest.raises(StepError) as first:
        first_run.step("declined", declined, "o-1")

    with pytest.raises(StepError) as replayed:
        replay_ctx(
            mock_client,
            [
                recorded_step(
                    0, "declined", ["o-1"], error=("ValueError", "card declined")
                )
            ],
        ).step("declined", must_not_run, "o-1")
    assert type(replayed.value) is type(first.value)
    assert str(replayed.value) == str(first.value)


@pytest.mark.parametrize(
    "recorded, failures",
    [
        (recorded_step(0, "charge", ["o-1"], output=1), 0),
        (recorded_step(0, "charge", ["o-1"], done=False), 2),
    ],
    ids=["finished", "open"],
)
def test_unencodable_replay_args_diverge_from_recorded_args(
    mock_client, recorded, failures
):
    ctx = replay_ctx(
        mock_client, [recorded], [recorded_attempt(0, n) for n in range(failures)]
    )

    with pytest.raises(DeterminismError) as raised:
        ctx.step("charge", must_not_run, datetime(2026, 10, 20))

    assert raised.value.details.kind == DeterminismKind.INPUT_HASH
    assert requests(mock_client) == []
    assert ctx.run_failure is raised.value


@pytest.mark.parametrize(
    "error, has_input",
    [
        (("TypeError", "Object of type datetime is not JSON serializable"), False),
        (("DeterminismError", "Flow replay diverged from its history"), True),
    ],
    ids=["encoding-failure", "divergence"],
)
def test_recorded_error_is_raised_at_its_step_without_trusting_its_name(
    mock_client, error, has_input
):
    step = recorded_step(0, "charge", ["o-1"], error=error)
    if not has_input:
        del step["input"]

    with replay_ctx(mock_client, [step]) as context:
        args = ("o-1",) if has_input else (datetime(2026, 10, 20),)
        with pytest.raises(StepError, match=error[1]) as raised:
            context.step("charge", must_not_run, *args)
        assert context.run_failure is None
    assert raised.value.error_name == error[0]
    assert requests(mock_client) == []


@pytest.mark.asyncio
async def test_executor_replays_failed_step_before_reporting_uncaught_error(
    app, mock_client
):
    ran = False

    @app.flow
    def wf(ctx) -> None:
        nonlocal ran
        ran = True
        ctx.step("charge", must_not_run, "o-1")

    response = replay_input(
        [recorded_step(0, "charge", ["o-1"], error=("ValueError", "card declined"))]
    )
    with pytest.raises(
        RuntimeError, match="Step 'charge' failed with ValueError"
    ) as raised:
        await TaskExecutor(app._registry, mock_client).execute(
            "wf", [], input_response=response
        )

    assert ran
    assert requests(mock_client) == []
    mock_client.post_callback.assert_awaited_once()
    callback = mock_client.post_callback.await_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.error == str(raised.value)


@pytest.mark.parametrize(
    "recorded_type, recorded_name, call_name, kind",
    [
        ("inline", "charge", "refund", DeterminismKind.INPUT_HASH),
        ("sleep", "charge", "charge", DeterminismKind.TYPE),
    ],
)
def test_cut_off_encoding_failure_still_checks_name_and_type(
    mock_client, recorded_type, recorded_name, call_name, kind
):
    step = recorded_step(0, recorded_name, [], done=False, type=recorded_type)
    del step["input"]
    ctx = replay_ctx(mock_client, [step])

    with pytest.raises(DeterminismError) as raised:
        ctx.step(
            call_name,
            must_not_run,
            datetime(2026, 10, 20),
        )

    assert raised.value.details.kind == kind
    assert requests(mock_client) == []
    assert ctx.run_failure is raised.value


def test_divergence_fails_without_closing_the_open_step(mock_client):
    ctx = replay_ctx(mock_client, [recorded_step(0, "charge", ["o-1"], done=False)])
    mock_client.step_complete.side_effect = ServerError("write was not acknowledged")

    with pytest.raises(DeterminismError) as raised:
        ctx.step("charge", must_not_run, "o-2")
    assert raised.value.__cause__ is None
    assert ctx.run_failure is raised.value
    mock_client.step_complete.assert_not_called()

    with pytest.raises(DeterminismError) as later:
        ctx.step("refund", must_not_run, "o-3")
    assert later.value is raised.value


@pytest.mark.asyncio
async def test_unencodable_changed_input_is_a_sticky_determinism_failure(
    app, mock_client
):
    ran = False

    def effect(value):
        nonlocal ran
        ran = True

    @app.flow
    def wf(ctx, value):
        with contextlib.suppress(Exception):
            ctx.step("effect", effect, value)
        return "carried on"

    response = replay_input([recorded_step(0, "effect", ["old"], output="done")])

    with pytest.raises(DeterminismError) as raised:
        await TaskExecutor(app._registry, mock_client).execute(
            "wf",
            [datetime(2026, 10, 20)],
            input_response=response,
        )

    assert raised.value.details.kind == DeterminismKind.INPUT_HASH
    assert ran is False
    assert requests(mock_client) == []
    callback = mock_client.post_callback.call_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.determinism is raised.value.details


def test_object_key_order_does_not_change_the_input(mock_client):
    ctx = replay_ctx(
        mock_client, [recorded_step(0, "charge", [{"b": 1, "a": [1, 2]}], output="ok")]
    )

    def charge(order):
        must_not_run()

    assert ctx.step("charge", charge, {"a": (1, 2), "b": 1}) == "ok"


def test_steps_after_the_history_run_normally(mock_client):
    ctx = replay_ctx(mock_client, [recorded_step(0, "first", [], output=1)])

    def first():
        must_not_run()

    def second():
        return 2

    assert ctx.step("first", first) == 1
    assert ctx.step("second", second) == 2
    assert [
        (r["kind"], r.get("step_key", r.get("key"))["seq"])
        for r in requests(mock_client)
    ] == [
        ("start", 1),
        ("complete", 1),
    ]


def test_same_function_at_distinct_seqs_skips_only_the_completed_call(
    mock_client,
):
    ctx = replay_ctx(mock_client, [recorded_step(0, "effect", ["first"], output=1)])
    calls = []

    def effect(label):
        calls.append(label)
        return 2

    assert ctx.step("effect", effect, "first") == 1
    assert ctx.step("effect", effect, "second") == 2

    assert calls == ["second"]
    assert [
        (r["kind"], r.get("step_key", r.get("key"))["seq"])
        for r in requests(mock_client)
    ] == [
        ("start", 1),
        ("complete", 1),
    ]


@pytest.mark.parametrize(
    "recorded, call_name, call_args, kind",
    [
        (
            recorded_step(0, "charge", ["o-1"], output=1),
            "charge",
            ["o-2"],
            DeterminismKind.INPUT_HASH,
        ),
        (
            recorded_step(0, "charge", ["o-1"], output=1),
            "refund",
            ["o-1"],
            DeterminismKind.INPUT_HASH,
        ),
        (
            recorded_step(0, "charge", ["o-1"], type="sleep"),
            "charge",
            ["o-1"],
            DeterminismKind.TYPE,
        ),
        (
            recorded_step(0, "charge", ["o-1"], type="later"),
            "charge",
            ["o-1"],
            DeterminismKind.UNKNOWN_TYPE,
        ),
    ],
)
def test_a_diverging_call_is_a_determinism_error(
    mock_client, recorded, call_name, call_args, kind
):
    ctx = replay_ctx(mock_client, [recorded])

    def step(*args):
        must_not_run()

    with pytest.raises(DeterminismError) as raised:
        ctx.step(call_name, step, *call_args)

    details = raised.value.details
    assert (details.kind, details.step_key) == (kind, StepKey(seq=0))
    assert details.actual == f'inline {call_name}("{call_args[0]}")'
    assert details.expected == f'{StepType(recorded["type"]).value} charge("o-1")'
    assert requests(mock_client) == []


def test_a_determinism_error_cannot_be_caught(mock_client):
    ctx = replay_ctx(mock_client, [recorded_step(0, "charge", ["o-1"], output=1)])

    def charge(order_id):
        return order_id

    with pytest.raises(DeterminismError):
        ctx.step("charge", charge, "o-2")
    with pytest.raises(DeterminismError):
        ctx.step("charge", charge, "o-3")


@pytest.mark.asyncio
async def test_executor_fails_the_run_with_determinism_details(app, mock_client):
    def charge(order_id):
        return order_id

    @app.flow
    def wf(ctx, order_id):
        with contextlib.suppress(DeterminismError):
            ctx.step("charge", charge, order_id)
        return "carried on"

    response = replay_input([recorded_step(0, "charge", ["o-1"], output="o-1")])
    executor = TaskExecutor(app._registry, mock_client)
    with pytest.raises(DeterminismError):
        await executor.execute("wf", ["o-2"], input_response=response)

    callback = mock_client.post_callback.call_args[0][0]
    assert callback.status == Status.ERROR
    assert callback.determinism.kind == DeterminismKind.INPUT_HASH


@pytest.mark.asyncio
async def test_system_error_callback_carries_the_reason(mocker):
    client = UDSClient("unused.sock")
    request = mocker.patch.object(client, "_request", mocker.AsyncMock())

    await client.post_callback(
        CallbackRequest(
            status=Status.ERROR, error="unreachable", reason=TaskErrorReason.SYSTEM
        )
    )

    error = request.call_args.args[2]["error"]
    assert error["reason"] == "system_error"
    assert "determinism" not in error


@pytest.mark.asyncio
async def test_determinism_callback_carries_the_reason(mocker):
    client = UDSClient("unused.sock")
    request = mocker.patch.object(client, "_request", mocker.AsyncMock())
    details = DeterminismDetails(step_key=StepKey(seq=0), kind=DeterminismKind.TYPE)

    await client.post_callback(
        CallbackRequest(status=Status.ERROR, error="diverged", determinism=details)
    )

    error = request.call_args.args[2]["error"]
    assert error["reason"] == "DeterminismError"
    assert error["determinism"] == {
        "step_key": {"seq": 0, "sub_key": ""},
        "kind": "type",
    }


DIVERGENCE = DeterminismDetails(step_key=StepKey(seq=0), kind=DeterminismKind.TYPE)


@pytest.mark.parametrize(
    "error, extra",
    [
        (ExecutionError("boom", type="flow"), {}),
        (FlowBadRequestError("rejected", code="missing_start"), {}),
        (FlowUnreachableError("lost"), {"reason": TaskErrorReason.SYSTEM}),
        (DeterminismError(DIVERGENCE), {"determinism": DIVERGENCE}),
        (
            FlowLimitError(
                "too large", code="workflow_payload_too_large", limit=10, value=11
            ),
            {
                "reason": TaskErrorReason.WORKFLOW_PAYLOAD_TOO_LARGE,
                "limit": 10,
                "value": 11,
            },
        ),
    ],
    ids=["execution", "bad-request", "unreachable", "determinism", "limit"],
)
def test_an_execution_error_builds_its_own_callback(error, extra):
    assert error.to_callback_request() == CallbackRequest(
        status=Status.ERROR, error=str(error), **extra
    )


@pytest.mark.asyncio
async def test_limit_callback_carries_the_reason_and_limit(mocker):
    client = UDSClient("unused.sock")
    request = mocker.patch.object(client, "_request", mocker.AsyncMock())

    await client.post_callback(
        CallbackRequest(
            status=Status.ERROR,
            error="too large",
            reason=TaskErrorReason.WORKFLOW_PAYLOAD_TOO_LARGE,
            limit=1024,
            value=2048,
        )
    )

    error = request.call_args.args[2]["error"]
    assert error == {
        "details": "too large",
        "reason": "workflow_payload_too_large",
        "limit": 1024,
        "value": 2048,
    }


def test_later_steps_fail_with_the_first_determinism_error(mock_client):
    ctx = replay_ctx(mock_client, [recorded_step(0, "charge", ["o-1"], output=1)])

    with pytest.raises(DeterminismError) as first_error:
        ctx.step("charge", must_not_run, "o-2")
    with pytest.raises(DeterminismError) as later_error:
        ctx.step("later", must_not_run)

    assert later_error.value is first_error.value
    assert ctx._next_seq == 1
    assert requests(mock_client) == []


@pytest.mark.parametrize("consumed", [0, 1])
@pytest.mark.asyncio
async def test_returning_before_history_is_consumed_fails(app, mock_client, consumed):
    @app.flow
    def wf(ctx):
        if consumed:
            ctx.step("first", must_not_run)
        return "done"

    response = replay_input(
        [
            recorded_step(0, "first", [], output=1),
            recorded_step(1, "second", [], output=2),
        ]
    )
    executor = TaskExecutor(app._registry, mock_client)
    with pytest.raises(DeterminismError, match="flow completion") as raised:
        await executor.execute("wf", [], input_response=response)

    assert raised.value.details.step_key == StepKey(seq=consumed)
    assert raised.value.step_key is raised.value.details.step_key
    callback = mock_client.post_callback.call_args.args[0]
    assert callback.status == Status.ERROR
    assert callback.determinism is raised.value.details
    assert requests(mock_client) == []


@pytest.mark.asyncio
async def test_consuming_all_history_can_succeed(app, mock_client):
    @app.flow
    def wf(ctx):
        return ctx.step("first", must_not_run)

    response = replay_input([recorded_step(0, "first", [], output=1)])
    assert (
        await TaskExecutor(app._registry, mock_client).execute(
            "wf", [], input_response=response
        )
        == 1
    )
    assert mock_client.post_callback.call_args.args[0].status == Status.SUCCESS


@pytest.mark.parametrize("recorded_input", [None, ""])
def test_missing_recorded_input_cannot_match_a_replay(mock_client, recorded_input):
    step = recorded_step(0, "charge", ["o-1"], output="old result")
    if recorded_input is None:
        del step["input"]
    else:
        step["input"] = recorded_input
    ctx = replay_ctx(mock_client, [step])

    with pytest.raises(DeterminismError, match="missing recorded input") as raised:
        ctx.step("charge", must_not_run, "o-2")
    assert raised.value.details.kind == DeterminismKind.INPUT_HASH
    with pytest.raises(DeterminismError):
        ctx.step("later", must_not_run)
    assert requests(mock_client) == []


@pytest.mark.parametrize(
    "recorded, resumed",
    [([], 1), ([0, 1], 2), ([1], 2)],
    ids=["cut-off-first-attempt", "after-failures", "after-a-gap"],
)
def test_open_step_resumes_after_its_recorded_attempts(
    mock_client, sleeps, recorded, resumed
):
    failures = [recorded_attempt(0, n) for n in recorded]
    ctx = replay_ctx(mock_client, [recorded_step(0, "flaky", [], done=False)], failures)
    calls = 0

    def flaky():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise ConnectionError("timeout")
        return "ok"

    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)

    assert (
        ctx.step("flaky", flaky, retry=Retry(max_retries=3, wait_duration_ms=10))
        == "ok"
    )
    assert [(r["kind"], r.get("attempt")) for r in requests(mock_client)] == [
        ("attempt", resumed),
        ("complete", None),
    ]


def test_start_step_yields_the_attempt_a_replay_resumes_at(mock_client):
    step = recorded_step(0, "flaky", [], done=False)
    ctx = replay_ctx(mock_client, [step], [recorded_attempt(0, 0)])

    with ctx.start_step("flaky", None) as (step_ctx, recorded):
        assert step_ctx.attempt == 1
        assert recorded.step_key == step_ctx.step_key


def test_each_replay_counts_on_from_the_attempts_before_it(mock_client, sleeps):
    def flaky():
        raise ConnectionError("timeout")

    retry = Retry(max_retries=3, wait_duration_ms=10)
    step = recorded_step(0, "flaky", [], done=False)
    failures = [recorded_attempt(0, 0)]
    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)
    # The worker dies while backing off, so each execution records one failure.
    sleeps.side_effect = SystemExit

    for expected in (1, 2):
        mock_client.reset_mock()
        ctx = replay_ctx(mock_client, [step], failures)
        with pytest.raises(SystemExit):
            ctx.step("flaky", flaky, retry=retry)

        (attempt,) = requests(mock_client)
        assert (attempt["kind"], attempt["attempt"]) == ("attempt", expected)
        failures.append(recorded_attempt(0, attempt["attempt"]))

    # The 4th attempt uses up the step's 3 retries.
    mock_client.reset_mock()
    ctx = replay_ctx(mock_client, [step], failures)
    with pytest.raises(StepError):
        ctx.step("flaky", flaky, retry=retry)

    (complete,) = requests(mock_client)
    assert complete["outcome"]["final_attempt"]["attempt"] == 3


def test_open_step_past_its_retries_records_a_catchable_failure(mock_client, sleeps):
    ctx = replay_ctx(
        mock_client,
        [recorded_step(0, "flaky", [], done=False)],
        [recorded_attempt(0, 0)],
    )

    with pytest.raises(StepError, match="timeout"):
        ctx.step("flaky", must_not_run)
    assert ctx.run_failure is None
    (complete,) = requests(mock_client)
    assert complete["outcome"]["final_attempt"]["attempt"] == 0
    assert final_error(complete)["name"] == "ConnectionError"
    (step,) = ctx._journal._history.steps
    assert step.completed_at is not None
    sleeps.assert_not_called()
    assert ctx.step("fallback", lambda: "recovered") == "recovered"


def test_interrupted_step_without_a_recorded_error_is_terminal(mock_client, sleeps):
    ctx = replay_ctx(mock_client, [recorded_step(0, "flaky", [], done=False)])

    with pytest.raises(TerminalFlowError, match="past its 0 retries") as raised:
        ctx.step("flaky", must_not_run)
    assert ctx.run_failure is raised.value
    assert requests(mock_client) == []
    sleeps.assert_not_called()
    with pytest.raises(TerminalFlowError) as later:
        ctx.step("fallback", must_not_run)
    assert later.value is raised.value


def test_open_step_past_its_retries_stops_on_an_unacknowledged_failure(
    mock_client,
):
    ctx = replay_ctx(
        mock_client,
        [recorded_step(0, "flaky", [], done=False)],
        [recorded_attempt(0, 0)],
    )
    mock_client.step_complete.side_effect = ServerError("write was not acknowledged")

    with pytest.raises(
        FlowUnreachableError, match="write was not acknowledged"
    ) as raised:
        ctx.step("flaky", must_not_run)
    assert isinstance(raised.value.__cause__, ServerError)
    assert ctx.run_failure is raised.value
    mock_client.step_complete.assert_called_once()

    with pytest.raises(FlowUnreachableError) as later:
        ctx.step("later", must_not_run)
    assert later.value is raised.value


def test_a_cancelled_close_out_overrides_the_run_failure(mock_client):
    ctx = replay_ctx(
        mock_client,
        [recorded_step(0, "flaky", [], done=False)],
        [recorded_attempt(0, 0)],
    )
    mock_client.step_complete.side_effect = ClientError(
        "record step failed with status 409",
        status_code=409,
        json_body={"code": "run_cancelled"},
    )

    with pytest.raises(FlowCancelledError) as raised:
        ctx.step("flaky", must_not_run)
    assert ctx.run_failure is raised.value

    with pytest.raises(FlowCancelledError) as later:
        ctx.step("later", must_not_run)
    assert later.value is raised.value


def test_new_step_with_a_negative_retry_policy_runs(ctx):
    retry = Retry(max_retries=-1, wait_duration_ms=10)
    assert ctx.step("charge", lambda: "ok", retry=retry) == "ok"


def test_history_tracks_the_attempts_own_writes(ctx, mock_client, sleeps):
    mock_client.step_attempt.return_value = StepAttemptResponse(applied=True)
    seen = []

    def flaky():
        seen.append([a.attempt for a in ctx._journal._history.attempts(StepKey(seq=0))])
        if len(seen) < 3:
            raise ConnectionError("timeout")
        return "ok"

    assert (
        ctx.step("flaky", flaky, retry=Retry(max_retries=3, wait_duration_ms=10))
        == "ok"
    )

    assert seen == [[], [0], [0, 1]]
    (step,) = ctx._journal._history.steps
    assert (step.task_name, step.input_, step.output, step.error) == (
        "flaky",
        "[]",
        '"ok"',
        None,
    )
    assert step.completed_at is not None
    assert ctx._journal._history.attempts(StepKey(seq=0)) == []
    ctx._journal._history.validate()


def test_history_tracks_a_failed_step(ctx, mock_client):
    def declined():
        raise ValueError("card declined")

    with pytest.raises(StepError):
        ctx.step("declined", declined)

    (step,) = ctx._journal._history.steps
    assert step.error is not None
    assert (step.error.name, step.error.message) == ("ValueError", "card declined")
    assert step.completed_at is not None


def test_history_records_a_write_before_it_is_sent(ctx, mock_client):
    recorded = []
    mock_client.step_start.side_effect = lambda request: recorded.append(
        list(ctx._journal._history.steps)
    )

    ctx.step("charge", lambda: "ok")

    ((started,),) = recorded
    assert (started.step_key, started.task_name, started.completed_at) == (
        StepKey(seq=0),
        "charge",
        None,
    )


@pytest.mark.parametrize("fails", [False, True], ids=["succeeds", "fails"])
def test_resumed_step_never_completes_before_its_recorded_start(mock_client, fails):
    # The step started on a worker whose clock is ahead of this one.
    started_at = "2999-01-01T00:00:00Z"
    ctx = replay_ctx(
        mock_client,
        [recorded_step(0, "charge", [], done=False, started_at=started_at)],
    )

    def charge():
        if fails:
            raise ValueError("card declined")
        return "ok"

    retry = Retry(max_retries=1, wait_duration_ms=10)
    with contextlib.suppress(StepError):
        ctx.step("charge", charge, retry=retry)

    (complete,) = requests(mock_client)
    completed_at = parse_time(complete["outcome"]["completed_at"])
    assert completed_at == parse_time(started_at)
    if fails:
        ended_at = complete["outcome"]["final_attempt"]["ended_at"]
        assert parse_time(ended_at) == completed_at
    assert ctx._journal._history.steps[0].completed_at == completed_at


def test_exhausted_replay_completes_the_actual_last_attempt(mock_client):
    final = recorded_attempt(0, 2)
    final["started_at"] = "2026-10-13T21:00:00.200Z"
    final["ended_at"] = "2026-10-13T21:00:00.400Z"
    final["workflow_attempt"] = 7
    context = replay_ctx(
        mock_client, [recorded_step(0, "flaky", [], done=False)], [final]
    )
    with pytest.raises(StepError, match="timeout"):
        context.step(
            "flaky", must_not_run, retry=Retry(max_retries=2, wait_duration_ms=0)
        )
    (complete,) = requests(mock_client)
    sent = complete["outcome"]["final_attempt"]
    assert sent["attempt"] == 2
    assert sent["data"]["workflow_attempt"] == 7
    assert parse_time(sent["started_at"]) == parse_time(final["started_at"])
    assert parse_time(sent["ended_at"]) == parse_time(final["ended_at"])
    assert parse_time(complete["outcome"]["completed_at"]) == parse_time(
        final["ended_at"]
    )
    assert final_error(complete) == final["error"]
