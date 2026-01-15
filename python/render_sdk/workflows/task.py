"""Task decorator and related functionality."""

import asyncio
import contextvars
import functools
import inspect
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
    wait_duration: int
    backoff_scaling: float = 1.5


@dataclass
class Options:
    """Configuration options for a task."""

    retry: Retry | None = None
    timeout_seconds: int | None = None


@dataclass
class ParameterInfo:
    """
    Information about a task parameter extracted from the task's function
    signature.
    """

    name: str
    type_hint: str | None
    has_default: bool
    default_value: Any | None = None


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

    def __init__(
        self,
        func: Callable,
        name: str,
        options: Options | None = None,
        parameters: list[ParameterInfo] | None = None,
    ):
        self.func = func
        self.name = name
        self.options = options or Options()
        self.parameters = parameters


class TaskRegistry:
    """Registry for managing tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, TaskInfo] = {}

    def _extract_parameters(self, func: Callable) -> list[ParameterInfo]:
        """Extract parameter information from a function signature."""
        sig = inspect.signature(func)
        parameters: list[ParameterInfo] = []

        for param_name, param in sig.parameters.items():
            # Get type hint as string if available
            type_hint: str | None = None
            if param.annotation is not inspect.Parameter.empty:
                if hasattr(param.annotation, "__name__"):
                    type_hint = param.annotation.__name__
                else:
                    type_hint = str(param.annotation)

            # Check if the parameter has a default value
            has_default = param.default is not inspect.Parameter.empty
            default_value = param.default if has_default else None

            parameters.append(
                ParameterInfo(
                    name=param_name,
                    type_hint=type_hint,
                    has_default=has_default,
                    default_value=default_value,
                )
            )

        return parameters

    def register(
        self,
        func: Callable,
        name: str | None = None,
        options: Options | None = None,
    ) -> str:
        """Register a task function."""
        task_name = name or func.__name__

        parameters = self._extract_parameters(func)

        task_info = TaskInfo(func, task_name, options, parameters)

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


class TaskInstance:
    """Represents a single task execution that can be awaited."""

    def __init__(self, name: str, future: asyncio.Task):
        self._name = name
        self._future = future

    def __await__(self):
        """Await the task execution."""

        async def run_subtask():
            try:
                return await self._future
            except LookupError as e:
                raise RuntimeError(
                    f"Cannot run {self._name} as subtask \
                      outside of task execution context"
                ) from e

        return run_subtask().__await__()


class TaskCallable:
    """A callable that can be awaited to run as a subtask."""

    def __init__(self, func, name):
        self._func = func
        self._name = name
        # Copy function attributes for introspection
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        # Create a new TaskInstance for each call
        client = _current_client.get()

        # Error on mixed positional and kw args
        if args and kwargs:
            raise ValueError(
                "Cannot mix positional and keyword arguments when calling a task. "
                "Use either positional arguments (e.g., task(arg1, arg2)) or "
                "keyword arguments (e.g., task(param1=value1, param2=value2)), "
                "but not both."
            )

        # Determine input data type based on how the task was called
        if kwargs:
            # Named parameters: pass as dict
            input_data: dict[str, Any] = kwargs
        else:
            # Positional parameters: pass as list
            input_data = list(args)

        # Start execution immediately
        future = asyncio.create_task(client.run_subtask(self._name, input_data))
        return TaskInstance(self._name, future)


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
