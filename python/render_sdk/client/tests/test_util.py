import httpx
import pytest

from render_sdk.client.errors import ClientError, ServerError, TimeoutError
from render_sdk.client.util import (
    handle_api_error,
    handle_http_error,
    handle_http_errors,
    handle_httpx_exception,
    handle_storage_http_error,
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


class TestHandleStorageHttpError:
    """Tests for handle_storage_http_error function."""

    def test_404_with_s3_xml_error_does_not_expose_raw_content(self):
        """Verify that raw S3 XML error content is not exposed in error message."""
        s3_xml_error = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Error><Code>NoSuchKey</Code>"
            "<Message>The specified key does not exist.</Message>"
            "<Key>tea-d3tc3fuuk2gs73d0paug/foo/bar/test.txt</Key>"
            "<RequestId>95N55HR7H0QBF3X9</RequestId>"
            "<HostId>QfLXA55SGkqZ6VEKV97lgMjiFNWRFhpTj29FAylq2SOh2LJFMyvHuRdUjDu1IaZ"
            "/NmQR0znt4/0=</HostId></Error>"
        )

        response = httpx.Response(status_code=404, text=s3_xml_error)

        with pytest.raises(ClientError) as exc_info:
            handle_storage_http_error(response, "download object")

        error_message = str(exc_info.value)

        # Should contain sanitized message
        assert "failed with status 404" in error_message
        assert "object not found" in error_message

        # Should NOT contain sensitive/raw content
        assert "NoSuchKey" not in error_message
        assert "tea-d3tc3fuuk2gs73d0paug" not in error_message
        assert "RequestId" not in error_message
        assert "HostId" not in error_message

    def test_403_access_denied_does_not_expose_bucket_info(self):
        """Verify that storage bucket info is not exposed in error message."""
        gcs_error = (
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<Error><Code>AccessDenied</Code><Message>Access denied.</Message>"
            "<Details>render-objects-bucket/some/path</Details></Error>"
        )

        response = httpx.Response(status_code=403, text=gcs_error)

        with pytest.raises(ClientError) as exc_info:
            handle_storage_http_error(response, "upload object")

        error_message = str(exc_info.value)

        # Should contain sanitized message
        assert "failed with status 403" in error_message
        assert "access denied" in error_message

        # Should NOT contain sensitive info
        assert "render-objects-bucket" not in error_message
        assert "AccessDenied" not in error_message

    def test_500_server_error(self):
        """Verify 5xx errors raise ServerError with sanitized message."""
        response = httpx.Response(
            status_code=500,
            text="Internal Server Error: connection to storage backend failed",
        )

        with pytest.raises(ServerError) as exc_info:
            handle_storage_http_error(response, "download object")

        error_message = str(exc_info.value)

        # Should contain sanitized message
        assert "failed with status 500" in error_message
        assert "storage service temporarily unavailable" in error_message

        # Should NOT contain raw error content
        assert "Internal Server Error" not in error_message
        assert "storage backend" not in error_message

    def test_413_payload_too_large(self):
        """Verify 413 errors are handled with appropriate message."""
        xml_error = (
            '<?xml version="1.0"?><Error><Code>EntityTooLarge</Code>'
            "<MaxSizeAllowed>5368709120</MaxSizeAllowed></Error>"
        )
        response = httpx.Response(status_code=413, text=xml_error)

        with pytest.raises(ClientError) as exc_info:
            handle_storage_http_error(response, "upload object")

        error_message = str(exc_info.value)

        assert "failed with status 413" in error_message
        assert "object too large" in error_message
        assert "EntityTooLarge" not in error_message
        assert "MaxSizeAllowed" not in error_message

    def test_success_response_does_not_raise(self):
        """Verify successful responses don't raise exceptions."""
        response = httpx.Response(status_code=200, text="OK")
        # Should not raise
        handle_storage_http_error(response, "download object")
