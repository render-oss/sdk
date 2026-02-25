#!/usr/bin/env python3
"""Unit tests for the RenderSync entry point."""

import pytest

from render_sdk.client.workflows_sync import SyncWorkflowsService
from render_sdk.experimental.experimental_sync import SyncExperimentalService
from render_sdk.render_sync import RenderSync


@pytest.fixture
def mock_authenticated_client(mocker):
    client = mocker.Mock()
    client._base_url = "https://api.test.com/v1"
    return client


@pytest.fixture
def render_sync(mocker, mock_authenticated_client):
    mocker.patch(
        "render_sdk.client.client.AuthenticatedClient",
        return_value=mock_authenticated_client,
    )
    return RenderSync(token="test-token", base_url="https://api.test.com")


def test_render_sync_creates_sync_workflows_service(render_sync):
    assert isinstance(render_sync.workflows, SyncWorkflowsService)


def test_render_sync_creates_sync_experimental_service(render_sync):
    assert isinstance(render_sync.experimental, SyncExperimentalService)


def test_render_sync_exposes_client(render_sync):
    from render_sdk.client.client import Client

    assert isinstance(render_sync.client, Client)


def test_render_sync_requires_token():
    """RenderSync raises when no token is provided and env var is unset."""
    import os

    # Ensure the env var is not set
    old = os.environ.pop("RENDER_API_KEY", None)
    try:
        with pytest.raises(ValueError, match="provide a token"):
            RenderSync()
    finally:
        if old is not None:
            os.environ["RENDER_API_KEY"] = old
