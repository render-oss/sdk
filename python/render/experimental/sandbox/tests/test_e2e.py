"""End-to-end test for the sandbox client.

Creates a real sandbox, runs commands through exec (token mint plus proxy
stream), verifies the streamed output and exit codes, and always terminates the
sandbox. Gated on real credentials, so it is skipped by default.

Run with:
    uv run pytest render/experimental/sandbox/tests/test_e2e.py -m e2e -v

CI runs this against staging as `test+sdk-e2e@test.render.com`, in its own
`Python Sandbox E2E Tests` job so it reports separately from the rest of the e2e
set. The API key is in shared 1Password. Staging sandboxes now reach `running`,
so these cases exercise the real token mint, proxy stream and file transfer.
"""

from __future__ import annotations

import asyncio
import os
import time

import pytest

from render.experimental.sandbox import (
    SandboxExecExit,
    SandboxExecOutput,
    SandboxFileNotFoundError,
)
from render.render_async import RenderAsync

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


async def _exec_output(sandboxes, sandbox_id, owner_id, command):
    """Run command and return its stdout, asserting a zero exit."""
    outputs = []
    exit_event = None
    async for event in sandboxes.exec(sandbox_id, command, owner_id=owner_id):
        if isinstance(event, SandboxExecOutput):
            if event.stream == "stdout":
                outputs.append(event.data)
        elif isinstance(event, SandboxExecExit):
            exit_event = event
    assert exit_event is not None
    assert exit_event.exit_code == 0, f"{command!r} exited {exit_event.exit_code}"
    return "".join(outputs)


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

        filtered = await sandboxes.list(
            owner_id=owner_id, status=["running", "creating"], limit=100
        )
        assert any(s.id == sandbox.id for s in filtered.sandboxes)
        assert all(s.status in {"running", "creating"} for s in filtered.sandboxes)

        excluded = await sandboxes.list(
            owner_id=owner_id, status=["suspended"], limit=100
        )
        assert all(s.id != sandbox.id for s in excluded.sandboxes)
        assert all(s.status == "suspended" for s in excluded.sandboxes)

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


@pytest.mark.asyncio
async def test_copy_from_file_and_directory(sandboxes, tmp_path):
    owner_id = _OWNER_ID

    sandbox = await sandboxes.create(owner_id=owner_id)
    try:
        await _wait_until_running(sandboxes, sandbox.id, owner_id)

        # build a tree inside the sandbox to pull back out
        await _exec_output(
            sandboxes,
            sandbox.id,
            owner_id,
            'cd "$HOME" && mkdir -p copy-from-tree/nested '
            '&& printf "hello from copy_from\\n" > copy-from-greeting.txt '
            '&& printf "nested file\\n" > copy-from-tree/nested/data.txt '
            "&& ln -sf nested/data.txt copy-from-tree/link.txt",
        )

        # a single file lands at exactly the path asked for
        target = tmp_path / "greeting.txt"
        written = await sandboxes.copy_from(
            sandbox.id, "copy-from-greeting.txt", target, owner_id=owner_id
        )
        assert written == str(target)
        assert target.read_text() == "hello from copy_from\n"

        # into an existing directory, the name comes from the sandbox
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        written = await sandboxes.copy_from(
            sandbox.id, "copy-from-greeting.txt", inbox, owner_id=owner_id
        )
        assert written == str(inbox / "copy-from-greeting.txt")
        assert (
            inbox / "copy-from-greeting.txt"
        ).read_text() == "hello from copy_from\n"

        # a directory arrives as an x-tar archive under Content-Encoding: gzip
        # and is extracted under local_path, symlink stored rather than followed
        tree = tmp_path / "tree"
        written = await sandboxes.copy_from(
            sandbox.id, "copy-from-tree", tree, owner_id=owner_id
        )
        assert written == str(tree)
        assert (tree / "nested" / "data.txt").read_text() == "nested file\n"
        assert os.readlink(tree / "link.txt") == "nested/data.txt"

        # a path the sandbox does not have is a missing file, not a missing
        # sandbox: the agent says so with a file_not_found code in the body
        with pytest.raises(SandboxFileNotFoundError):
            await sandboxes.copy_from(
                sandbox.id,
                "no-such-file.txt",
                tmp_path / "nope.txt",
                owner_id=owner_id,
            )
    finally:
        await sandboxes.terminate(sandbox.id, owner_id=owner_id)


@pytest.mark.asyncio
async def test_copy_to_file_and_directory(sandboxes, tmp_path):
    owner_id = _OWNER_ID

    (tmp_path / "greeting.txt").write_text("hello from copy_to\n")
    tree = tmp_path / "tree"
    (tree / "nested").mkdir(parents=True)
    (tree / "nested" / "data.txt").write_text("nested file\n")
    (tree / "link.txt").symlink_to("nested/data.txt")

    sandbox = await sandboxes.create(owner_id=owner_id)
    try:
        await _wait_until_running(sandboxes, sandbox.id, owner_id)

        # a single file arrives as raw bytes. A relative remote path resolves
        # under the sandbox's home directory, scp style.
        await sandboxes.copy_to(
            sandbox.id,
            tmp_path / "greeting.txt",
            "copy-to-greeting.txt",
            owner_id=owner_id,
        )
        contents = await _exec_output(
            sandboxes, sandbox.id, owner_id, 'cat "$HOME/copy-to-greeting.txt"'
        )
        assert contents == "hello from copy_to\n"

        # a directory arrives as an archive the sandbox extracts, with entry
        # names relative to the local root
        await sandboxes.copy_to(sandbox.id, tree, "copy-to-tree", owner_id=owner_id)
        listing = await _exec_output(
            sandboxes,
            sandbox.id,
            owner_id,
            'cd "$HOME" && find copy-to-tree -mindepth 1 | sort',
        )
        assert listing.split() == [
            "copy-to-tree/link.txt",
            "copy-to-tree/nested",
            "copy-to-tree/nested/data.txt",
        ]

        # the symlink was stored, not followed into a second copy of the file
        target = await _exec_output(
            sandboxes, sandbox.id, owner_id, 'readlink "$HOME/copy-to-tree/link.txt"'
        )
        assert target.strip() == "nested/data.txt"
    finally:
        await sandboxes.terminate(sandbox.id, owner_id=owner_id)
