#!/usr/bin/env python3
"""Tests for the task executor functionality."""

import pytest

from render.workflows import TaskRegistry, create_task_decorator
from render.workflows.client import UDSClient
from render.workflows.executor import TaskExecutor


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
    assert call_args.type == "complete"


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
    assert call_args.type == "error"
    assert "Negative numbers not allowed" in call_args.error


@pytest.mark.asyncio
async def test_nonexistent_task(task_executor, mock_client):
    """Test executing a task that doesn't exist."""
    with pytest.raises(ValueError):
        await task_executor.execute("nonexistent_task", [])

    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]
    assert call_args.type == "error"


# Task Context Tests (Subtask execution)
def test_subtask_execution(task_registry, task_decorator):
    """Test executing subtasks within a task using direct calls."""

    @task_decorator
    def square(x: int) -> int:
        return x * x

    @task_decorator
    def add_squares(a: int, b: int) -> int:
        # Direct function calls for now, will become socket calls later
        result1 = square(a)
        result2 = square(b)
        return result1 + result2

    result = task_registry.execute_task("add_squares", 3, 4)

    # Should compute 3^2 + 4^2 = 9 + 16 = 25
    assert result.result == 25


def test_subtask_error_propagation(task_registry, task_decorator):
    """Test that errors in subtasks are properly propagated."""

    @task_decorator
    def divide(a: int, b: int) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b

    @task_decorator
    def compute_ratio(x: int, y: int) -> float:
        # Direct function call for now, will become socket call later
        result = divide(x, y)
        return result * 2

    result = task_registry.execute_task("compute_ratio", 10, 0)

    assert result.error is not None
    assert isinstance(result.error, ZeroDivisionError)


def test_task_execution_by_name(task_registry, task_decorator):
    """Test executing tasks by name through registry."""

    @task_decorator
    def multiply(a: int, b: int) -> int:
        return a * b

    result = task_registry.execute_task("multiply", 6, 7)

    assert result.result == 42
    assert result.error is None


# Integration Tests
@pytest.mark.asyncio
async def test_complex_task_chain(task_registry, task_decorator, mock_client):
    """Test a complex chain of task executions."""

    @task_decorator
    def increment(x: int) -> int:
        return x + 1

    @task_decorator
    def double(x: int) -> int:
        return x * 2

    @task_decorator
    def complex_calculation(start: int) -> int:
        # Direct function calls (will become socket calls in future)
        step1 = increment(start)
        step2 = double(step1)
        step3 = increment(step2)
        return step3

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
    result = await executor.execute("simple_task", ["test"])

    # Check that callback was called with correct format
    mock_client.post_callback.assert_called_once()
    call_args = mock_client.post_callback.call_args[0][0]

    # Verify the result
    assert result == "processed: test"
