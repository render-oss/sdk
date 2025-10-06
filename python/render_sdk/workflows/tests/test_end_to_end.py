#!/usr/bin/env python3
"""End-to-end tests that simulate the full workflow."""

import pytest

from render_sdk.workflows.callback_api.models.task_options import TaskOptions
from render_sdk.workflows.client import Status, UDSClient
from render_sdk.workflows.executor import TaskExecutor
from render_sdk.workflows.runner import register
from render_sdk.workflows.task import (
    Options,
    Retry,
    TaskRegistry,
    create_task_decorator,
)


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


# End-to-end tests
def test_task_registration_network_payload(task_registry, task_decorator, mocker):
    """
    Test that task registration actually sends the
    correct payload over the network.
    """

    # Mock the UDSClient class
    mock_uds_client_class = mocker.patch("render_sdk.workflows.runner.UDSClient")

    # Set up the mock instance
    mock_client_instance = mocker.Mock()
    mock_uds_client_class.return_value = mock_client_instance
    mock_client_instance.register_tasks = mocker.AsyncMock(
        return_value={"status": "success"},
    )
    mock_client_instance.disconnect = mocker.AsyncMock()

    # Define tasks with various configurations
    @task_decorator
    def simple_task(x: int) -> int:
        return x * 2

    @task_decorator(name="custom_name")
    def renamed_task(msg: str) -> str:
        return f"Hello {msg}"

    @task_decorator(
        options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000, factor=1.5)),
    )
    def retry_task(data: str) -> str:
        return data.upper()

    # Mock get_task_registry to return our test registry
    mock_get_registry = mocker.patch("render_sdk.workflows.runner.get_task_registry")
    mock_get_registry.return_value = task_registry

    register("/tmp/test.sock")  # noqa:S108

    # Verify that UDSClient was instantiated with correct socket path
    mock_uds_client_class.assert_called_once_with("/tmp/test.sock")  # noqa:S108

    # Verify that register_tasks was called exactly once
    mock_client_instance.register_tasks.assert_called_once()

    # Get the actual payload that was sent
    sent_tasks = mock_client_instance.register_tasks.call_args[0][0]

    # Verify we have the expected number of tasks
    assert len(sent_tasks.tasks) == 3

    # Find tasks by name to verify their structure
    task_by_name = {task.name: task for task in sent_tasks.tasks}

    # Verify simple task
    assert "simple_task" in task_by_name
    simple_task_payload = task_by_name["simple_task"]
    assert simple_task_payload.name == "simple_task"
    assert isinstance(simple_task_payload.options, TaskOptions)

    # Verify renamed task
    assert "custom_name" in task_by_name
    renamed_task_payload = task_by_name["custom_name"]
    assert renamed_task_payload.name == "custom_name"
    assert isinstance(renamed_task_payload.options, TaskOptions)

    # Verify retry task with options
    assert "retry_task" in task_by_name
    retry_task_payload = task_by_name["retry_task"]
    assert retry_task_payload.name == "retry_task"

    # Verify retry options structure
    retry_options = retry_task_payload.options.retry
    assert retry_options.max_retries == 3
    assert retry_options.wait_duration_ms == 1000
    assert retry_options.factor == 1.5


@pytest.mark.asyncio
async def test_callback_payloads_with_mocked_client(
    task_registry,
    task_decorator,
    mock_client,
):
    """Test that callback payloads are correctly formatted and sent."""

    @task_decorator
    def test_task(value: int) -> int:
        return value * 10

    @task_decorator
    def failing_task(should_fail: bool) -> str:
        if should_fail:
            raise ValueError("Test failure")
        return "success"

    # Test success callback
    executor = TaskExecutor(task_registry, mock_client)

    result = await executor.execute("test_task", [5])
    assert result == 50

    # Verify success callback was sent with correct payload
    mock_client.post_callback.assert_called_once()
    success_payload = mock_client.post_callback.call_args[0][0]
    assert success_payload.status == Status.SUCCESS
    assert success_payload.result == 50

    # Reset mock and test error callback
    mock_client.reset_mock()

    with pytest.raises(ValueError):
        await executor.execute("failing_task", [True])

    # Verify error callback was sent with correct payload
    mock_client.post_callback.assert_called_once()
    error_payload = mock_client.post_callback.call_args[0][0]
    assert error_payload.status == Status.ERROR
    assert "Test failure" in error_payload.error
