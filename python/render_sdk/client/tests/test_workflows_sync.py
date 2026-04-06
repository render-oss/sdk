#!/usr/bin/env python3
"""Unit tests for the synchronous Render REST API client functionality."""

import datetime
import json

import pytest

from render_sdk.client import Client, ListTaskRunsParams
from render_sdk.client.errors import ClientError, ServerError
from render_sdk.client.workflows_sync import SyncWorkflowsService
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
        attempts=[],
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
        attempts=[],
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
def sync_workflows_service(client):
    """Create a SyncWorkflowsService instance."""
    return SyncWorkflowsService(client)


@pytest.fixture
def mock_cancel_task_run_sync(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflow_tasks_beta.cancel_task_run.sync_detailed"
    )


@pytest.fixture
def mock_list_task_runs_sync(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflow_tasks_beta.list_task_runs.sync_detailed"
    )


@pytest.fixture
def mock_create_task_sync(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflow_tasks_beta.create_task.sync_detailed"
    )


@pytest.fixture
def mock_get_task_run_sync(mocker):
    return mocker.patch(
        "render_sdk.public_api.api.workflow_tasks_beta.get_task_run.sync_detailed"
    )


def test_start_task_success(
    mock_create_task_sync, sync_workflows_service, mock_task_run
):
    """Test successful task start."""
    mock_create_task_sync.return_value = Response(
        status_code=202, content=b"", headers={}, parsed=mock_task_run
    )

    result = sync_workflows_service.start_task("test-task", {"input": "data"})

    assert isinstance(result, TaskRun)
    assert result.id == "trn-test123"
    mock_create_task_sync.assert_called_once()


def test_start_task_failure(mock_create_task_sync, sync_workflows_service):
    """Test task start failure."""

    error = Error(message="Task creation failed")
    mock_create_task_sync.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="create task failed: Task creation failed"):
        sync_workflows_service.start_task("test-task", {"input": "data"})


def test_run_task_returns_task_run_details(
    mocker,
    mock_create_task_sync,
    sync_workflows_service,
    mock_task_run,
    mock_task_run_details,
):
    """Test that run_task starts a task and waits for completion."""
    mock_create_task_sync.return_value = Response(
        status_code=202, content=b"", headers={}, parsed=mock_task_run
    )
    mocker.patch.object(
        sync_workflows_service,
        "_task_run_completed_with_sse",
        return_value=mock_task_run_details,
    )

    result = sync_workflows_service.run_task("test-task", {"input": "data"})

    assert isinstance(result, TaskRunDetails)
    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED


def test_run_task_failure(mock_create_task_sync, sync_workflows_service):
    """Test that run_task propagates errors from start_task."""
    error = Error(message="Task creation failed")
    mock_create_task_sync.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="create task failed: Task creation failed"):
        sync_workflows_service.run_task("test-task", {"input": "data"})


def test_get_task_run_success(
    mock_get_task_run_sync, sync_workflows_service, mock_task_run_details
):
    """Test successful task run retrieval."""
    mock_get_task_run_sync.return_value = Response(
        status_code=200, content=b"", headers={}, parsed=mock_task_run_details
    )

    result = sync_workflows_service.get_task_run("trn-test123")

    assert result.id == "trn-test123"
    assert result.status.value == TaskRunStatus.COMPLETED
    mock_get_task_run_sync.assert_called_once_with(
        client=sync_workflows_service.client.internal, task_run_id="trn-test123"
    )


def test_get_task_run_failure(mock_get_task_run_sync, sync_workflows_service):
    """Test task run retrieval failure."""
    error = Error(message="Task not found")
    mock_get_task_run_sync.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="get task run failed: Task not found"):
        sync_workflows_service.get_task_run("trn-test123")


def test_cancel_task_run_success(mock_cancel_task_run_sync, sync_workflows_service):
    """Test successful task run cancellation."""
    mock_cancel_task_run_sync.return_value = Response(
        status_code=204, content=b"", headers={}, parsed=None
    )

    sync_workflows_service.cancel_task_run("trn-test123")

    mock_cancel_task_run_sync.assert_called_once_with(
        client=sync_workflows_service.client.internal, task_run_id="trn-test123"
    )


def test_cancel_task_run_failure(mock_cancel_task_run_sync, sync_workflows_service):
    """Test task run cancellation failure."""
    error = Error(message="Cannot cancel task")
    mock_cancel_task_run_sync.return_value = Response(
        status_code=400, content=b"", headers={}, parsed=error
    )

    with pytest.raises(ClientError, match="cancel task run failed: Cannot cancel task"):
        sync_workflows_service.cancel_task_run("trn-test123")


def test_list_task_runs_success(
    mocker, mock_list_task_runs_sync, sync_workflows_service, mock_task_run
):
    """Test successful task runs listing."""
    task_runs = [mock_task_run]
    mock_list_task_runs_sync.return_value = Response(
        status_code=200, content=b"", headers={}, parsed=task_runs
    )

    params = ListTaskRunsParams(limit=5, owner_id="test-owner")
    result = sync_workflows_service.list_task_runs(params)

    assert len(result) == 1
    assert result[0].id == "trn-test123"
    mock_list_task_runs_sync.assert_called_once_with(
        client=sync_workflows_service.client.internal,
        limit=5,
        cursor=mocker.ANY,
        owner_id="test-owner",
    )


@pytest.fixture
def mock_httpx_stream(mocker):
    """Mock httpx.Client to return a controllable SSE stream.

    Returns a list that tests populate with bytes chunks before calling
    task_run_events(). The mock wires up the nested context managers
    (Client → stream → response.iter_bytes).
    """
    chunks: list[bytes] = []

    def iter_bytes():
        yield from chunks

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.iter_bytes = iter_bytes

    stream_cm = mocker.MagicMock()
    stream_cm.__enter__ = mocker.Mock(return_value=mock_response)
    stream_cm.__exit__ = mocker.Mock(return_value=False)

    mock_http_client = mocker.Mock()
    mock_http_client.stream.return_value = stream_cm

    client_cm = mocker.MagicMock()
    client_cm.__enter__ = mocker.Mock(return_value=mock_http_client)
    client_cm.__exit__ = mocker.Mock(return_value=False)

    mocker.patch(
        "render_sdk.client.workflows_sync.httpx.Client", return_value=client_cm
    )

    return chunks, mock_response


def test_task_run_events_yields_events(sync_workflows_service, mock_httpx_stream):
    """Test that task_run_events streams and yields TaskRunDetails."""
    chunks, _ = mock_httpx_stream

    details = TaskRunDetails(
        id="trn-test123",
        task_id="tsk-test123",
        status=TaskRunStatus.COMPLETED,
        results=[42],
        input_=[],
        parent_task_run_id=None,
        root_task_run_id=None,
        retries=0,
        attempts=[],
    )
    sse_payload = json.dumps(details.to_dict()).encode()
    chunks.append(b"event: task.completed\ndata: " + sse_payload + b"\n\n")

    events = []
    for event in sync_workflows_service.task_run_events(["trn-test123"]):
        events.append(event)

    assert len(events) == 1
    assert events[0].id == "trn-test123"
    assert events[0].status.value == TaskRunStatus.COMPLETED


def test_task_run_events_raises_on_http_error(
    sync_workflows_service, mock_httpx_stream
):
    """Test that task_run_events raises on HTTP errors."""
    _, mock_response = mock_httpx_stream

    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_response.json.return_value = {"message": "Internal Server Error"}

    with pytest.raises(ServerError):
        for _ in sync_workflows_service.task_run_events(["trn-test123"]):
            pass
