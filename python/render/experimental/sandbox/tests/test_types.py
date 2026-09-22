from datetime import datetime

import pytest

from render.client.errors import ClientError, RenderError
from render.experimental.sandbox.errors import (
    SandboxExecError,
    SandboxExecStreamError,
    SandboxNotFoundError,
    SnapshotNotFoundError,
    SnapshotNotReadyError,
    SnapshotPlanMismatchError,
)
from render.experimental.sandbox.types import (
    Sandbox,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxGroup,
    SandboxGroupList,
    SandboxList,
    Snapshot,
    SnapshotList,
)


def test_sandbox_has_expected_fields():
    sb = Sandbox(
        id="sbx-1",
        status="running",
        plan="starter",
        network_policy="deny-all",
        region="oregon",
        timeout_seconds=7200,
        created_at=datetime(2026, 7, 17),
    )
    assert sb.id == "sbx-1"
    assert sb.network_policy == "deny-all"
    assert sb.terminated_at is None


def test_snapshot_has_expected_fields():
    snapshot = Snapshot(
        id="snp-1",
        sandbox_group_id="sbg-1",
        source_sandbox_id="sbx-1",
        kind="filesystem",
        status="creating",
        plan="starter",
        requested_at=datetime(2026, 9, 1),
        expires_at=datetime(2026, 9, 8),
    )
    assert snapshot.id == "snp-1"
    assert snapshot.kind == "filesystem"
    assert snapshot.status == "creating"
    assert snapshot.name is None
    assert snapshot.captured_at is None
    assert snapshot.expires_at == datetime(2026, 9, 8)
    assert snapshot.size_bytes is None
    assert snapshot.error is None


def test_snapshot_list_defaults_are_empty():
    page = SnapshotList()
    assert page.snapshots == []
    assert page.next_cursor is None


def test_sandbox_list_defaults_are_empty():
    page = SandboxList()
    assert page.sandboxes == []
    assert page.next_cursor is None


def test_sandbox_group_has_expected_fields():
    group = SandboxGroup(
        id="sbg-1",
        owner_id="tea-1",
        name="Default",
        region="oregon",
        is_default=True,
        concurrency_limit=10,
        created_at=datetime(2026, 7, 2),
        updated_at=datetime(2026, 7, 2),
    )
    assert group.id == "sbg-1"
    assert group.name == "Default"
    assert group.is_default is True
    assert group.concurrency_limit == 10
    assert group.environment_id is None


def test_sandbox_group_list_defaults_are_empty():
    page = SandboxGroupList()
    assert page.groups == []
    assert page.next_cursor is None


def test_exec_event_shapes():
    out = SandboxExecOutput(stream="stdout", data="hi\n")
    done = SandboxExecExit(exit_code=7)
    assert out.stream == "stdout"
    assert out.data == "hi\n"
    assert done.exit_code == 7


def test_not_found_is_a_client_error():
    err = SandboxNotFoundError("missing")
    assert isinstance(err, ClientError)
    assert isinstance(err, RenderError)


def test_exec_errors_subclass_render_error():
    stream_err = SandboxExecStreamError(408, "timed out")
    assert stream_err.status == 408
    assert stream_err.message == "timed out"
    assert isinstance(stream_err, RenderError)
    assert isinstance(SandboxExecError("boom"), RenderError)


@pytest.mark.parametrize(
    "error_type",
    [SnapshotNotFoundError, SnapshotNotReadyError, SnapshotPlanMismatchError],
)
def test_snapshot_errors_are_client_errors_carrying_a_code(error_type):
    err = error_type("boom", code="some_code")
    assert isinstance(err, ClientError)
    assert str(err) == "boom"
    assert err.code == "some_code"
    assert error_type("boom").code is None
