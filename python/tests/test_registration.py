#!/usr/bin/env python3
"""Unit tests for task registration functionality."""

import unittest
import sys
import os
import json
from unittest.mock import Mock, patch

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from render.workflows import task, Options, Retry, get_task_registry
from render.workflows.runner import register


class TestTaskRegistration(unittest.TestCase):
    """Test task registration functionality."""

    def setUp(self):
        """Clear registry for clean tests."""
        registry = get_task_registry()
        registry._tasks.clear()

    def test_basic_task_registration(self):
        """Test that basic tasks are registered correctly."""
        @task
        def simple_task(x: int) -> int:
            return x * 2

        registry = get_task_registry()

        # Verify task is registered
        self.assertIn("simple_task", registry.get_task_names())
        self.assertEqual(len(registry.get_task_names()), 1)

        # Verify task info
        task_info = registry.get_task("simple_task")
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.func.__name__, "simple_task")
        # Tasks always get an Options object, but with retry=None when no options provided
        if task_info.options:
            self.assertIsNone(task_info.options.retry)

    def test_custom_name_registration(self):
        """Test task registration with custom name."""
        @task(name="custom_name")
        def original_function(data: str) -> str:
            return data.upper()

        registry = get_task_registry()

        # Verify custom name is used
        self.assertIn("custom_name", registry.get_task_names())
        self.assertNotIn("original_function", registry.get_task_names())

        task_info = registry.get_task("custom_name")
        self.assertEqual(task_info.func.__name__, "original_function")

    def test_retry_options_registration(self):
        """Test task registration with retry options."""
        @task(options=Options(retry=Retry(max_retries=3, wait_duration_ms=1000, factor=1.5)))
        def retry_task(value: int) -> int:
            return value + 1

        registry = get_task_registry()
        task_info = registry.get_task("retry_task")

        # Verify retry options
        self.assertIsNotNone(task_info.options)
        self.assertIsNotNone(task_info.options.retry)

        retry = task_info.options.retry
        self.assertEqual(retry.max_retries, 3)
        self.assertEqual(retry.wait_duration_ms, 1000)
        self.assertEqual(retry.factor, 1.5)

if __name__ == "__main__":
    unittest.main(verbosity=2)
