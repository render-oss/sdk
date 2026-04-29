"""Shared utilities for the Key Value module."""


def _format_error_message(failure: str, call_to_action: str) -> str:
    return f"{failure}\n\n{call_to_action}"
