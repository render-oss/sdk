"""Task decorator and related functionality."""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class Retry:
    """Retry configuration for a task."""

    max_retries: int
    wait_duration_ms: int
    factor: float = 1.5


@dataclass
class Options:
    """Configuration options for a task."""

    retry: Optional[Retry] = None


class TaskResult:
    """Represents the result of a task execution."""

    def __init__(self, result: Any = None, error: Optional[Exception] = None):
        self._result = result
        self._error = error

    @property
    def result(self) -> Any:
        if self._error:
            raise self._error
        return self._result

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    def get(self, *output_vars):
        """Get the result and assign to output variables."""
        if self._error:
            raise self._error

        if isinstance(self._result, (list, tuple)):
            if len(output_vars) != len(self._result):
                raise ValueError(
                    f"Expected {len(self._result)} output variables, got {len(output_vars)}"
                )
            for i, var in enumerate(output_vars):
                if hasattr(var, "__setitem__"):
                    var[0] = self._result[i]
                else:
                    # For simple assignments, we can't modify the variable in place
                    # So we return the results instead
                    return self._result
        else:
            if len(output_vars) != 1:
                raise ValueError(f"Expected 1 output variable, got {len(output_vars)}")
            if hasattr(output_vars[0], "__setitem__"):
                output_vars[0][0] = self._result
            else:
                return self._result


class TaskContext(ABC):
    """Abstract base class for task context."""

    @abstractmethod
    def execute_task(self, task_func: Callable, *args, **kwargs) -> TaskResult:
        """Execute a task and return the result."""
        pass


class TaskInfo:
    """Information about a registered task."""

    def __init__(self, func: Callable, name: str, options: Optional[Options] = None):
        self.func = func
        self.name = name
        self.options = options or Options()


class TaskRegistry:
    """Registry for managing tasks."""

    def __init__(self):
        self._tasks: Dict[str, TaskInfo] = {}

    def register(
        self,
        func: Callable,
        name: Optional[str] = None,
        options: Optional[Options] = None,
    ) -> str:
        """Register a task function."""
        task_name = name or func.__name__

        task_info = TaskInfo(func, task_name, options)

        if task_name in self._tasks:
            raise ValueError(f"Task '{task_name}' already registered")

        self._tasks[task_name] = task_info
        return task_name

    def get_task(self, name: str) -> Optional[TaskInfo]:
        """Get a task by name."""
        return self._tasks.get(name)

    def get_task_names(self) -> List[str]:
        """Get all task names."""
        return list(self._tasks.keys())

    def execute_task(self, name: str, *args, **kwargs) -> TaskResult:
        """Execute a task by name."""
        task_info = self.get_task(name)
        if not task_info:
            return TaskResult(error=ValueError(f"Task '{name}' not found"))

        try:
            result = task_info.func(*args, **kwargs)
            return TaskResult(result=result)
        except Exception as e:
            return TaskResult(error=e)


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
        func: F = None, *, name: Optional[str] = None, options: Optional[Options] = None
    ) -> F:
        """
        Decorator to register a function as a task in the bound registry.

        Args:
            func: The function to decorate
            name: Optional name for the task (defaults to function name)
            options: Optional configuration options

        Returns:
            The decorated function
        """

        def decorator(f: F) -> F:
            task_name = registry.register(f, name, options)
            # Add the task name as an attribute so we can reference it later
            f._task_name = task_name
            return f

        if func is None:
            # Called with arguments: @task(name="...", options=...)
            return decorator
        else:
            # Called without arguments: @task
            return decorator(func)

    return task


_global_registry = TaskRegistry()
task = create_task_decorator(_global_registry)


def get_task_registry() -> TaskRegistry:
    """Get the global task registry."""
    return _global_registry
