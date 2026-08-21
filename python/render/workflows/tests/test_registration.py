#!/usr/bin/env python3
"""Unit tests for task registration functionality."""

import pytest

from render.workflows.task import (
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
    def simple_task(ctx, x: int) -> int:
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


def test_context_parameter_is_not_a_declared_input(task_registry, task_decorator):
    """The leading context is supplied by the runtime, not by the caller."""

    @task_decorator
    def simple_task(ctx, x: int, flag: bool = False) -> int:
        return x * 2

    task_info = task_registry.get_task("simple_task")
    assert [p.name for p in task_info.parameters] == ["x", "flag"]
    assert [p.type_hint for p in task_info.parameters] == ["int", "bool"]
    assert [p.has_default for p in task_info.parameters] == [False, True]


def test_task_with_only_a_context_has_no_declared_inputs(task_registry, task_decorator):
    """A task that takes nothing but the context registers zero parameters."""

    @task_decorator
    def ping(ctx) -> str:
        return "pong"

    assert task_registry.get_task("ping").parameters == []


def test_task_without_a_context_parameter_is_rejected(task_decorator):
    """A task must be able to receive a context as its first argument."""

    with pytest.raises(ValueError, match="must accept a TaskContext"):

        @task_decorator
        def no_context() -> int:
            return 1


def test_task_with_keyword_only_first_parameter_is_rejected(task_decorator):
    """The context is passed positionally, so it cannot be keyword-only."""

    with pytest.raises(ValueError, match="keyword-only"):

        @task_decorator
        def keyword_only(*, ctx) -> int:
            return 1


def test_definition_exposes_the_function_for_in_process_invocation(task_decorator):
    """A definition hands back the undecorated function for direct calls."""

    @task_decorator
    def square(ctx, a: int) -> int:
        return a * a

    assert square.func(object(), 5) == 25
    assert square.name == "square"


def test_function_attributes_do_not_overwrite_definition_fields(task_decorator):
    """
    A function carrying its own `name` attribute must not clobber the task name.

    functools.update_wrapper copies the function's __dict__ over the definition,
    so the definition's own fields have to be assigned after it runs. This test
    pins that ordering.
    """

    def tagged(ctx, a: int) -> int:
        return a

    tagged.name = "attribute-from-the-function"
    tagged.func = "also-not-ours"

    definition = task_decorator(tagged)

    assert definition.name == "tagged"
    assert definition.func is tagged


def test_definition_is_not_callable(task_decorator):
    """Running a task goes through a context, so a definition is inert."""

    @task_decorator
    def square(ctx, a: int) -> int:
        return a * a

    assert not callable(square)
    with pytest.raises(TypeError):
        square(object(), 5)


def test_custom_name_registration(task_registry, task_decorator):
    """Test task registration with custom name."""

    @task_decorator(name="custom_name")
    def original_function(ctx, data: str) -> str:
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
    def duplicate_task(ctx, value: int) -> int:
        return value + 1

    with pytest.raises(ValueError, match="Task 'duplicate_task' already registered"):

        @task_decorator
        def duplicate_task(ctx, value: int) -> int:  # noqa: F811
            return value + 2


def test_task_registration_with_options_object():
    """Test task registration with different Options configurations."""
    registry = TaskRegistry()
    task_decorator = create_task_decorator(registry)

    # Task with None options
    @task_decorator(options=None)
    def task_with_none_options(ctx, x: int) -> int:
        return x

    # Task with empty options
    @task_decorator(options=Options())
    def task_with_empty_options(ctx, x: int) -> int:
        return x

    # Task with only retry options
    @task_decorator(
        options=Options(
            retry=Retry(max_retries=1, wait_duration_ms=500, backoff_scaling=1.0)
        ),
    )
    def task_with_retry_only(ctx, x: int) -> int:
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


def test_options_coerces_dict_retry_to_retry():
    """
    Test that Options.__post_init__ coerces a dict retry config to a Retry instance.
    """
    options = Options(
        retry={"max_retries": 5, "wait_duration_ms": 2000, "backoff_scaling": 2.0}
    )
    assert isinstance(options.retry, Retry)
    assert options.retry.max_retries == 5
    assert options.retry.wait_duration_ms == 2000
    assert options.retry.backoff_scaling == 2.0


def test_options_rejects_incomplete_dict_retry():
    """Test that dict-to-Retry coercion raises KeyError for missing required keys."""
    with pytest.raises(KeyError):
        Options(retry={})


def test_task_registration_preserves_function_attributes(task_registry, task_decorator):
    """Test that task registration preserves original function attributes."""

    @task_decorator
    def documented_task(ctx, x: int) -> int:
        """This is a documented function."""
        return x * 3

    # Verify the original function attributes are preserved
    assert documented_task.__name__ == "documented_task"
    assert documented_task.__doc__ == "This is a documented function."


def test_task_registration_with_timeout_seconds():
    """Test task registration with timeout_seconds option."""
    registry = TaskRegistry()
    task_decorator = create_task_decorator(registry)

    # Task with timeout_seconds
    @task_decorator(options=Options(timeout_seconds=120))
    def task_with_timeout(ctx, x: int) -> int:
        return x

    # Verify task registered correctly
    task_names = registry.get_task_names()
    assert "task_with_timeout" in task_names

    # Verify timeout_seconds is set
    task_info = registry.get_task("task_with_timeout")
    assert task_info.options is not None
    assert task_info.options.timeout_seconds == 120


def test_task_registration_without_timeout_seconds():
    """Test task registration without timeout_seconds defaults to None."""
    registry = TaskRegistry()
    task_decorator = create_task_decorator(registry)

    @task_decorator
    def task_without_timeout(ctx, x: int) -> int:
        return x

    task_info = registry.get_task("task_without_timeout")
    assert task_info.options is not None
    assert task_info.options.timeout_seconds is None


def test_task_registration_with_timeout_and_retry():
    """Test task registration with both timeout_seconds and retry options."""
    registry = TaskRegistry()
    task_decorator = create_task_decorator(registry)

    @task_decorator(
        options=Options(
            timeout_seconds=300,
            retry=Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0),
        )
    )
    def task_with_both(ctx, x: int) -> int:
        return x

    task_info = registry.get_task("task_with_both")
    assert task_info.options is not None
    assert task_info.options.timeout_seconds == 300
    assert task_info.options.retry is not None
    assert task_info.options.retry.max_retries == 3
