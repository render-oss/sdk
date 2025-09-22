import pytest

from render.client.util import retry_with_backoff

@pytest.mark.asyncio
async def test_retry_with_backoff_success():
    async def fn() -> int:
        return 1

    result = await retry_with_backoff(fn)
    assert result == 1


@pytest.mark.asyncio
async def test_retry_with_backoff_failure():
    async def fn() -> int:
        raise Exception("Test failure")

    with pytest.raises(Exception):
      result = await retry_with_backoff(fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0)
      assert result == None


@pytest.mark.asyncio
async def test_retry_with_backoff_success_after_failure():
    count = 0
    async def fn() -> int:
        nonlocal count
        count += 1
        if count == 1:
            raise Exception("Test failure")
        else:
            return 1

    result = await retry_with_backoff(fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0)
    assert result == 1


@pytest.mark.asyncio
async def test_retry_with_backoff_success_after_failure_with_exempted_exception():
    class ExemptedException(Exception):
        pass

    count = 0
    async def fn() -> int:
        nonlocal count
        count += 1
        raise ExemptedException("Test failure")

    with pytest.raises(ExemptedException):
        result = await retry_with_backoff(fn, max_retries=2, poll_interval=0.001, backoff_factor=1.0, exempted_exceptions=(ExemptedException,))
        assert result == None
        assert count == 1
