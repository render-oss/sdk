#!/usr/bin/env python3
"""Tests for the task executor functionality."""

import pytest

from render_sdk.workflows.client import Status, UDSClient
from render_sdk.workflows.executor import TaskExecutor
from render_sdk.workflows.task import TaskRegistry, create_task_decorator


# Fixtures
@pytest.fixture
def task_registry():
    """Create a fresh task registry for each test."""
    return TaskRegistry()


@pytest.fixture
def task_decorator(task_registry):
    """Create a task decorator bound to the test registry."""
    return create_task_decorator(task_registry)


@pytest.fixture
def mock_client(mocker):
    """Create a mock UDS client."""
    mock = mocker.create_autospec(UDSClient, spec_set=True)
    mock.post_callback = mocker.AsyncMock()
    return mock


@pytest.fixture
def task_executor(task_registry, mock_client):
    """Create a task executor with mocked client."""
    return TaskExecutor(task_registry, mock_client)


# Basic Task Execution Tests
@pytest.mark.asyncio
async def test_simple_task_execution(task_decorator, task_executor, mock_client):
    """Test executing a simple task without subtasks."""

    @task_decorator
    def add_numbers(a: int, b: int) -> int:
        return a + b

    result = await task_executor.execute("add_numbers", [5, 3])

    assert result == 8
    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]
    assert call_args.status == Status.SUCCESS
    assert call_args.result == 8


@pytest.mark.asyncio
async def test_task_with_string_result(task_decorator, task_executor, mock_client):
    """Test task that returns a string."""

    @task_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    result = await task_executor.execute("greet", ["World"])

    assert result == "Hello, World!"
    mock_client.post_callback.assert_called_once()


@pytest.mark.asyncio
async def test_task_execution_error(task_decorator, task_executor, mock_client):
    """Test task execution that raises an error."""

    @task_decorator
    def failing_task(x: int) -> int:
        if x < 0:
            raise ValueError("Negative numbers not allowed")
        return x * 2

    with pytest.raises(ValueError):
        await task_executor.execute("failing_task", [-5])

    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]
    assert call_args.status == Status.ERROR
    assert "Negative numbers not allowed" in call_args.error


@pytest.mark.asyncio
async def test_nonexistent_task(task_executor, mock_client):
    """Test executing a task that doesn't exist."""
    with pytest.raises(ValueError):
        await task_executor.execute("nonexistent_task", [])

    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]
    assert call_args.status == Status.ERROR


# Integration Tests
@pytest.mark.asyncio
async def test_complex_task_chain(task_registry, task_decorator, mock_client, mocker):
    """Test a complex chain of task executions."""

    @task_decorator
    def increment(x: int) -> int:
        return x + 1

    @task_decorator
    def double(x: int) -> int:
        return x * 2

    @task_decorator
    async def complex_calculation(start: int) -> int:
        # Use await for subtask calls
        step1 = await increment(start)
        step2 = await double(step1)
        step3 = await increment(step2)
        return step3

    # Configure mock to simulate subtask execution
    def mock_run_subtask(task_name, args):
        if task_name == "increment":
            return args[0] + 1
        elif task_name == "double":
            return args[0] * 2
        else:
            raise ValueError(f"Unknown task: {task_name}")

    mock_client.run_subtask = mocker.AsyncMock(side_effect=mock_run_subtask)

    executor = TaskExecutor(task_registry, mock_client)
    result = await executor.execute("complex_calculation", [5])

    # Should compute: ((5 + 1) * 2) + 1 = (6 * 2) + 1 = 12 + 1 = 13
    assert result == 13


@pytest.mark.asyncio
async def test_callback_format(task_registry, task_decorator, mock_client):
    """Test that callbacks are formatted correctly."""

    @task_decorator
    def simple_task(value: str) -> str:
        return f"processed: {value}"

    executor = TaskExecutor(task_registry, mock_client)
    await executor.execute("simple_task", ["test"])

    # Check that callback was called with correct format
    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]
    assert call_args.status == Status.SUCCESS
    assert call_args.result == "processed: test"
