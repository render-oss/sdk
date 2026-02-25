#!/usr/bin/env python3
"""Unit tests for the Render entry point."""

import pytest

from render_sdk.client.workflows_sync import SyncWorkflowsService
from render_sdk.experimental.experimental_sync import SyncExperimentalService
from render_sdk.render import Render


@pytest.fixture
def mock_authenticated_client(mocker):
    client = mocker.Mock()
    client._base_url = "https://api.test.com/v1"
    return client


@pytest.fixture
def render(mocker, mock_authenticated_client):
    mocker.patch(
        "render_sdk.client.client.AuthenticatedClient",
        return_value=mock_authenticated_client,
    )
    return Render(token="test-token", base_url="https://api.test.com")


def test_render_creates_sync_workflows_service(render):
    assert isinstance(render.workflows, SyncWorkflowsService)


def test_render_creates_sync_experimental_service(render):
    assert isinstance(render.experimental, SyncExperimentalService)


def test_render_exposes_client(render):
    from render_sdk.client.client import Client

    assert isinstance(render.client, Client)


def test_render_requires_token():
    """Render raises when no token is provided and env var is unset."""
    import os

    # Ensure the env var is not set
    old = os.environ.pop("RENDER_API_KEY", None)
    try:
        with pytest.raises(ValueError, match="provide a token"):
            Render()
    finally:
        if old is not None:
            os.environ["RENDER_API_KEY"] = old
