import pytest
from render.client.util import poll_fn
from typing import Tuple
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_poll_fn_success():
    async def fn() -> Tuple[int, bool]:
        return 1, True

    result = await poll_fn(fn)
    assert result == 1

@pytest.mark.asyncio
async def test_poll_fn_failure_then_success(mocker):
    """Test that poll_fn returns the correct result after a failure."""

    # patch time.sleep to return immediately
    mock_sleep = mocker.AsyncMock()
    mocker.patch("asyncio.sleep", mock_sleep)
    count = 0
    async def fn() -> Tuple[int, bool]:
        nonlocal count
        count += 1
        if count == 1:
            return 1, False
        else:
            return 1, True

    result = await poll_fn(fn)
    assert result == 1
    assert count == 2
