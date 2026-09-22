"""Tests for the task execution context."""

from dataclasses import FrozenInstanceError

import pytest

from render.workflows._callback_models import InputResponse
from render.workflows.client import UDSClient
from render.workflows.context import TaskContext, TaskRunMetadata, WorkflowTaskContext
from render.workflows.task import TaskRegistry, create_task_decorator


@pytest.fixture
def task_decorator():
    """Create a task decorator bound to a fresh registry."""
    return create_task_decorator(TaskRegistry())


@pytest.fixture
def mock_client(mocker):
    """Create a mock UDS client that records subtask submissions."""
    mock = mocker.create_autospec(UDSClient, spec_set=True)
    mock.run_subtask = mocker.AsyncMock(return_value="subtask result")
    return mock


@pytest.fixture
def ctx(mock_client):
    return WorkflowTaskContext(mock_client)


@pytest.mark.asyncio
async def test_a_stand_in_can_satisfy_the_protocol(task_decorator):
    """
    TaskContext is a Protocol, so a test double needs no subclassing.
    """

    class RecordingContext:
        metadata = TaskRunMetadata()

        def __init__(self):
            self.runs = []

        async def run(self, task, *args, **kwargs):
            self.runs.append((task.name, args, kwargs))
            return "stubbed"

    @task_decorator
    async def caller(ctx, a: int) -> str:
        return await ctx.run(callee, a)

    @task_decorator
    def callee(ctx, a: int) -> int:
        return a

    recording: TaskContext = RecordingContext()
    assert await caller.func(recording, 5) == "stubbed"
    assert recording.runs == [("callee", (5,), {})]


def test_metadata_is_a_read_only_snapshot(mock_client):
    input_response = InputResponse(
        task_name="example",
        input_="W10=",
        task_run_id="trn-child",
        root_task_run_id="trn-root",
        parent_task_run_id="trn-parent",
    )
    ctx = WorkflowTaskContext(mock_client, input_response)
    metadata = ctx.metadata
    input_response.task_run_id = "trn-other"
    input_response.root_task_run_id = "trn-other"
    input_response.parent_task_run_id = "trn-other"

    assert ctx.metadata is metadata
    assert metadata == TaskRunMetadata("trn-child", "trn-root", "trn-parent")
    with pytest.raises(AttributeError):
        ctx.metadata = TaskRunMetadata()
    for field in ("task_run_id", "root_task_run_id", "parent_task_run_id"):
        with pytest.raises(FrozenInstanceError):
            setattr(metadata, field, "trn-overwrite")


class TestRun:
    """ctx.run submits the task to run on its own compute."""

    @pytest.mark.asyncio
    async def test_submits_by_name_with_positional_input(
        self, ctx, mock_client, task_decorator
    ):
        @task_decorator
        def square(ctx, a: int) -> int:
            return a * a

        result = await ctx.run(square, 5)

        assert result == "subtask result"
        mock_client.run_subtask.assert_awaited_once_with("square", [5])

    @pytest.mark.asyncio
    async def test_submits_named_parameters_as_a_dict(
        self, ctx, mock_client, task_decorator
    ):
        @task_decorator
        def add(ctx, a: int, b: int) -> int:
            return a + b

        await ctx.run(add, a=1, b=2)

        mock_client.run_subtask.assert_awaited_once_with("add", {"a": 1, "b": 2})

    @pytest.mark.asyncio
    async def test_submits_empty_input_for_a_task_with_no_arguments(
        self, ctx, mock_client, task_decorator
    ):
        @task_decorator
        def ping(ctx) -> str:
            return "pong"

        await ctx.run(ping)

        mock_client.run_subtask.assert_awaited_once_with("ping", [])

    @pytest.mark.asyncio
    async def test_rejects_mixed_positional_and_named_input(self, ctx, task_decorator):
        @task_decorator
        def add(ctx, a: int, b: int) -> int:
            return a + b

        with pytest.raises(ValueError, match="Cannot mix positional and keyword"):
            await ctx.run(add, 1, b=2)

    @pytest.mark.asyncio
    async def test_propagates_subtask_failures(
        self, ctx, mock_client, task_decorator, mocker
    ):
        @task_decorator
        def failing(ctx) -> None:
            return None

        mock_client.run_subtask = mocker.AsyncMock(
            side_effect=RuntimeError("subtask failed")
        )

        with pytest.raises(RuntimeError, match="subtask failed"):
            await ctx.run(failing)
