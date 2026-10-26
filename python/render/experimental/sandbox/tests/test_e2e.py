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
from uuid import uuid4

import pytest

from render.client.errors import ClientError
from render.experimental.sandbox import (
    EgressRule,
    NetworkPolicy,
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
    return await sandboxes.wait_until_running(
        sandbox_id, owner_id=owner_id, timeout_seconds=timeout_s
    )


async def _wait_until_snapshot_available(
    sandboxes, snapshot, owner_id, timeout_s=180.0
):
    return await sandboxes.snapshots.wait_until_available(
        sandbox_group_id=snapshot.sandbox_group_id,
        snapshot_id=snapshot.id,
        owner_id=owner_id,
        timeout_seconds=timeout_s,
    )


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
async def test_list_groups_returns_the_workspace_default(sandboxes):
    # Needs no runner, only the sandboxes rollout this file already requires.
    page = await sandboxes.list_groups(owner_id=_OWNER_ID)

    assert page.groups, "expected at least one sandbox group for the e2e workspace"
    assert all(group.id.startswith("sbg-") for group in page.groups)
    assert all(group.owner_id == _OWNER_ID for group in page.groups)
    assert all(group.region for group in page.groups)
    assert any(group.is_default for group in page.groups)
    assert page.next_cursor is not None


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


async def _exec_exit_code(sandboxes, sandbox_id, owner_id, command):
    """Run command and return its exit code, whatever it is."""
    exit_event = None
    async for event in sandboxes.exec(sandbox_id, command, owner_id=owner_id):
        if isinstance(event, SandboxExecExit):
            exit_event = event
    assert exit_event is not None
    return exit_event.exit_code


@pytest.mark.asyncio
@pytest.mark.parametrize("domains", [["example.com"], []])
async def test_allow_list_network_policy_limits_egress(sandboxes, domains):
    owner_id = _OWNER_ID
    policy = NetworkPolicy(
        type="allow-list", rules=[EgressRule(domain=d) for d in domains]
    )

    if not domains:
        # The API requires a rule despite the schema omitting minItems.
        with pytest.raises(ClientError, match="rules must list at least one rule"):
            await sandboxes.create(owner_id=owner_id, network_policy=policy)
        return
    sandbox = await sandboxes.create(owner_id=owner_id, network_policy=policy)
    try:
        assert sandbox.network_policy == policy
        await _wait_until_running(sandboxes, sandbox.id, owner_id)

        fetched = await sandboxes.from_id(sandbox.id, owner_id=owner_id)
        assert fetched.network_policy == policy

        curl = "curl -sS -o /dev/null --max-time 15"
        allowed = await _exec_exit_code(
            sandboxes, sandbox.id, owner_id, f"{curl} https://example.com"
        )
        assert allowed == 0, f"allow-listed domain exited {allowed}"
        blocked = await _exec_exit_code(
            sandboxes, sandbox.id, owner_id, f"{curl} https://www.render.com"
        )
        assert blocked != 0, "domain outside the allow-list was reachable"
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


@pytest.mark.asyncio
async def test_restore_from_named_snapshot(sandboxes):
    owner_id = _OWNER_ID
    name = f"sdk-e2e-{uuid4()}"
    marker = f"marker-{uuid4()}"

    source = restored = snapshot = None
    try:
        source = await sandboxes.create(owner_id=owner_id)
        await _wait_until_running(sandboxes, source.id, owner_id)
        await _exec_output(
            sandboxes,
            source.id,
            owner_id,
            f"printf {marker} > /tmp/marker",
        )

        snapshot = await sandboxes.snapshots.create(
            source.id,
            kind="filesystem",
            name=name,
            owner_id=owner_id,
        )
        snapshot = await _wait_until_snapshot_available(sandboxes, snapshot, owner_id)
        assert snapshot.name == name

        page = await sandboxes.snapshots.list(
            sandbox_group_id=snapshot.sandbox_group_id,
            owner_id=owner_id,
        )
        assert any(
            item.id == snapshot.id and item.name == name for item in page.snapshots
        )

        restored = await sandboxes.create(
            owner_id=owner_id,
            snapshot_name=name,
        )
        await _wait_until_running(sandboxes, restored.id, owner_id)
        assert (
            await _exec_output(
                sandboxes,
                restored.id,
                owner_id,
                "cat /tmp/marker",
            )
            == marker
        )
    finally:
        cleanup = []
        if restored is not None:
            cleanup.append(sandboxes.terminate(restored.id, owner_id=owner_id))
        if source is not None:
            cleanup.append(sandboxes.terminate(source.id, owner_id=owner_id))
        if snapshot is not None and snapshot.status == "available":
            cleanup.append(
                sandboxes.snapshots.delete(
                    sandbox_group_id=snapshot.sandbox_group_id,
                    snapshot_id=snapshot.id,
                    owner_id=owner_id,
                )
            )
        results = await asyncio.gather(*cleanup, return_exceptions=True)
        errors = [result for result in results if isinstance(result, BaseException)]
        assert not errors, f"resource cleanup failed: {errors}"


@pytest.mark.parametrize("domains", [["example.com"], []])
def test_sync_allow_list_network_policy_limits_egress(domains):
    from render.render import Render

    sandboxes = Render(
        base_url=os.environ.get("RENDER_BASE_URL") or "https://api.render.com"
    ).experimental.sandboxes
    policy = NetworkPolicy(
        type="allow-list", rules=[EgressRule(domain=d) for d in domains]
    )
    if not domains:
        with pytest.raises(ClientError, match="rules must list at least one rule"):
            sandboxes.create(owner_id=_OWNER_ID, network_policy=policy)
        return
    sandbox = sandboxes.create(owner_id=_OWNER_ID, network_policy=policy)
    try:
        assert sandbox.network_policy == policy
        deadline = time.monotonic() + 180
        while True:
            fetched = sandboxes.from_id(sandbox.id, owner_id=_OWNER_ID)
            assert fetched.network_policy == policy
            if fetched.status == "running":
                break
            assert fetched.status not in {"errored", "terminated"}
            assert time.monotonic() < deadline, "sandbox did not become running"
            time.sleep(2)
        for domain in ["example.com", "www.render.com"]:
            exit_code = None
            for event in sandboxes.exec(
                sandbox.id,
                f"curl -sS -o /dev/null --max-time 15 https://{domain}",
                owner_id=_OWNER_ID,
            ):
                if isinstance(event, SandboxExecExit):
                    exit_code = event.exit_code
            assert exit_code is not None
            if domain in domains:
                assert exit_code == 0, f"allow-listed domain exited {exit_code}"
            else:
                assert exit_code != 0, "domain outside the allow-list was reachable"
    finally:
        sandboxes.terminate(sandbox.id, owner_id=_OWNER_ID)
