"""End-to-end test for the sandbox client.

Creates a real sandbox, runs commands through exec (token mint plus proxy
stream), verifies the streamed output and exit codes, and always terminates the
sandbox. Gated on real credentials, so it is skipped by default.

Run with:
    uv run pytest render_sdk/experimental/sandbox/tests/test_e2e.py -m e2e -v

CI runs this against staging as `test+sdk-e2e@test.render.com`, in its own
`Python Sandbox E2E Tests` job so it reports separately from the rest of the e2e
set. The API key is in shared 1Password. It is expected to fail until a sandbox
runner (renderd) fleet is available, since the sandbox never leaves `creating`.
"""

from __future__ import annotations

import asyncio
import os
import time

import pytest

from render_sdk.experimental.sandbox import SandboxExecExit, SandboxExecOutput
from render_sdk.render_async import RenderAsync

_OWNER_ID = os.environ.get("RENDER_E2E_OWNER_ID") or os.environ.get(
    "RENDER_WORKSPACE_ID"
)

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.sandbox_e2e,
    pytest.mark.skipif(
        not os.environ.get("RENDER_API_KEY") or not _OWNER_ID,
        reason=(
            "RENDER_API_KEY and RENDER_E2E_OWNER_ID (or RENDER_WORKSPACE_ID) "
            "required for sandbox e2e tests"
        ),
    ),
]


@pytest.fixture
def sandboxes():
    render = RenderAsync(
        base_url=os.environ.get("RENDER_BASE_URL") or "https://api.render.com"
    )
    return render.experimental.sandboxes


async def _wait_until_running(sandboxes, sandbox_id, owner_id, timeout_s=180.0):
    """Poll from_id until the sandbox is running, or fail on timeout/error."""
    deadline = time.monotonic() + timeout_s
    while True:
        sandbox = await sandboxes.from_id(sandbox_id, owner_id=owner_id)
        if sandbox.status == "running":
            return sandbox
        if sandbox.status in ("errored", "terminated"):
            raise AssertionError(
                f"sandbox {sandbox_id} reached terminal status {sandbox.status!r}"
            )
        if time.monotonic() > deadline:
            raise AssertionError(
                f"sandbox {sandbox_id} still {sandbox.status!r} after {timeout_s}s"
            )
        await asyncio.sleep(3.0)


@pytest.mark.asyncio
async def test_create_exec_terminate(sandboxes):
    owner_id = _OWNER_ID

    sandbox = await sandboxes.create(owner_id=owner_id)
    assert sandbox.id.startswith("sbx-")
    try:
        await _wait_until_running(sandboxes, sandbox.id, owner_id)

        # from_id round-trips the same sandbox
        fetched = await sandboxes.from_id(sandbox.id, owner_id=owner_id)
        assert fetched.id == sandbox.id

        # list includes the new sandbox
        page = await sandboxes.list(owner_id=owner_id)
        assert any(s.id == sandbox.id for s in page.sandboxes)

        # exec streams stdout and reports a zero exit
        outputs = []
        exit_event = None
        async for event in sandboxes.exec(
            sandbox.id, "echo hello-from-e2e", owner_id=owner_id
        ):
            if isinstance(event, SandboxExecOutput):
                outputs.append(event.data)
            elif isinstance(event, SandboxExecExit):
                exit_event = event
        assert "hello-from-e2e" in "".join(outputs)
        assert exit_event is not None
        assert exit_event.exit_code == 0

        # a non-zero process exit is reported via the exit event, not an error
        exit_event = None
        async for event in sandboxes.exec(sandbox.id, "exit 3", owner_id=owner_id):
            if isinstance(event, SandboxExecExit):
                exit_event = event
        assert exit_event is not None
        assert exit_event.exit_code == 3
    finally:
        await sandboxes.terminate(sandbox.id, owner_id=owner_id)
