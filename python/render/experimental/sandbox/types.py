"""Public return and event types for the sandbox client."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

# The plans the API offered when this SDK was released, for editor hints. The
# API can add plans at any time, and create() sends any plan string as is, so a
# newer plan works without an SDK update.
SandboxPlan = Literal["1c-2g", "2c-4g", "4c-8g", "8c-16g"]


@dataclass
class EgressRule:
    """A destination a sandbox under an ``allow-list`` network policy may reach.

    Matching on domain is exact: ``foo.local`` does not cover ``api.foo.local``,
    which needs its own rule or ``*.foo.local``. A wildcard is only allowed as
    the leftmost label.
    """

    domain: str
    protocol: str = "https"


@dataclass
class NetworkPolicy:
    """How a sandbox's outbound traffic is handled.

    type is ``allow-all``, ``deny-all``, or ``allow-list``. rules lists the
    destinations an ``allow-list`` policy admits and is empty otherwise.
    """

    type: str
    rules: list[EgressRule] = field(default_factory=list)


@dataclass
class Sandbox:
    """A sandbox as returned by create, from_id, and list."""

    id: str
    status: str
    plan: str
    network_policy: NetworkPolicy
    region: str
    timeout_seconds: int
    idle_timeout_seconds: int
    created_at: datetime
    terminated_at: datetime | None = None


@dataclass
class SandboxList:
    """A page of sandboxes with an optional pagination cursor."""

    sandboxes: list[Sandbox] = field(default_factory=list)
    next_cursor: str | None = None


@dataclass
class SandboxGroup:
    """A sandbox group as returned by list_groups."""

    id: str
    owner_id: str
    name: str
    region: str
    is_default: bool
    concurrency_limit: int
    created_at: datetime
    updated_at: datetime
    environment_id: str | None = None


@dataclass
class SandboxGroupList:
    """A page of sandbox groups with an optional pagination cursor."""

    groups: list[SandboxGroup] = field(default_factory=list)
    next_cursor: str | None = None


@dataclass
class Snapshot:
    """A snapshot of a sandbox, as returned by snapshots.create, from_id, and list."""

    id: str
    sandbox_group_id: str
    source_sandbox_id: str
    kind: str
    status: str
    plan: str
    requested_at: datetime
    expires_at: datetime
    name: str | None = None
    captured_at: datetime | None = None
    size_bytes: int | None = None
    error: str | None = None


@dataclass
class SnapshotList:
    """A page of snapshots with an optional pagination cursor."""

    snapshots: list[Snapshot] = field(default_factory=list)
    next_cursor: str | None = None


@dataclass
class SandboxExecOutput:
    """A chunk of stdout or stderr from an exec stream."""

    stream: str
    data: str


@dataclass
class SandboxExecExit:
    """The terminal exit event of an exec stream."""

    exit_code: int


SandboxExecEvent = SandboxExecOutput | SandboxExecExit
