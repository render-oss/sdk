"""Task decorator and related functionality."""

import contextvars
import functools
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# Context variable to hold the current client for subtask execution
_current_client: contextvars.ContextVar = contextvars.ContextVar("current_client")


@dataclass
class Retry:
    """Retry configuration for a task."""

    max_retries: int
    wait_duration_ms: int
    factor: float = 1.5


@dataclass
class Options:
    """Configuration options for a task."""

    retry: Retry | None = None


class TaskResult:
    """Represents the result of a task execution."""

    def __init__(self, result: Any = None, error: Exception | None = None):
        self._result = result
        self._error = error

    @property
    def result(self) -> Any:
        if self._error:
            raise self._error
        return self._result

    @property
    def error(self) -> Exception | None:
        return self._error


class TaskContext(ABC):
    """Abstract base class for task context."""

    @abstractmethod
    def execute_task(self, task_func: Callable, *args, **kwargs) -> TaskResult:
        """Execute a task and return the result."""


class TaskInfo:
    """Information about a registered task."""

    def __init__(self, func: Callable, name: str, options: Options | None = None):
        self.func = func
        self.name = name
        self.options = options or Options()


class TaskRegistry:
    """Registry for managing tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, TaskInfo] = {}

    def register(
        self,
        func: Callable,
        name: str | None = None,
        options: Options | None = None,
    ) -> str:
        """Register a task function."""
        task_name = name or func.__name__

        task_info = TaskInfo(func, task_name, options)

        if task_name in self._tasks:
            raise ValueError(f"Task '{task_name}' already registered")

        self._tasks[task_name] = task_info
        return task_name

    def get_task(self, name: str) -> TaskInfo | None:
        """Get a task by name."""
        return self._tasks.get(name)

    def get_task_names(self) -> list[str]:
        """Get all task names."""
        return list(self._tasks.keys())

    def get_function(self, name: str) -> Callable | None:
        """Execute a task by name."""
        task_info = self.get_task(name)
        if not task_info:
            return None

        return task_info.func


class TaskCallable:
    """A callable that can be awaited to run as a subtask."""

    def __init__(self, func, name):
        self._func = func
        self._name = name
        # Copy function attributes for introspection
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        # Store args for potential await
        self._args = args
        self._kwargs = kwargs
        return self

    def __await__(self):
        """Run as a subtask when awaited."""

        async def run_subtask():
            try:
                client = _current_client.get()
                return await client.run_subtask(self._name, list(self._args))
            except LookupError as e:
                raise RuntimeError(
                    f"Cannot run {self._name} as subtask \
                      outside of task execution context"
                ) from e

        return run_subtask().__await__()


def create_task_decorator(registry: TaskRegistry) -> Callable:
    """
    Create a task decorator bound to a specific registry.

    Args:
        registry: The TaskRegistry to register tasks with

    Returns:
        A task decorator function

    Example:
        registry = TaskRegistry()
        task = create_task_decorator(registry)

        @task
        def my_task(value: int) -> int:
            return value * 2
    """

    def task(
        func: F | None = None,
        *,
        name: str | None = None,
        options: Options | None = None,
    ) -> F | Callable[[F], TaskCallable]:
        """
        Decorator to register a function as a task in the bound registry.

        Args:
            func: The function to decorate
            name: Optional name for the task (defaults to function name)
            options: Optional configuration options

        Returns:
            The decorated function
        """

        def decorator(f: F) -> TaskCallable:
            task_name = registry.register(f, name, options)

            return TaskCallable(f, task_name)

        if func is None:
            # Called with arguments: @task(name="...", options=...)
            return decorator
        # Called without arguments: @task
        return decorator(func)

    return task


_global_registry = TaskRegistry()
task = create_task_decorator(_global_registry)


def get_task_registry() -> TaskRegistry:
    """Get the global task registry."""
    return _global_registry
