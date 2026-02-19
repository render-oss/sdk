"""End-to-end tests for object storage."""

import contextlib
import os
import uuid

import pytest

from render_sdk.experimental.object.e2e_helpers import object_storage_crud_check
from render_sdk.render import Render

# ---------------------------------------------------------------------------
# Gating: skip entire module when credentials are missing
# (GitHub Actions sets missing secrets to empty string, so use `not get()`)
# ---------------------------------------------------------------------------
pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not os.environ.get("RENDER_API_KEY")
        or not os.environ.get("RENDER_E2E_OWNER_ID"),
        reason="RENDER_API_KEY and RENDER_E2E_OWNER_ID required for e2e tests",
    ),
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def render():
    """Construct Render client inside fixture to avoid constructor throw before skip."""
    return Render(base_url=os.environ.get("RENDER_BASE_URL", "https://api.render.com"))


@pytest.fixture
def owner_id():
    return os.environ["RENDER_E2E_OWNER_ID"]


@pytest.fixture
def region():
    return os.environ.get("RENDER_E2E_REGION", "oregon")


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------
class TestObjectClientE2E:
    @pytest.mark.asyncio
    async def test_crud_cycle(self, render, owner_id, region):
        """Full PUT → LIST → GET → DELETE → verify-deletion cycle."""
        await object_storage_crud_check(
            render.client.experimental.storage.objects,
            owner_id,
            region,
        )

    @pytest.mark.asyncio
    async def test_scoped_accessor(self, render, owner_id, region):
        """Verify scoped() wiring with a simple PUT/GET/DELETE."""
        scoped = render.client.experimental.storage.objects.scoped(
            owner_id=owner_id, region=region
        )
        key = f"e2e-test/{uuid.uuid4()}/scoped-test.txt"

        try:
            await scoped.put(key=key, data=b"scoped")
            obj = await scoped.get(key=key)
            assert obj.data == b"scoped"
            await scoped.delete(key=key)
        except Exception:
            with contextlib.suppress(Exception):
                await scoped.delete(key=key)
            raise


# ---------------------------------------------------------------------------
# Pagination tests (pre-seeded org)
# ---------------------------------------------------------------------------
@pytest.mark.skipif(
    not os.environ.get("RENDER_E2E_PAGINATION_OWNER_ID"),
    reason="RENDER_E2E_PAGINATION_OWNER_ID required for pagination tests",
)
class TestObjectClientPagination:
    @pytest.mark.asyncio
    async def test_pagination(self, render):
        """Walk all pages with limit=2, verify multiple pages returned."""
        owner_id = os.environ["RENDER_E2E_PAGINATION_OWNER_ID"]
        region = os.environ.get("RENDER_E2E_REGION", "oregon")
        objects = render.client.experimental.storage.objects

        page_size = 2
        cursor = None
        total_objects = 0
        pages = 0

        while True:
            response = await objects.list(
                owner_id=owner_id,
                region=region,
                limit=page_size,
                cursor=cursor,
            )

            assert len(response.objects) > 0
            total_objects += len(response.objects)
            pages += 1

            if not response.has_next:
                break
            cursor = response.next_cursor

        # Pre-seeded org should have enough objects to require multiple pages
        assert total_objects > page_size
        assert pages > 1
