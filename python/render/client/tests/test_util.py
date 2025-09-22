import pytest

from render.client.util import retry_with_backoff


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
