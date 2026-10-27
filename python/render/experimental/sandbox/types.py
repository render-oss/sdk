"""Public return and event types for the sandbox client."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from render.experimental.sandbox._wait import DEFAULT_INTERVAL_SECONDS

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
    sandbox_group_id: str | None = None


@dataclass
class SandboxWaitOptions:
    """How create(wait=...) and snapshots.create(wait=...) wait for the result.

    timeout_seconds bounds the whole wait, including status checks. None uses
    the default: 60 seconds for a sandbox, 5 minutes for a snapshot.
    interval_seconds is the first delay between checks. It doubles after each
    check, up to 2 seconds or interval_seconds, whichever is longer.
    """

    timeout_seconds: float | None = None
    interval_seconds: float = DEFAULT_INTERVAL_SECONDS


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
class BuildSource:
    """The OCI image a build converts, as the registry resolved it.

    repository is the registry host and namespace, like ``docker.io/library``,
    image the name within it, like ``python``, and reference the tag or digest
    the build was requested at, like ``3.13``.
    """

    repository: str
    image: str
    reference: str


@dataclass
class Build:
    """A sandbox build, as returned by builds.create and builds.from_id.

    status is ``pending``, ``running``, ``succeeded`` or ``failed``.
    """

    id: str
    sandbox_group_id: str
    name: str
    source: BuildSource
    source_digest: str
    status: str
    created_at: datetime
    failure_reason: str | None = None
    finished_at: datetime | None = None


@dataclass
class RegistryCredential:
    """Credentials for pulling a build's source image from a private registry.

    The API uses them for that build only and does not store them.
    """

    username: str
    password: str = field(repr=False)


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
