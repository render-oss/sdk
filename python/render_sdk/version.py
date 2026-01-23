"""Version information for the Render SDK."""

import importlib.metadata
import platform


def get_version() -> str:
    """Get the SDK version from package metadata."""
    try:
        return importlib.metadata.version("render_sdk")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def get_user_agent() -> str:
    """Get the User-Agent string for the SDK.

    Returns a string like:
        render-sdk-python/0.1.3 (cpython/3.11.4; darwin/arm64)
    """
    version = get_version()
    impl = platform.python_implementation().lower()
    py_version = platform.python_version()
    os_name = platform.system().lower()
    arch = platform.machine().lower()

    return f"render-sdk-python/{version} ({impl}/{py_version}; {os_name}/{arch})"
