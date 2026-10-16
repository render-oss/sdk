"""Tests for the e2e rate-limit retry wrapper."""

from types import SimpleNamespace

import pytest

from render.client.errors import ClientError, RateLimitError
from render.experimental.object.client import ObjectClient
from render.experimental.object.tests.rate_limit import (
    MAX_ATTEMPTS,
    patch_rate_limit_retries,
    retry_rate_limited,
)
from render.experimental.object.types import ListObjectsResponse


@pytest.mark.asyncio
async def test_retries_rate_limit_until_success():
    calls = 0

    async def fn() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RateLimitError("list objects failed: rate limit exceeded")
        return "ok"

    assert await retry_rate_limited(fn, initial_delay_s=0)() == "ok"
    assert calls == 3


@pytest.mark.asyncio
async def test_reraises_after_max_attempts():
    calls = 0

    async def fn() -> None:
        nonlocal calls
        calls += 1
        raise RateLimitError("rate limit exceeded")

    with pytest.raises(RateLimitError):
        await retry_rate_limited(fn, initial_delay_s=0)()
    assert calls == MAX_ATTEMPTS


@pytest.mark.asyncio
async def test_does_not_retry_other_client_errors():
    calls = 0

    async def fn() -> None:
        nonlocal calls
        calls += 1
        raise ClientError("object not found")

    with pytest.raises(ClientError):
        await retry_rate_limited(fn, initial_delay_s=0)()
    assert calls == 1


@pytest.mark.asyncio
async def test_patch_covers_scoped_client(mocker):
    client = ObjectClient(SimpleNamespace())
    list_mock = mocker.AsyncMock(
        side_effect=[
            RateLimitError("rate limit exceeded"),
            ListObjectsResponse(objects=[], next_cursor=None, has_next=False),
        ]
    )
    mocker.patch.object(client, "list", new=list_mock)

    patch_rate_limit_retries(client, initial_delay_s=0)
    response = await client.scoped(owner_id="tea-test", region="oregon").list()

    assert response.objects == []
    assert list_mock.await_count == 2
