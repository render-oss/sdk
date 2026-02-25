#!/usr/bin/env python3
"""Unit tests for synchronous utility functions."""

import pytest

from render_sdk.client.errors import ClientError
from render_sdk.client.util_sync import handle_http_errors, retry_with_backoff
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.types import Response


class _TestException(Exception):
    pass


def test_retry_with_backoff_success():
    def fn() -> int:
        return 1

    result = retry_with_backoff(fn)
    assert result == 1


def test_retry_with_backoff_failure():
    def fn() -> int:
        raise _TestException("Test failure")

    with pytest.raises(_TestException):
        retry_with_backoff(fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0)


def test_retry_with_backoff_success_after_failure():
    count = 0

    def fn() -> int:
        nonlocal count
        count += 1
        if count == 1:
            raise _TestException("Test failure")
        return 1

    result = retry_with_backoff(
        fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0
    )
    assert result == 1


def test_retry_with_backoff_exempted_exception():
    count = 0

    def fn() -> int:
        nonlocal count
        count += 1
        raise _TestException("Test failure")

    with pytest.raises(_TestException):
        retry_with_backoff(
            fn,
            max_retries=5,
            poll_interval=0.001,
            backoff_factor=1.0,
            exempted_exceptions=(_TestException,),
        )

    # Should have raised on the first attempt without retrying
    assert count == 1


def test_retry_with_backoff_returns_none_when_all_none():
    def fn():
        return None

    result = retry_with_backoff(
        fn, max_retries=3, poll_interval=0.001, backoff_factor=1.0
    )
    assert result is None


def test_decorator_handle_http_errors():
    @handle_http_errors("test operation")
    def test_operation():
        return Response(
            status_code=400,
            content=b"",
            headers={},
            parsed=Error(message="Bad request"),
        )

    with pytest.raises(ClientError, match="test operation failed: Bad request"):
        test_operation()


def test_decorator_handle_http_errors_success():
    @handle_http_errors("test operation")
    def test_operation():
        return Response(
            status_code=200,
            content=b"",
            headers={},
            parsed={"data": "ok"},
        )

    result = test_operation()
    assert result.status_code == 200
