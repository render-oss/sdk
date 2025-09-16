#!/usr/bin/env python3
"""Tests for the task executor functionality."""

import os
import sys
import unittest
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from render.workflows import Options, Retry, TaskRegistry, create_task_decorator, task
from render.workflows.client import UDSClient
from render.workflows.executor import TaskExecutor


@pytest.mark.asyncio
class TestTaskExecution:
    """Test basic task execution without server communication."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.task_decorator = create_task_decorator(self.registry)
        self.mock_client = Mock(spec=UDSClient)
        self.mock_client.post_callback = AsyncMock()
        self.executor = TaskExecutor(self.registry, self.mock_client)

    async def test_simple_task_execution(self):
        """Test executing a simple task without subtasks."""

        # Define a simple task
        @self.task_decorator
        def add_numbers(a: int, b: int) -> int:
            return a + b

        # Execute the task
        result = await self.executor.execute("add_numbers", [5, 3])

        # Verify the result
        assert result == 8

        # Verify callback was sent
        self.mock_client.post_callback.assert_called_once()
        call_args = self.mock_client.post_callback.call_args[0][0]
        assert call_args.type == "complete"

    async def test_task_with_string_result(self):
        """Test task that returns a string."""

        @self.task_decorator
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        result = await self.executor.execute("greet", ["World"])

        assert result == "Hello, World!"
        self.mock_client.post_callback.assert_called_once()

    async def test_task_execution_error(self):
        """Test task execution that raises an error."""

        @self.task_decorator
        def failing_task(x: int) -> int:
            if x < 0:
                raise ValueError("Negative numbers not allowed")
            return x * 2

        # Test that exception is raised
        with pytest.raises(ValueError):
            await self.executor.execute("failing_task", [-5])

        # Verify error callback was sent
        self.mock_client.post_callback.assert_called_once()
        call_args = self.mock_client.post_callback.call_args[0][0]
        assert call_args.type == "error"
        assert "Negative numbers not allowed" in call_args.error

    async def test_nonexistent_task(self):
        """Test executing a task that doesn't exist."""
        with pytest.raises(ValueError):
            await self.executor.execute("nonexistent_task", [])

        # Verify error callback was sent
        self.mock_client.post_callback.assert_called_once()
        call_args = self.mock_client.post_callback.call_args[0][0]
        assert call_args.type == "error"


class TestTaskContext(unittest.TestCase):
    """Test task execution with direct function calls (preparing for future subtask socket calls)."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.task_decorator = create_task_decorator(self.registry)

    def test_subtask_execution(self):
        """Test executing subtasks within a task using direct calls."""

        # Define tasks
        @self.task_decorator
        def square(x: int) -> int:
            return x * x

        @self.task_decorator
        def add_squares(a: int, b: int) -> int:
            # Direct function calls for now, will become socket calls later
            result1 = square(a)
            result2 = square(b)
            return result1 + result2

        # Execute the compound task
        result = self.registry.execute_task("add_squares", 3, 4)

        # Should compute 3^2 + 4^2 = 9 + 16 = 25
        self.assertEqual(result.result, 25)

    def test_subtask_error_propagation(self):
        """Test that errors in subtasks are properly propagated."""

        @self.task_decorator
        def divide(a: int, b: int) -> float:
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

        @self.task_decorator
        def compute_ratio(x: int, y: int) -> float:
            # Direct function call for now, will become socket call later
            result = divide(x, y)
            return result * 2


        # Test error propagation
        result = self.registry.execute_task("compute_ratio", 10, 0)

        self.assertIsNotNone(result.error)
        self.assertIsInstance(result.error, ZeroDivisionError)


class TestTaskRegistry(unittest.TestCase):
    """Test the task registry functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.task_decorator = create_task_decorator(self.registry)

    def test_task_registration(self):
        """Test basic task registration."""

        @self.task_decorator
        def test_task(x: int) -> int:
            return x + 1

        # Check that task is registered
        task_info = self.registry.get_task("test_task")
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.name, "test_task")
        self.assertEqual(task_info.func, test_task)

    def test_custom_task_name(self):
        """Test registering task with custom name."""

        @self.task_decorator(name="custom_name")
        def my_function(x: str) -> str:
            return x.upper()

        task_info = self.registry.get_task("custom_name")
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.name, "custom_name")

    def test_task_with_options(self):
        """Test registering task with retry options."""

        @self.task_decorator(options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000, factor=2.0)))
        def retry_task(x: int) -> int:
            return x * 2

        retry_options = Options(
            retry=Retry(max_retries=3, wait_duration_ms=1000, factor=2.0)
        )
        task_info = self.registry.get_task("retry_task")
        self.assertIsNotNone(task_info.options)
        self.assertIsNotNone(task_info.options.retry)
        self.assertEqual(task_info.options.retry.max_retries, 3)
        self.assertEqual(task_info.options.retry.wait_duration_ms, 1000)
        self.assertEqual(task_info.options.retry.factor, 2.0)

    def test_task_execution_by_name(self):
        """Test executing tasks by name through registry."""

        @self.task_decorator
        def multiply(a: int, b: int) -> int:
            return a * b

        result = self.registry.execute_task("multiply", 6, 7)

        self.assertEqual(result.result, 42)
        self.assertIsNone(result.error)


@pytest.mark.asyncio
class TestExecutorIntegration:
    """Integration tests for the executor with realistic scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.task_decorator = create_task_decorator(self.registry)
        self.mock_client = Mock(spec=UDSClient)
        self.mock_client.post_callback = AsyncMock()

    async def test_complex_task_chain(self):
        """Test a complex chain of task executions."""

        # Define a set of interconnected tasks
        @self.task_decorator
        def increment(x: int) -> int:
            return x + 1

        @self.task_decorator
        def double(x: int) -> int:
            return x * 2

        @self.task_decorator
        def complex_calculation(start: int) -> int:
            # Direct function calls (will become socket calls in future)
            step1 = increment(start)
            step2 = double(step1)
            step3 = increment(step2)
            return step3

        # Execute the complex calculation
        executor = TaskExecutor(self.registry, self.mock_client)
        result = await executor.execute("complex_calculation", [5])

        # Should compute: ((5 + 1) * 2) + 1 = (6 * 2) + 1 = 12 + 1 = 13
        assert result == 13

    async def test_callback_format(self):
        """Test that callbacks are formatted correctly."""

        @self.task_decorator
        def simple_task(value: str) -> str:
            return f"processed: {value}"


        executor = TaskExecutor(self.registry, self.mock_client)
        result = await executor.execute("simple_task", ["test"])

        # Check that callback was called with correct format
        self.mock_client.post_callback.assert_called_once()
        call_args = self.mock_client.post_callback.call_args[0][0]

        # Verify callback structure
        assert call_args.type == "complete"
        assert call_args.result == "processed: test"


if __name__ == "__main__":
    # Set up logging for tests
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # Run tests
    unittest.main(verbosity=2)
