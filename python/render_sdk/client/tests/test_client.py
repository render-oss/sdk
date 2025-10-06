#!/usr/bin/env python3
"""Unit tests for the Render REST API client functionality."""

import datetime

import pytest

from render_sdk.client import Client, ListTaskRunsParams, WorkflowsService
from render_sdk.client.errors import ClientError
from render_sdk.client.workflows import AwaitableTaskRun
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.models.task_run import TaskRun
from render_sdk.public_api.models.task_run_details import TaskRunDetails
from render_sdk.public_api.models.task_run_status import TaskRunStatus
from render_sdk.public_api.types import Response


# Fixtures
@pytest.fixture
def mock_task_run(mocker):
    return TaskRun(
        id="trn-test123",
        status=TaskRunStatus.RUNNING,
        completed_at=None,
        parent_task_run_id=None,
        root_task_run_id=None,
        retries=0,
        started_at=None,
        task_id=None,
    )


@pytest.fixture
def mock_task_run_details(mocker):
    return TaskRunDetails(
        id="trn-test123",
        status=TaskRunStatus.COMPLETED,
        error=None,
        completed_at=datetime.datetime.now(),
        results=[42],
        input_=[42],
        parent_task_run_id=None,
        root_task_run_id=None,
        retries=0,
        started_at=None,
        task_id=None,
    )


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
        "render_sdk.client.client.AuthenticatedClient",
        return_value=mock_authenticated_client,
    )
    return Client("test-token", base_url="https://api.test.com")


@pytest.fixture
def workflows_service(client):
    """Create a WorkflowsService instance."""
    return client.workflows


@pytest.fixture
def mock_cancel_task_run_asyncio(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflows.cancel_task_run.asyncio_detailed"
    )


@pytest.fixture
def mock_list_task_runs_asyncio(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflows.list_task_runs.asyncio_detailed"
    )


@pytest.fixture
def mock_create_task_asyncio(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflows.create_task.asyncio_detailed"
    )


@pytest.fixture
def mock_get_task_run_asyncio(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflows.get_task_run.asyncio_detailed"
    )


@pytest.mark.asyncio
async def test_run_task_success(
    mock_create_task_asyncio, workflows_service, mock_task_run
):
    """Test successful task execution."""
    mock_create_task_asyncio.return_value = Response(
        status_code=202, content=b"", headers={}, parsed=mock_task_run
    )

    result = await workflows_service.run_task("test-task", {"input": "data"})

    assert isinstance(result, AwaitableTaskRun)
    assert result.id == "trn-test123"
    mock_create_task_asyncio.assert_called_once()


@pytest.mark.asyncio
async def test_run_task_failure(mock_create_task_asyncio, workflows_service):
    """Test task execution failure."""

    error = Error(message="Task creation failed")
    mock_create_task_asyncio.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="create task failed: Task creation failed"):
        await workflows_service.run_task("test-task", {"input": "data"})


@pytest.mark.asyncio
async def test_get_task_run_success(
    mock_get_task_run_asyncio, workflows_service, mock_task_run_details
):
    """Test successful task run retrieval."""
    mock_get_task_run_asyncio.return_value = Response(
        status_code=200, content=b"", headers={}, parsed=mock_task_run_details
    )

    result = await workflows_service.get_task_run("trn-test123")

    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    mock_get_task_run_asyncio.assert_called_once_with(
        client=workflows_service.client.internal, task_run_id="trn-test123"
    )


@pytest.mark.asyncio
async def test_get_task_run_failure(mock_get_task_run_asyncio, workflows_service):
    """Test task run retrieval failure."""
    error = Error(message="Task not found")
    mock_get_task_run_asyncio.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="get task run failed: Task not found"):
        await workflows_service.get_task_run("trn-test123")


@pytest.mark.asyncio
async def test_cancel_task_run_success(mock_cancel_task_run_asyncio, workflows_service):
    """Test successful task run cancellation."""
    mock_cancel_task_run_asyncio.return_value = Response(
        status_code=204, content=b"", headers={}, parsed=None
    )

    await workflows_service.cancel_task_run("trn-test123")

    mock_cancel_task_run_asyncio.assert_called_once_with(
        client=workflows_service.client.internal, task_run_id="trn-test123"
    )


@pytest.mark.asyncio
async def test_cancel_task_run_failure(mock_cancel_task_run_asyncio, workflows_service):
    """Test task run cancellation failure."""
    error = Error(message="Cannot cancel task")
    mock_cancel_task_run_asyncio.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="cancel task run failed: Cannot cancel task"):
        await workflows_service.cancel_task_run("trn-test123")


@pytest.mark.asyncio
async def test_list_task_runs_success(
    mocker, mock_list_task_runs_asyncio, workflows_service, mock_task_run
):
    """Test successful task runs listing."""
    task_runs = [mock_task_run]
    mock_list_task_runs_asyncio.return_value = Response(
        status_code=200, content=b"", headers={}, parsed=task_runs
    )

    params = ListTaskRunsParams(limit=5, owner_id="test-owner")
    result = await workflows_service.list_task_runs(params)

    assert len(result) == 1
    assert result[0].id == "trn-test123"
    mock_list_task_runs_asyncio.assert_called_once_with(
        client=workflows_service.client.internal,
        limit=5,
        cursor=mocker.ANY,
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


@pytest.mark.parametrize(
    "status,expected",
    [
        (TaskRunStatus.RUNNING, False),
        (TaskRunStatus.COMPLETED, True),
        (TaskRunStatus.FAILED, True),
    ],
)
def test_is_terminal_status(mock_task_run, mock_workflows_service, status, expected):
    """Test terminal status detection."""
    mock_task_run.status = status
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)
    assert awaitable_task_run.is_terminal_status() == expected


@pytest.mark.asyncio
async def test_await_already_completed_task(
    mocker, mock_task_run, mock_workflows_service, mock_task_run_details
):
    """Test awaiting an already completed task."""
    # Set task as completed
    mock_task_run.status = TaskRunStatus.COMPLETED
    awaitable_task_run = AwaitableTaskRun(mock_task_run, mock_workflows_service)

    # Mock the get_task_run call
    mock_workflows_service.get_task_run = mocker.AsyncMock(
        return_value=mock_task_run_details
    )

    result = await awaitable_task_run

    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    mock_workflows_service.get_task_run.assert_called_once_with("trn-test123")
