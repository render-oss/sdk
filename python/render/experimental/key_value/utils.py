"""Shared utilities for the Key Value module."""

import os


def _format_error_message(failure: str, call_to_action: str) -> str:
    return f"{failure}\n\n{call_to_action}"


def _is_local_dev() -> bool:
    return os.environ.get("RENDER_USE_LOCAL_DEV") == "true"
