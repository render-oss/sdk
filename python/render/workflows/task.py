"""Task decorator and related functionality."""

from __future__ import annotations

import functools
import inspect
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from itertools import islice
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    ParamSpec,
    Protocol,
    TypeVar,
    overload,
)

if TYPE_CHECKING:
    from render.workflows.context import TaskContext

# P is the task's own inputs, i.e. everything after the leading TaskContext.
# Task bodies are therefore Callable[Concatenate[TaskContext, P], R | Awaitable[R]].
P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class Retry:
    """Retry configuration for a task."""

    max_retries: int
    wait_duration_ms: int
    backoff_scaling: float = 1.5

    @classmethod
    def from_dict(cls, d: dict) -> Retry:
        return cls(
            max_retries=d["max_retries"],
            wait_duration_ms=d["wait_duration_ms"],
            backoff_scaling=d["backoff_scaling"],
        )


@dataclass
class Options:
    """Configuration options for a task.

    Attributes:
        retry: Retry configuration for automatic task retries.
        timeout_seconds: Task execution timeout in seconds (30-86400).
        plan: Resource plan for task execution. Options: "starter" (0.5CPU/512MB),
              "standard" (1CPU/2GB), "pro" (2CPU/4GB). Defaults to "standard".
    """

    retry: Retry | None = None
    timeout_seconds: int | None = None
    plan: str | None = None

    def __post_init__(self):
        if isinstance(self.retry, dict):
            self.retry = Retry.from_dict(self.retry)


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


def _verify_signature(func: Callable, task_name: str) -> None:
    """Reject tasks that cannot accept a context as their first argument."""
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())

    if not parameters:
        raise ValueError(
            f"Task '{task_name}' must accept a TaskContext as its first "
            f"parameter, e.g. def {task_name}(ctx, ...)."
        )

    first = parameters[0]
    if first.kind in (
        inspect.Parameter.KEYWORD_ONLY,
        inspect.Parameter.VAR_KEYWORD,
    ):
        raise ValueError(
            f"Task '{task_name}' must accept a TaskContext as its first "
            f"positional parameter, but '{first.name}' is keyword-only."
        )


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
        """
        Extract the task's input parameters from its function signature.

        The leading context parameter is supplied by the runtime rather than by
        the caller, so it is not part of the task's declared inputs.
        """
        sig = inspect.signature(func)
        parameters: list[ParameterInfo] = []

        for param_name, param in islice(sig.parameters.items(), 1, None):
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

        _verify_signature(func, task_name)
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


class TaskDefinition(Generic[P, R]):
    """A registered task."""

    def __init__(
        self,
        func: Callable[Concatenate[TaskContext, P], R | Awaitable[R]],
        name: str,
    ) -> None:
        # Copy function attributes for introspection. This runs before the
        # assignments below because update_wrapper ends by copying func.__dict__
        # over this object, which would otherwise overwrite them.
        #
        # The ignore is because update_wrapper is typed for callable wrappers,
        # and a definition is deliberately not callable.
        functools.update_wrapper(self, func)  # type: ignore[arg-type]
        self.func = func
        self.name = name

    def __repr__(self) -> str:
        return f"TaskDefinition(name={self.name!r})"


class BoundTaskDecorator(Protocol):
    """The decorator produced by calling ``task(...)`` with options."""

    # The async overload must stay first: a coroutine function also matches the
    # sync signature, with R bound to the coroutine rather than its result.
    @overload
    def __call__(
        self, func: Callable[Concatenate[TaskContext, P], Awaitable[R]], /
    ) -> TaskDefinition[P, R]: ...

    @overload
    def __call__(
        self, func: Callable[Concatenate[TaskContext, P], R], /
    ) -> TaskDefinition[P, R]: ...


class TaskDecorator(Protocol):
    """
    The decorator returned by :func:`create_task_decorator`.

    A Protocol rather than a Callable so that the ``@task`` and ``@task(...)``
    forms keep their distinct return types.
    """

    @overload
    def __call__(
        self,
        func: Callable[Concatenate[TaskContext, P], Awaitable[R]],
        /,
        *,
        name: str | None = ...,
        options: Options | None = ...,
    ) -> TaskDefinition[P, R]: ...

    @overload
    def __call__(
        self,
        func: Callable[Concatenate[TaskContext, P], R],
        /,
        *,
        name: str | None = ...,
        options: Options | None = ...,
    ) -> TaskDefinition[P, R]: ...

    @overload
    def __call__(
        self,
        *,
        name: str | None = ...,
        options: Options | None = ...,
    ) -> BoundTaskDecorator: ...


def create_task_decorator(registry: TaskRegistry) -> TaskDecorator:
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
        def my_task(ctx: TaskContext, value: int) -> int:
            return value * 2
    """

    def task(
        func: Callable[..., Any] | None = None,
        *,
        name: str | None = None,
        options: Options | None = None,
    ) -> Any:
        """
        Decorator to register a function as a task in the bound registry.

        The decorated function takes a TaskContext as its first parameter,
        followed by its inputs.

        Args:
            func: The function to decorate
            name: Optional name for the task (defaults to function name)
            options: Optional configuration options

        Returns:
            A TaskDefinition wrapping the decorated function
        """

        def decorator(f: Callable[..., Any]) -> TaskDefinition:
            task_name = registry.register(f, name, options)

            return TaskDefinition(f, task_name)

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
