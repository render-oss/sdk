import httpx
import pytest

from render_sdk.client.errors import ClientError, ServerError, TimeoutError
from render_sdk.client.util import (
    handle_api_error,
    handle_http_error,
    handle_http_errors,
    handle_httpx_exception,
    retry_with_backoff,
)
from render_sdk.public_api.models.error import Error
from render_sdk.public_api.types import Response


class TestException(Exception):
    pass


@pytest.mark.asyncio
async def test_retry_with_backoff_success():
    async def fn() -> int:
        return 1

    result = await retry_with_backoff(fn)
    assert result == 1


@pytest.mark.asyncio
async def test_retry_with_backoff_failure():
    async def fn() -> int:
        raise TestException("Test failure")

    with pytest.raises(TestException):
        result = await retry_with_backoff(
            fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0
        )
        assert result is None


@pytest.mark.asyncio
async def test_retry_with_backoff_success_after_failure():
    count = 0

    async def fn() -> int:
        nonlocal count
        count += 1
        if count == 1:
            raise TestException("Test failure")
        else:
            return 1

    result = await retry_with_backoff(
        fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0
    )
    assert result == 1


@pytest.mark.asyncio
async def test_retry_with_backoff_success_after_failure_with_exempted_exception():
    count = 0

    async def fn() -> int:
        nonlocal count
        count += 1
        raise TestException("Test failure")

    with pytest.raises(TestException):
        result = await retry_with_backoff(
            fn,
            max_retries=2,
            poll_interval=0.001,
            backoff_factor=1.0,
            exempted_exceptions=(TestException,),
        )
        assert result is None
        assert count == 1


def test_handle_http_error_4xx():
    response = httpx.Response(
        status_code=404, json={"message": "Not found"}, text="Not found"
    )
    with pytest.raises(
        ClientError, match="API request failed with status 404: Not found"
    ):
        handle_http_error(response, "API request")


def test_handle_http_error_5xx():
    response = httpx.Response(
        status_code=500,
        json={"error": "Internal server error"},
        text="Internal server error",
    )
    with pytest.raises(
        ServerError, match="API request failed with status 500: Internal server error"
    ):
        handle_http_error(response, "API request")


def test_handle_httpx_exception_timeout():
    exception = httpx.TimeoutException("Request timed out")
    with pytest.raises(TimeoutError, match="HTTP request timed out"):
        handle_httpx_exception(exception, "HTTP request")


def test_handle_api_error_client_error():
    response = Response(
        status_code=400, content=b"", headers={}, parsed=Error(message="Bad request")
    )
    with pytest.raises(ClientError, match="API request failed: Bad request"):
        handle_api_error(response, "API request")


def test_handle_api_error_server_error():
    response = Response(
        status_code=500,
        content=b"",
        headers={},
        parsed=Error(message="Internal server error"),
    )
    with pytest.raises(ServerError, match="API request failed: Internal server error"):
        handle_api_error(response, "API request")


@pytest.mark.asyncio
async def test_decorator_handle_http_errors():
    @handle_http_errors("test operation")
    async def test_operation():
        return Response(
            status_code=400,
            content=b"",
            headers={},
            parsed=Error(message="Bad request"),
        )

    with pytest.raises(ClientError, match="test operation failed: Bad request"):
        await test_operation()
