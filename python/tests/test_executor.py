#!/usr/bin/env python3
"""Tests for the task executor functionality."""

import sys
import os
import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import json
import pytest

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from render_tasks.task import task, TaskContext, TaskRegistry, Options, Retry
from render_tasks.executor import TaskExecutor, ExecutorTaskContext
from render_tasks.client import UDSClient

@pytest.mark.asyncio
class TestTaskExecution:
    """Test basic task execution without server communication."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.mock_client = Mock(spec=UDSClient)
        self.mock_client.post_callback = AsyncMock()
        self.executor = TaskExecutor(self.registry, self.mock_client)

    async def test_simple_task_execution(self):
        """Test executing a simple task without subtasks."""
        # Define a simple task
        @task
        def add_numbers(ctx: TaskContext, a: int, b: int) -> int:
            return a + b

        # Register the task manually
        self.registry.register(add_numbers)

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
        @task
        def greet(ctx: TaskContext, name: str) -> str:
            return f"Hello, {name}!"

        self.registry.register(greet)

        result = await self.executor.execute("greet", ["World"])

        assert result == "Hello, World!"
        self.mock_client.post_callback.assert_called_once()

    async def test_task_execution_error(self):
        """Test task execution that raises an error."""
        @task
        def failing_task(ctx: TaskContext, x: int) -> int:
            if x < 0:
                raise ValueError("Negative numbers not allowed")
            return x * 2

        self.registry.register(failing_task)

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
    """Test TaskContext functionality and subtask execution."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.mock_client = Mock(spec=UDSClient)
        self.ctx = ExecutorTaskContext(self.mock_client, self.registry)

    def test_subtask_execution(self):
        """Test executing subtasks within a task."""
        # Define tasks
        @task
        def square(ctx: TaskContext, x: int) -> int:
            return x * x

        @task
        def add_squares(ctx: TaskContext, a: int, b: int) -> int:
            result1 = ctx.execute_task(square, a)
            result2 = ctx.execute_task(square, b)
            return result1.result + result2.result

        # Register tasks
        self.registry.register(square)
        self.registry.register(add_squares)

        # Execute the compound task
        result = self.ctx.execute_task(add_squares, 3, 4)

        # Should compute 3^2 + 4^2 = 9 + 16 = 25
        self.assertEqual(result.result, 25)

    def test_subtask_error_propagation(self):
        """Test that errors in subtasks are properly propagated."""
        @task
        def divide(ctx: TaskContext, a: int, b: int) -> float:
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

        @task
        def compute_ratio(ctx: TaskContext, x: int, y: int) -> float:
            result = ctx.execute_task(divide, x, y)
            return result.result * 2

        self.registry.register(divide)
        self.registry.register(compute_ratio)

        # Test error propagation
        result = self.ctx.execute_task(compute_ratio, 10, 0)

        self.assertIsNotNone(result.error)
        self.assertIsInstance(result.error, ZeroDivisionError)


class TestTaskRegistry(unittest.TestCase):
    """Test the task registry functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()

    def test_task_registration(self):
        """Test basic task registration."""
        @task
        def test_task(ctx: TaskContext, x: int) -> int:
            return x + 1

        name = self.registry.register(test_task)
        self.assertEqual(name, "test_task")

        # Check that task is registered
        task_info = self.registry.get_task("test_task")
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.name, "test_task")
        self.assertEqual(task_info.func, test_task)

    def test_custom_task_name(self):
        """Test registering task with custom name."""
        @task
        def my_function(ctx: TaskContext, x: str) -> str:
            return x.upper()

        name = self.registry.register(my_function, name="custom_name")
        self.assertEqual(name, "custom_name")

        task_info = self.registry.get_task("custom_name")
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.name, "custom_name")

    def test_task_with_options(self):
        """Test registering task with retry options."""
        @task
        def retry_task(ctx: TaskContext, x: int) -> int:
            return x * 2

        retry_options = Options(retry=Retry(max_retries=3, wait_duration_ms=1000, factor=2.0))
        name = self.registry.register(retry_task, options=retry_options)

        task_info = self.registry.get_task(name)
        self.assertIsNotNone(task_info.options)
        self.assertIsNotNone(task_info.options.retry)
        self.assertEqual(task_info.options.retry.max_retries, 3)
        self.assertEqual(task_info.options.retry.wait_duration_ms, 1000)
        self.assertEqual(task_info.options.retry.factor, 2.0)

    def test_invalid_task_signature(self):
        """Test that invalid task signatures are rejected."""
        # Task without TaskContext parameter
        def invalid_task(x: int) -> int:
            return x + 1

        with self.assertRaises(ValueError):
            self.registry.register(invalid_task)

    def test_task_execution_by_name(self):
        """Test executing tasks by name through registry."""
        @task
        def multiply(ctx: TaskContext, a: int, b: int) -> int:
            return a * b

        self.registry.register(multiply)

        # Create a mock context
        mock_ctx = Mock(spec=TaskContext)

        result = self.registry.execute_task("multiply", mock_ctx, 6, 7)

        self.assertEqual(result.result, 42)
        self.assertIsNone(result.error)


@pytest.mark.asyncio
class TestExecutorIntegration:
    """Integration tests for the executor with realistic scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = TaskRegistry()
        self.mock_client = Mock(spec=UDSClient)
        self.mock_client.post_callback = AsyncMock()

    async def test_complex_task_chain(self):
        """Test a complex chain of task executions."""
        # Define a set of interconnected tasks
        @task
        def increment(ctx: TaskContext, x: int) -> int:
            return x + 1

        @task
        def double(ctx: TaskContext, x: int) -> int:
            return x * 2

        @task
        def complex_calculation(ctx: TaskContext, start: int) -> int:
            # Increment, then double, then increment again
            step1 = ctx.execute_task(increment, start)
            step2 = ctx.execute_task(double, step1.result)
            step3 = ctx.execute_task(increment, step2.result)
            return step3.result

        # Register all tasks
        for func in [increment, double, complex_calculation]:
            self.registry.register(func)

        # Execute the complex calculation
        executor = TaskExecutor(self.registry, self.mock_client)
        result = await executor.execute("complex_calculation", [5])

        # Should compute: ((5 + 1) * 2) + 1 = (6 * 2) + 1 = 12 + 1 = 13
        assert result == 13

    async def test_callback_format(self):
        """Test that callbacks are formatted correctly."""
        @task
        def simple_task(ctx: TaskContext, value: str) -> str:
            return f"processed: {value}"

        self.registry.register(simple_task)

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
