"""Tests for the CLI entrypoint module."""

import pytest

from render_sdk.workflows import cli


class TestCLIMain:
    """Tests for the main() CLI entrypoint."""

    def test_no_arguments_shows_usage_and_exits(self, mocker, capsys):
        """Test that running with no arguments shows usage and exits with code 1."""
        mocker.patch("sys.argv", ["render-workflows"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage: render-workflows <module:app>" in captured.err
        assert "Example: render-workflows myapp:app" in captured.err

    def test_invalid_format_no_colon_shows_error(self, mocker, capsys):
        """Test that an argument without a colon shows an error."""
        mocker.patch("sys.argv", ["render-workflows", "myapp"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid app path 'myapp'" in captured.err
        assert "Expected format: <module>:<app_variable>" in captured.err

    def test_module_not_found_shows_error(self, mocker, capsys):
        """Test that a non-existent module shows an import error."""
        mocker.patch("sys.argv", ["render-workflows", "nonexistent_module:app"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Could not import module 'nonexistent_module'" in captured.err

    def test_attribute_not_found_shows_error(self, mocker, capsys):
        """Test that a missing attribute shows an error."""
        mocker.patch("sys.argv", ["render-workflows", "os:nonexistent_attr"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Module 'os' has no attribute 'nonexistent_attr'" in captured.err

    def test_object_without_start_method_shows_error(self, mocker, capsys):
        """Test that an object without a start() method shows an error."""
        # os.path is a module, not a Workflows instance
        mocker.patch("sys.argv", ["render-workflows", "os:path"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: 'path' does not have a start() method" in captured.err
        assert "Expected a Workflows instance" in captured.err

    def test_valid_app_calls_start(self, mocker):
        """Test that a valid app path calls the app's start() method."""
        # Create a mock app with a start method
        mock_app = mocker.Mock()
        mock_app.start = mocker.Mock()

        # Create a mock module containing the app
        mock_module = mocker.Mock()
        mock_module.app = mock_app

        # Patch sys.argv and importlib
        mocker.patch("sys.argv", ["render-workflows", "mymodule:app"])
        mocker.patch("importlib.import_module", return_value=mock_module)

        # Should not raise
        cli.main()

        # Verify start() was called
        mock_app.start.assert_called_once()

    def test_nested_module_path(self, mocker):
        """Test that nested module paths (e.g., 'myproject.tasks:app') work."""
        mock_app = mocker.Mock()
        mock_app.start = mocker.Mock()

        mock_module = mocker.Mock()
        mock_module.app = mock_app

        mocker.patch("sys.argv", ["render-workflows", "myproject.tasks.workers:app"])
        mock_import = mocker.patch("importlib.import_module", return_value=mock_module)

        cli.main()

        # Verify the full module path was used
        mock_import.assert_called_once_with("myproject.tasks.workers")
        mock_app.start.assert_called_once()

    def test_colon_in_module_path_uses_last_colon(self, mocker, capsys):
        """Test that multiple colons use rsplit to get the last segment."""
        # This is an edge case: "weird:module:app" should split as
        # module="weird:module", app="app"
        mocker.patch("sys.argv", ["render-workflows", "weird:module:app"])

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        # Should fail on import (module "weird:module" doesn't exist)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Could not import module 'weird:module'" in captured.err

    def test_import_error_includes_original_message(self, mocker, capsys):
        """Test that import errors include the original exception message."""
        mocker.patch("sys.argv", ["render-workflows", "mymodule:app"])
        mocker.patch(
            "importlib.import_module",
            side_effect=ImportError("No module named 'dependency'"),
        )

        with pytest.raises(SystemExit) as exc_info:
            cli.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No module named 'dependency'" in captured.err
