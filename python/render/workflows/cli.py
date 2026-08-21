"""CLI entrypoint for running Render Workflows.

Usage:
    render-workflows myapp:app
    render-workflows myapp.tasks:app

Provides explicit control over when and how the worker starts.
"""

from __future__ import annotations

import importlib
import sys


def main() -> None:
    """Main CLI entrypoint."""
    # Ensure the current working directory is on sys.path so that
    # `render-workflows <module>:<app>` can find modules in the cwd.
    if "" not in sys.path:
        sys.path.insert(0, "")

    if len(sys.argv) < 2:
        print("Usage: render-workflows <module:app>", file=sys.stderr)
        print("Example: render-workflows myapp:app", file=sys.stderr)
        sys.exit(1)

    app_path = sys.argv[1]

    if ":" not in app_path:
        print(f"Error: Invalid app path '{app_path}'", file=sys.stderr)
        print("Expected format: <module>:<app_variable>", file=sys.stderr)
        print("Example: render-workflows myapp:app", file=sys.stderr)
        sys.exit(1)

    module_path, app_name = app_path.rsplit(":", 1)

    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        print(f"Error: Could not import module '{module_path}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        app = getattr(module, app_name)
    except AttributeError:
        print(
            f"Error: Module '{module_path}' has no attribute '{app_name}'",
            file=sys.stderr,
        )
        sys.exit(1)

    if not hasattr(app, "start"):
        print(f"Error: '{app_name}' does not have a start() method", file=sys.stderr)
        print("Expected a Workflows instance", file=sys.stderr)
        sys.exit(1)

    app.start()


if __name__ == "__main__":
    main()
