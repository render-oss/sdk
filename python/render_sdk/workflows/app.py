"""Workflows application for defining durable tasks."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from render_sdk.workflows.runner import register, run
from render_sdk.workflows.task import (
    Options,
    Retry,
    TaskCallable,
    TaskRegistry,
    create_task_decorator,
)

F = TypeVar("F", bound=Callable[..., Any])


class Workflows:
    """
    Task definition app for Render Durable Workflows.

    This is the primary entry point for defining tasks that run on Render.
    For calling tasks via REST API, use the Render class instead.

    Example:
        app = Workflows()

        @app.task
        def my_task(x: int) -> int:
            return x * 2

    With configuration:
        app = Workflows(
            default_retry=Retry(max_retries=3, wait_duration_ms=1000),
            default_timeout=300,
        )

        @app.task
        def my_task(x: int) -> int:
            return x * 2

    Combining multiple modules:
        from tasks_a import app as app_a
        from tasks_b import app as app_b

        combined = Workflows.from_workflows(app_a, app_b)
    """

    _registry: TaskRegistry
    _default_retry: Retry | None
    _default_timeout: int | None
    _default_plan: str | None

    def __init__(
        self,
        *,
        default_retry: Retry | None = None,
        default_timeout: int | None = None,
        default_plan: str | None = None,
    ) -> None:
        """
        Initialize a Workflows application.

        Args:
            default_retry: Default retry configuration for all tasks.
            default_timeout: Default timeout in seconds for all tasks.
            default_plan: Default resource plan for all tasks.
        """
        self._registry = TaskRegistry()
        self._default_retry = default_retry
        self._default_timeout = default_timeout
        self._default_plan = default_plan

    def __repr__(self) -> str:
        task_count = len(self._registry.get_task_names())
        return f"Workflows(tasks={task_count})"

    def task(
        self,
        func: F | None = None,
        *,
        name: str | None = None,
        retry: Retry | None = None,
        timeout: int | None = None,
        plan: str | None = None,
    ) -> F | Callable[[F], TaskCallable]:
        """
        Decorator to register a function as a task.

        Args:
            func: The function to decorate (when used without parentheses).
            name: Optional custom name for the task (defaults to function name).
            retry: Retry configuration (overrides default_retry).
            timeout: Timeout in seconds (overrides default_timeout).
            plan: Resource plan (overrides default_plan).

        Returns:
            The decorated function as a TaskCallable.

        Example:
            @app.task
            def simple_task(x: int) -> int:
                return x * 2

            @app.task(timeout=60, plan="starter")
            def quick_task(x: int) -> int:
                return x + 1
        """
        # Build options from defaults and overrides
        effective_retry = retry if retry is not None else self._default_retry
        effective_timeout = timeout if timeout is not None else self._default_timeout
        effective_plan = plan if plan is not None else self._default_plan

        options = Options(
            retry=effective_retry,
            timeout_seconds=effective_timeout,
            plan=effective_plan,
        )

        # Create the task decorator bound to this app's registry
        task_decorator = create_task_decorator(self._registry)

        def decorator(f: F) -> TaskCallable:
            return task_decorator(f, name=name, options=options)

        if func is None:
            # Called with arguments: @app.task(name="...", timeout=30)
            return decorator
        # Called without arguments: @app.task
        return decorator(func)

    def start(self) -> None:
        """
        Start the workflow worker.

        Reads RENDER_SDK_MODE and RENDER_SDK_SOCKET_PATH environment variables
        to determine whether to run tasks or register them.

        Typically invoked via the render-workflows CLI:
            render-workflows myapp:app

        Raises:
            ValueError: If required environment variables are not set.
        """
        import os

        mode = os.environ.get("RENDER_SDK_MODE")
        socket_path = os.environ.get("RENDER_SDK_SOCKET_PATH")

        if not mode:
            raise ValueError("RENDER_SDK_MODE environment variable is required")

        if not socket_path:
            raise ValueError("RENDER_SDK_SOCKET_PATH environment variable is required")

        # Copy tasks to global registry for the runner to use
        from render_sdk.workflows.task import _global_registry

        for task_name in self._registry.get_task_names():
            task_info = self._registry.get_task(task_name)
            if task_info and task_name not in _global_registry._tasks:
                _global_registry._tasks[task_name] = task_info

        if mode == "run":
            run(socket_path)
        elif mode == "register":
            register(socket_path)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    @classmethod
    def from_workflows(
        cls,
        *apps: Workflows,
        default_retry: Retry | None = None,
        default_timeout: int | None = None,
        default_plan: str | None = None,
    ) -> Workflows:
        """
        Combine multiple Workflows apps into one.

        This is useful for organizing tasks across multiple modules.

        Args:
            *apps: Workflows instances to combine.
            default_retry: Default retry for new tasks on combined app.
            default_timeout: Default timeout for new tasks on combined app.
            default_plan: Default plan for new tasks on combined app.

        Returns:
            A new Workflows instance with all tasks from the input apps.

        Example:
            from tasks_a import app as app_a
            from tasks_b import app as app_b

            combined = Workflows.from_workflows(app_a, app_b)
        """
        combined = cls(
            default_retry=default_retry,
            default_timeout=default_timeout,
            default_plan=default_plan,
        )

        # Copy tasks from all apps
        for app in apps:
            for task_name in app._registry.get_task_names():
                task_info = app._registry.get_task(task_name)
                if task_info:
                    if task_name in combined._registry._tasks:
                        raise ValueError(
                            f"Task '{task_name}' is defined in multiple apps"
                        )
                    combined._registry._tasks[task_name] = task_info

        return combined
