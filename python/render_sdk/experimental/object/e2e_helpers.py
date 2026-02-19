"""Standalone CRUD check for object storage.

No pytest dependency — reusable by pollinators / health probes.
"""

import asyncio
import contextlib
import uuid

from render_sdk.client.errors import RenderError
from render_sdk.experimental.object.client import ObjectClient

RETRY_ATTEMPTS = 5
RETRY_INTERVAL_S = 1.0


async def object_storage_crud_check(
    client: ObjectClient, owner_id: str, region: str
) -> str:
    """Run a full PUT → LIST → GET → DELETE → verify-deletion cycle.

    Returns the key that was used (caller can use it for follow-up assertions).
    """
    key = f"e2e-test/{uuid.uuid4()}/crud-test.txt"
    content = b"hello from e2e"

    try:
        # --- PUT ---
        await client.put(
            owner_id=owner_id,
            region=region,
            key=key,
            data=content,
        )

        # --- LIST (with retry — eventual consistency) ---
        found = False
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            list_response = await client.list(owner_id=owner_id, region=region)
            match = next((o for o in list_response.objects if o.key == key), None)
            if match is not None:
                if match.size != len(content):
                    raise AssertionError(
                        f"LIST size mismatch: expected {len(content)}, got {match.size}"
                    )
                found = True
                break
            if attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(RETRY_INTERVAL_S)

        if not found:
            raise AssertionError(
                f"Object {key} not found in LIST after {RETRY_ATTEMPTS} attempts"
            )

        # --- GET ---
        obj = await client.get(owner_id=owner_id, region=region, key=key)
        if obj.data != content:
            raise AssertionError("GET data does not match uploaded content")
        if obj.size != len(content):
            raise AssertionError(
                f"GET size mismatch: expected {len(content)}, got {obj.size}"
            )
        # --- DELETE ---
        await client.delete(owner_id=owner_id, region=region, key=key)

        # --- Verify deletion ---
        try:
            await client.get(owner_id=owner_id, region=region, key=key)
            raise AssertionError("GET after DELETE should have raised")
        except RenderError:
            pass  # Expected — object was deleted

        return key
    except Exception:
        with contextlib.suppress(Exception):
            await client.delete(owner_id=owner_id, region=region, key=key)
        raise
