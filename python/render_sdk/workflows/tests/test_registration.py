#!/usr/bin/env python3
"""Unit tests for task registration functionality."""

import pytest

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


# Task Registration Tests
def test_basic_task_registration(task_registry, task_decorator):
    """Test that basic tasks are registered correctly."""

    @task_decorator
    def simple_task(x: int) -> int:
        return x * 2

    # Verify task is registered
    task_names = task_registry.get_task_names()
    assert "simple_task" in task_names
    assert len(task_names) == 1

    # Verify task info
    task_info = task_registry.get_task("simple_task")
    assert task_info is not None
    assert task_info.func.__name__ == "simple_task"
    # Tasks always get an Options object, but with retry=None when no options provided
    if task_info.options:
        assert task_info.options.retry is None


def test_custom_name_registration(task_registry, task_decorator):
    """Test task registration with custom name."""

    @task_decorator(name="custom_name")
    def original_function(data: str) -> str:
        return data.upper()

    # Verify custom name is used
    task_names = task_registry.get_task_names()
    assert "custom_name" in task_names
    assert "original_function" not in task_names

    task_info = task_registry.get_task("custom_name")
    assert task_info.func.__name__ == "original_function"


def test_duplicate_task_registration(task_registry, task_decorator):
    """Test that duplicate task registration raises an error."""

    @task_decorator
    def duplicate_task(value: int) -> int:
        return value + 1

    with pytest.raises(ValueError, match="Task 'duplicate_task' already registered"):

        @task_decorator
        def duplicate_task(value: int) -> int:  # noqa: F811
            return value + 2


def test_task_registration_with_options_object():
    """Test task registration with different Options configurations."""
    registry = TaskRegistry()
    task_decorator = create_task_decorator(registry)

    # Task with None options
    @task_decorator(options=None)
    def task_with_none_options(x: int) -> int:
        return x

    # Task with empty options
    @task_decorator(options=Options())
    def task_with_empty_options(x: int) -> int:
        return x

    # Task with only retry options
    @task_decorator(
        options=Options(retry=Retry(max_retries=1, wait_duration_ms=500, factor=1.0)),
    )
    def task_with_retry_only(x: int) -> int:
        return x

    # Verify all tasks registered correctly
    task_names = registry.get_task_names()
    assert len(task_names) == 3

    # Verify options are handled correctly
    none_task = registry.get_task("task_with_none_options")
    assert none_task.options is not None  # Always gets an Options object
    assert none_task.options.retry is None

    empty_task = registry.get_task("task_with_empty_options")
    assert empty_task.options is not None
    assert empty_task.options.retry is None

    retry_task = registry.get_task("task_with_retry_only")
    assert retry_task.options is not None
    assert retry_task.options.retry is not None
    assert retry_task.options.retry.max_retries == 1


def test_task_registration_preserves_function_attributes(task_registry, task_decorator):
    """Test that task registration preserves original function attributes."""

    @task_decorator
    def documented_task(x: int) -> int:
        """This is a documented function."""
        return x * 3

    # Verify the original function attributes are preserved
    assert documented_task.__name__ == "documented_task"
    assert documented_task.__doc__ == "This is a documented function."
