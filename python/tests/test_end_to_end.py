#!/usr/bin/env python3
"""End-to-end tests that simulate the full workflow like the Go SDK example."""

import sys
import os
import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import json
import pytest

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from render_tasks import task, get_task_registry, Options, Retry
from render_tasks.executor import TaskExecutor
from render_tasks.client import UDSClient
from render_tasks.runner import register

class TestEndToEnd:
    """End-to-end tests."""

    def setup_method(self):
        """Set up test fixtures - clear registry for clean tests."""
        # Get a fresh registry for each test
        self.registry = get_task_registry()
        # Clear any existing tasks
        self.registry._tasks.clear()

        self.mock_client = Mock(spec=UDSClient)
        self.executor = TaskExecutor(self.registry, self.mock_client)

    @patch('render_tasks.runner.UDSClient')
    def test_task_registration_network_payload(self, mock_uds_client_class):
        """Test that task registration actually sends the correct payload over the network."""

        # Set up the mock
        mock_client_instance = Mock()
        mock_uds_client_class.return_value = mock_client_instance
        mock_client_instance.register_tasks = AsyncMock(return_value={"status": "success"})
        mock_client_instance.disconnect = AsyncMock()

        # Define tasks with various configurations
        @task
        def simple_task(x: int) -> int:
            return x * 2

        @task(name="custom_name")
        def renamed_task(msg: str) -> str:
            return f"Hello {msg}"

        @task(options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000, factor=1.5)))
        def retry_task(data: str) -> str:
            return data.upper()

        # Call the actual registration function
        register("/tmp/test.sock")

        # Verify that UDSClient was instantiated with correct socket path
        mock_uds_client_class.assert_called_once_with("/tmp/test.sock")

        # Verify that register_tasks was called exactly once
        mock_client_instance.register_tasks.assert_called_once()

        # Get the actual payload that was sent
        sent_tasks = mock_client_instance.register_tasks.call_args[0][0]

        # Verify we have the expected number of tasks
        assert len(sent_tasks) == 3

        # Find tasks by name to verify their structure
        task_by_name = {task.name: task for task in sent_tasks}

        # Verify simple task
        assert "simple_task" in task_by_name
        simple_task_payload = task_by_name["simple_task"]
        assert simple_task_payload.name == "simple_task"
        assert simple_task_payload.options is None

        # Verify renamed task
        assert "custom_name" in task_by_name
        renamed_task_payload = task_by_name["custom_name"]
        assert renamed_task_payload.name == "custom_name"
        assert renamed_task_payload.options is None

        # Verify retry task with options
        assert "retry_task" in task_by_name
        retry_task_payload = task_by_name["retry_task"]
        assert retry_task_payload.name == "retry_task"
        assert retry_task_payload.options is not None

        # Verify retry options structure
        retry_options = retry_task_payload.options["retry"]
        assert retry_options["max_retries"] == 3
        assert retry_options["wait_duration_ms"] == 1000
        assert retry_options["factor"] == 1.5

        # Verify disconnect was called
        mock_client_instance.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_callback_payloads_with_mocked_client(self):
        """Test that callback payloads are correctly formatted and sent."""

        @task
        def test_task(value: int) -> int:
            return value * 10

        @task
        def failing_task(should_fail: bool) -> str:
            if should_fail:
                raise ValueError("Test failure")
            return "success"

        # Test success callback
        mock_client = Mock(spec=UDSClient)
        mock_client.post_callback = AsyncMock()
        executor = TaskExecutor(self.registry, mock_client)

        result = await executor.execute("test_task", [5])
        assert result == 50

        # Verify success callback was sent with correct payload
        mock_client.post_callback.assert_called_once()
        success_payload = mock_client.post_callback.call_args[0][0]
        assert success_payload.type == "complete"
        assert success_payload.result == 50

        # Reset mock and test error callback
        mock_client.reset_mock()

        with pytest.raises(ValueError):
            await executor.execute("failing_task", [True])

        # Verify error callback was sent with correct payload
        mock_client.post_callback.assert_called_once()
        error_payload = mock_client.post_callback.call_args[0][0]
        assert error_payload.type == "error"
        assert "Test failure" in error_payload.error

if __name__ == "__main__":
    # Set up logging for tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Run tests
    unittest.main(verbosity=2)
