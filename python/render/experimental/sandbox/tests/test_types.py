from datetime import datetime
from typing import get_args

import pytest

from render.client.errors import ClientError, RenderError
from render.experimental.sandbox.errors import (
    BuildNotFoundError,
    BuildNotReadyError,
    ImageFailedError,
    ImageNotFoundError,
    ImageNotReadyError,
    ImageWaitTimeoutError,
    SandboxExecError,
    SandboxExecStreamError,
    SandboxNotFoundError,
    SnapshotNotFoundError,
    SnapshotNotReadyError,
    SnapshotPlanMismatchError,
)
from render.experimental.sandbox.types import (
    Build,
    BuildSource,
    EgressRule,
    Image,
    ImageSource,
    NetworkPolicy,
    RegistryCredential,
    RegistryCredentials,
    Sandbox,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxGroup,
    SandboxGroupList,
    SandboxList,
    SandboxPlan,
    Snapshot,
    SnapshotList,
)
from render.public_api.models.sandbox_plan import SandboxPlan as GeneratedSandboxPlan


def test_sandbox_has_expected_fields():
    sb = Sandbox(
        id="sbx-1",
        status="running",
        plan="1c-2g",
        network_policy=NetworkPolicy(type="deny-all"),
        region="oregon",
        timeout_seconds=7200,
        idle_timeout_seconds=900,
        created_at=datetime(2026, 7, 17),
    )
    assert sb.id == "sbx-1"
    assert sb.network_policy.type == "deny-all"
    assert sb.network_policy.rules == []
    assert sb.idle_timeout_seconds == 900
    assert sb.terminated_at is None


def test_egress_rule_defaults_to_https():
    assert EgressRule(domain="pypi.org").protocol == "https"


def test_snapshot_has_expected_fields():
    snapshot = Snapshot(
        id="snp-1",
        sandbox_group_id="sbg-1",
        source_sandbox_id="sbx-1",
        kind="filesystem",
        status="creating",
        plan="1c-2g",
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


def test_image_has_expected_fields():
    image = Image(
        id="sbb-1",
        sandbox_group_id="sbg-1",
        name="python",
        source=ImageSource(
            repository="docker.io/library", image="python", reference="3.13"
        ),
        source_digest="sha256:abc",
        status="running",
        created_at=datetime(2026, 10, 1),
    )
    assert image.id == "sbb-1"
    assert image.source.image == "python"
    assert image.failure_reason is None
    assert image.finished_at is None


def test_registry_credentials_hide_the_password_from_repr():
    credentials = RegistryCredentials(username="bot", password="s3cret")
    assert "bot" in repr(credentials)
    assert "s3cret" not in repr(credentials)


@pytest.mark.parametrize(
    ("alias", "current"),
    [
        (Build, Image),
        (BuildSource, ImageSource),
        (RegistryCredential, RegistryCredentials),
        (BuildNotFoundError, ImageNotFoundError),
        (BuildNotReadyError, ImageNotReadyError),
    ],
)
def test_build_names_alias_the_image_names(alias, current):
    assert alias is current


def test_image_wait_errors_carry_the_image_id():
    failed = ImageFailedError("boom", image_id="sbb-1", failure_reason="bad arch")
    assert isinstance(failed, RenderError)
    assert failed.image_id == "sbb-1"
    assert failed.failure_reason == "bad arch"
    timed_out = ImageWaitTimeoutError(
        "slow", image_id="sbb-1", timeout_seconds=600, last_status="running"
    )
    assert isinstance(timed_out, RenderError)
    assert timed_out.image_id == "sbb-1"
    assert timed_out.last_status == "running"


@pytest.mark.parametrize("error_type", [ImageNotFoundError, ImageNotReadyError])
def test_image_errors_are_client_errors(error_type):
    err = error_type("boom")
    assert isinstance(err, ClientError)
    assert str(err) == "boom"
    assert err.code is None


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


def test_sandbox_plan_matches_generated_plans():
    """SandboxPlan is handwritten, so it has to track the generated schema.

    starter, standard and pro are left out because SandboxPlan does not
    suggest them.
    """
    generated = {plan.value for plan in GeneratedSandboxPlan}
    assert set(get_args(SandboxPlan)) == generated - {"starter", "standard", "pro"}
