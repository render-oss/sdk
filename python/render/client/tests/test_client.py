#!/usr/bin/env python3
"""Unit tests for the Render REST API client functionality."""

import copy

import pytest

from render.client import (
    Client,
    ListTaskRunsParams,
    WorkflowsService,
)
from render.client.render_public_api_client.models.error import Error
from render.client.render_public_api_client.models.task_run import TaskRun
from render.client.render_public_api_client.models.task_run_details import (
    TaskRunDetails,
)
from render.client.render_public_api_client.models.task_run_status import TaskRunStatus
from render.client.workflows import AwaitableTaskRun


# Fixtures
@pytest.fixture
def mock_task_run(mocker):
    """Create a mock TaskRun object."""
    task_run = mocker.Mock(spec=TaskRun)
    task_run.id = "trn-test123"
    task_run.status = mocker.Mock(spec=TaskRunStatus)
    task_run.status.value = TaskRunStatus.RUNNING
    task_run.completed_at = None
    return task_run


@pytest.fixture
def mock_task_run_details(mocker):
    """Create a mock TaskRunDetails object."""
    details = mocker.Mock(spec=TaskRunDetails)
    details.id = "trn-test123"
    details.status = mocker.Mock(spec=TaskRunStatus)
    details.status.value = TaskRunStatus.COMPLETED
    details.output = {"result": 42}
    details.error = None
    details.completed_at = "2024-01-01T00:00:00Z"
    return details


@pytest.fixture
def mock_authenticated_client(mocker):
    """Create a mock authenticated client."""
    client = mocker.Mock()
    client._base_url = "https://api.test.com/v1"
    return client


@pytest.fixture
def client(mocker, mock_authenticated_client):
    """Create a Client instance with mocked dependencies."""
    mocker.patch(
        "render.client.client.AuthenticatedClient",
        return_value=mock_authenticated_client,
    )
    return Client("test-token", base_url="https://api.test.com")


@pytest.fixture
def workflows_service(client):
    """Create a WorkflowsService instance."""
    return client.workflows


@pytest.mark.asyncio
async def test_run_task_success(mocker, workflows_service, mock_task_run):
    """Test successful task execution."""
    mock_create = mocker.patch("render.client.render_public_api_client.api.workflows.create_task.asyncio")
    mock_create.return_value = mock_task_run

    result = await workflows_service.run_task("test-task", {"input": "data"})

    assert isinstance(result, AwaitableTaskRun)
    assert result.id == "trn-test123"
    mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_run_task_failure(mocker, workflows_service):
    """Test task execution failure."""

    error = Error(message="Task creation failed")
    mock_create = mocker.patch("render.client.render_public_api_client.api.workflows.create_task.asyncio")
    mock_create.return_value = error

    with pytest.raises(Exception, match="Failed to create task: Task creation failed"):
        await workflows_service.run_task("test-task", {"input": "data"})


@pytest.mark.asyncio
async def test_get_task_run_success(mocker, workflows_service, mock_task_run_details):
    """Test successful task run retrieval."""
    mock_get = mocker.patch("render.client.render_public_api_client.api.workflows.get_task_run.asyncio")
    mock_get.return_value = mock_task_run_details

    result = await workflows_service.get_task_run("trn-test123")

    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    mock_get.assert_called_once_with(client=workflows_service.client.internal, task_run_id="trn-test123")


@pytest.mark.asyncio
async def test_get_task_run_failure(mocker, workflows_service):
    """Test task run retrieval failure."""
    error = Error(message="Task not found")
    mock_get = mocker.patch("render.client.render_public_api_client.api.workflows.get_task_run.asyncio")
    mock_get.return_value = error

    with pytest.raises(Exception, match="Failed to get task run trn-test123: Task not found"):
        await workflows_service.get_task_run("trn-test123")


@pytest.mark.asyncio
async def test_cancel_task_run_success(mocker, workflows_service):
    """Test successful task run cancellation."""
    mock_delete = mocker.patch("render.client.render_public_api_client.api.workflows.delete_task_run.asyncio")
    mock_delete.return_value = None  # Success returns None

    await workflows_service.cancel_task_run("trn-test123")

    mock_delete.assert_called_once_with(client=workflows_service.client.internal, task_run_id="trn-test123")


@pytest.mark.asyncio
async def test_cancel_task_run_failure(mocker, workflows_service):
    """Test task run cancellation failure."""
    error = Error(message="Cannot cancel task")
    mock_delete = mocker.patch("render.client.render_public_api_client.api.workflows.delete_task_run.asyncio")
    mock_delete.return_value = error

    with pytest.raises(Exception, match="Failed to cancel task run trn-test123: Cannot cancel task"):
        await workflows_service.cancel_task_run("trn-test123")


@pytest.mark.asyncio
async def test_list_task_runs_success(mocker, workflows_service, mock_task_run):
    """Test successful task runs listing."""
    task_runs = [mock_task_run]
    mock_list = mocker.patch("render.client.render_public_api_client.api.workflows.list_task_runs.asyncio")
    mock_list.return_value = task_runs

    params = ListTaskRunsParams(limit=5, owner_id="test-owner")
    result = await workflows_service.list_task_runs(params)

    assert len(result) == 1
    assert result[0].id == "trn-test123"
    mock_list.assert_called_once_with(
        client=workflows_service.client.internal,
        limit=5,
        cursor=None,
        owner_id="test-owner",
    )


@pytest.fixture
def mock_workflows_service(mocker, client):
    """Create a mock workflows service."""
    return mocker.Mock(spec=WorkflowsService, client=client)


@pytest.fixture
def awaitable_task_run(mock_task_run, mock_workflows_service):
    """Create an AwaitableTaskRun instance."""
    return AwaitableTaskRun(mock_task_run, mock_workflows_service)


def test_task_run_properties(awaitable_task_run):
    """Test AwaitableTaskRun properties."""
    assert awaitable_task_run.id == "trn-test123"
    assert awaitable_task_run.status == TaskRunStatus.RUNNING


def test_is_terminal_status(mock_task_run, mock_workflows_service):
    """Test terminal status detection."""
    # Test running status (not terminal)
    mock_task_run.status.value = TaskRunStatus.RUNNING
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)
    assert not awaitable_task_run.is_terminal_status()

    # Test completed status (terminal)
    mock_task_run.status.value = TaskRunStatus.COMPLETED
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)
    assert awaitable_task_run.is_terminal_status()

    # Test failed status (terminal)
    mock_task_run.status.value = TaskRunStatus.FAILED
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)
    assert awaitable_task_run.is_terminal_status()


@pytest.mark.asyncio
async def test_await_already_completed_task(mocker, mock_task_run, mock_workflows_service, mock_task_run_details):
    """Test awaiting an already completed task."""
    # Set task as completed
    mock_task_run.status.value = TaskRunStatus.COMPLETED
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)

    # Mock the get_task_run call
    mock_workflows_service.get_task_run = mocker.AsyncMock(return_value=mock_task_run_details)

    result = await awaitable_task_run
    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    mock_workflows_service.get_task_run.assert_called_once_with("trn-test123")


@pytest.mark.asyncio
async def test_await_with_sse_failure_fallback_to_polling(mocker, awaitable_task_run, mock_task_run_details):
    """Test fallback to polling when SSE fails."""
    # Mock SSE to fail
    awaitable_task_run.workflows_service.client.sse.stream_task_run_events = mocker.AsyncMock(
        side_effect=Exception("SSE connection failed")
    )

    # Mock polling to succeed
    mock_get_task_run = mocker.AsyncMock()
    awaitable_task_run.workflows_service.get_task_run = mock_get_task_run

    # First call returns running, second returns completed
    running_details = copy.deepcopy(mock_task_run_details)
    running_details.status.value = TaskRunStatus.RUNNING
    completed_details = copy.deepcopy(mock_task_run_details)
    completed_details.status.value = TaskRunStatus.COMPLETED

    mock_get_task_run.side_effect = [
        running_details,  # Still running
        completed_details,  # Now completed
    ]

    # Mock sleep to avoid actual delays
    mocker.patch("asyncio.sleep")
    result = await awaitable_task_run

    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    assert mock_get_task_run.call_count == 2
