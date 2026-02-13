"""Tests for the Workflows application class."""

import pytest

from render_sdk.workflows.app import Workflows
from render_sdk.workflows.task import Retry


class TestFromWorkflows:
    """Tests for Workflows.from_workflows() composition."""

    def test_combines_tasks_from_multiple_apps(self):
        """Test that from_workflows combines tasks from multiple apps."""
        app_a = Workflows()
        app_b = Workflows()

        @app_a.task
        def task_a(x: int) -> int:
            return x + 1

        @app_b.task
        def task_b(x: int) -> int:
            return x + 2

        combined = Workflows.from_workflows(app_a, app_b)

        # Verify both tasks are in the combined app
        task_names = combined._registry.get_task_names()
        assert "task_a" in task_names
        assert "task_b" in task_names
        assert len(task_names) == 2

    def test_raises_on_duplicate_task_names(self):
        """Test that from_workflows raises ValueError on duplicate task names."""
        app_a = Workflows()
        app_b = Workflows()

        @app_a.task
        def duplicate_task(x: int) -> int:
            return x + 1

        @app_b.task
        def duplicate_task(x: int) -> int:  # noqa: F811
            return x + 2

        with pytest.raises(
            ValueError, match="Task 'duplicate_task' is defined in multiple apps"
        ):
            Workflows.from_workflows(app_a, app_b)

    def test_combined_app_uses_its_own_defaults(self):
        """Test that the combined app uses its own defaults, not source app defaults."""
        source_retry = Retry(max_retries=5, wait_duration_ms=500, backoff_scaling=1.0)
        app_a = Workflows(default_retry=source_retry, default_timeout=100)

        @app_a.task
        def task_a(x: int) -> int:
            return x

        # Combined app has different defaults
        combined_retry = Retry(
            max_retries=10, wait_duration_ms=1000, backoff_scaling=2.0
        )
        combined = Workflows.from_workflows(
            app_a,
            default_retry=combined_retry,
            default_timeout=300,
            default_plan="premium",
        )

        # Verify the combined app stored its own defaults
        assert combined._default_retry == combined_retry
        assert combined._default_timeout == 300
        assert combined._default_plan == "premium"

    def test_combined_app_can_define_new_tasks(self):
        """Test that new tasks can be added to the combined app."""
        app_a = Workflows()

        @app_a.task
        def task_a(x: int) -> int:
            return x

        combined = Workflows.from_workflows(app_a)

        @combined.task
        def task_b(x: int) -> int:
            return x * 2

        task_names = combined._registry.get_task_names()
        assert "task_a" in task_names
        assert "task_b" in task_names
        assert len(task_names) == 2

    def test_works_with_zero_apps(self):
        """Test that from_workflows works with no input apps."""
        combined = Workflows.from_workflows()

        assert combined._registry.get_task_names() == []

    def test_works_with_single_app(self):
        """Test that from_workflows works with a single app."""
        app = Workflows()

        @app.task
        def my_task(x: int) -> int:
            return x

        combined = Workflows.from_workflows(app)

        assert "my_task" in combined._registry.get_task_names()
        assert len(combined._registry.get_task_names()) == 1

    def test_preserves_task_options(self):
        """Test that task options are preserved when combining apps."""
        retry = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0)
        app = Workflows()

        @app.task(retry=retry, timeout=60, plan="starter")
        def configured_task(x: int) -> int:
            return x

        combined = Workflows.from_workflows(app)

        task_info = combined._registry.get_task("configured_task")
        assert task_info is not None
        assert task_info.options.retry.max_retries == 3
        assert task_info.options.timeout_seconds == 60
        assert task_info.options.plan == "starter"

    def test_combines_three_or_more_apps(self):
        """Test that from_workflows works with many apps."""
        app1 = Workflows()
        app2 = Workflows()
        app3 = Workflows()

        @app1.task
        def task_1(x: int) -> int:
            return x + 1

        @app2.task
        def task_2(x: int) -> int:
            return x + 2

        @app3.task
        def task_3(x: int) -> int:
            return x + 3

        combined = Workflows.from_workflows(app1, app2, app3)

        task_names = combined._registry.get_task_names()
        assert len(task_names) == 3
        assert "task_1" in task_names
        assert "task_2" in task_names
        assert "task_3" in task_names


class TestWorkflowsInit:
    """Tests for Workflows initialization."""

    def test_stores_default_retry(self):
        """Test that default_retry is stored correctly."""
        retry = Retry(max_retries=5, wait_duration_ms=1000, backoff_scaling=2.0)
        app = Workflows(default_retry=retry)

        assert app._default_retry == retry

    def test_stores_default_timeout(self):
        """Test that default_timeout is stored correctly."""
        app = Workflows(default_timeout=300)

        assert app._default_timeout == 300

    def test_stores_default_plan(self):
        """Test that default_plan is stored correctly."""
        app = Workflows(default_plan="premium")

        assert app._default_plan == "premium"


class TestWorkflowsTaskDecorator:
    """Tests for the @app.task decorator."""

    def test_task_uses_app_defaults(self):
        """Test that tasks use app-level defaults when not overridden."""
        retry = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0)
        app = Workflows(
            default_retry=retry,
            default_timeout=120,
            default_plan="standard",
        )

        @app.task
        def my_task(x: int) -> int:
            return x

        task_info = app._registry.get_task("my_task")
        assert task_info.options.retry == retry
        assert task_info.options.timeout_seconds == 120
        assert task_info.options.plan == "standard"

    def test_task_overrides_app_defaults(self):
        """Test that task-level options override app defaults."""
        app_retry = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0)
        task_retry = Retry(max_retries=10, wait_duration_ms=5000, backoff_scaling=3.0)

        app = Workflows(
            default_retry=app_retry,
            default_timeout=120,
            default_plan="standard",
        )

        @app.task(retry=task_retry, timeout=60, plan="starter")
        def my_task(x: int) -> int:
            return x

        task_info = app._registry.get_task("my_task")
        assert task_info.options.retry == task_retry
        assert task_info.options.timeout_seconds == 60
        assert task_info.options.plan == "starter"

    def test_task_partial_override(self):
        """Test that tasks can partially override app defaults."""
        app_retry = Retry(max_retries=3, wait_duration_ms=1000, backoff_scaling=2.0)

        app = Workflows(
            default_retry=app_retry,
            default_timeout=120,
            default_plan="standard",
        )

        # Only override timeout, keep retry and plan from defaults
        @app.task(timeout=60)
        def my_task(x: int) -> int:
            return x

        task_info = app._registry.get_task("my_task")
        assert task_info.options.retry == app_retry  # From app default
        assert task_info.options.timeout_seconds == 60  # Overridden
        assert task_info.options.plan == "standard"  # From app default

    def test_task_with_custom_name(self):
        """Test that tasks can have custom names."""
        app = Workflows()

        @app.task(name="custom_task_name")
        def my_function(x: int) -> int:
            return x

        task_names = app._registry.get_task_names()
        assert "custom_task_name" in task_names
        assert "my_function" not in task_names

    def test_task_decorator_without_parentheses(self):
        """Test that @app.task works without parentheses."""
        app = Workflows()

        @app.task
        def my_task(x: int) -> int:
            return x

        assert "my_task" in app._registry.get_task_names()

    def test_task_decorator_with_empty_parentheses(self):
        """Test that @app.task() works with empty parentheses."""
        app = Workflows()

        @app.task()
        def my_task(x: int) -> int:
            return x

        assert "my_task" in app._registry.get_task_names()


class TestWorkflowsStart:
    """Tests for Workflows.start() method."""

    def test_raises_when_mode_not_set(self, monkeypatch):
        """Test that start() raises ValueError when RENDER_SDK_MODE is not set."""
        monkeypatch.delenv("RENDER_SDK_MODE", raising=False)
        monkeypatch.delenv("RENDER_SDK_SOCKET_PATH", raising=False)

        app = Workflows()

        with pytest.raises(
            ValueError, match="RENDER_SDK_MODE environment variable is required"
        ):
            app.start()

    def test_raises_when_socket_path_not_set(self, monkeypatch):
        """
        Test that start() raises ValueError when RENDER_SDK_SOCKET_PATH is not set.
        """
        monkeypatch.setenv("RENDER_SDK_MODE", "run")
        monkeypatch.delenv("RENDER_SDK_SOCKET_PATH", raising=False)

        app = Workflows()

        with pytest.raises(
            ValueError, match="RENDER_SDK_SOCKET_PATH environment variable is required"
        ):
            app.start()

    def test_raises_for_unknown_mode(self, monkeypatch):
        """Test that start() raises ValueError for unknown mode."""
        monkeypatch.setenv("RENDER_SDK_MODE", "invalid_mode")
        monkeypatch.setenv("RENDER_SDK_SOCKET_PATH", "/tmp/test.sock")  # noqa: S108

        app = Workflows()

        with pytest.raises(ValueError, match="Unknown mode: invalid_mode"):
            app.start()

    def test_copies_tasks_to_global_registry(self, monkeypatch):
        """Test that start() copies tasks to the global registry."""
        monkeypatch.setenv("RENDER_SDK_MODE", "register")
        monkeypatch.setenv("RENDER_SDK_SOCKET_PATH", "/tmp/test.sock")  # noqa: S108

        from render_sdk.workflows.task import _global_registry

        # Clear global registry
        _global_registry._tasks.clear()

        app = Workflows()

        @app.task
        def my_task(x: int) -> int:
            return x

        # Mock the register function to avoid actual socket operations
        import render_sdk.workflows.app as app_module

        original_register = app_module.register
        app_module.register = lambda _: None

        try:
            app.start()

            # Task should be in global registry
            assert "my_task" in _global_registry._tasks
        finally:
            app_module.register = original_register
            _global_registry._tasks.clear()
