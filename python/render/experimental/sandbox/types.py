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
    # A label set at create. Names aren't unique; use id to address the sandbox.
    name: str | None = None


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
class ImageSource:
    """The OCI image an import converts, as the registry resolved it.

    repository is the registry host and namespace, like ``docker.io/library``,
    image the name within it, like ``python``, and reference the tag or digest
    the image was imported at, like ``3.13``.
    """

    repository: str
    image: str
    reference: str


@dataclass
class Image:
    """A sandbox image, as returned by images.import_, from_id and wait_until_ready.

    status is ``pending``, ``running``, ``succeeded`` or ``failed``. Sandboxes
    can start from the image once it has ``succeeded``.
    """

    id: str
    sandbox_group_id: str
    name: str
    source: ImageSource
    source_digest: str
    status: str
    created_at: datetime
    failure_reason: str | None = None
    finished_at: datetime | None = None


@dataclass
class ImageList:
    """A page of images with an optional pagination cursor."""

    images: list[Image] = field(default_factory=list)
    next_cursor: str | None = None


@dataclass
class RegistryCredentials:
    """Credentials for pulling an image from a private registry.

    The API uses them for that import only and does not store them.
    """

    username: str
    password: str = field(repr=False)


# Deprecated aliases from when images were called builds.
Build = Image
BuildSource = ImageSource
RegistryCredential = RegistryCredentials


@dataclass
class CredentialInjection:
    """How a credential is added to a sandbox request that matches it.

    type is ``header``, ``cookie``, ``query`` or ``basic``. name is the header,
    cookie or query parameter to set; it is required for every type but
    ``basic``, which rejects it. template wraps the secret, like
    ``Bearer ${SECRET}``, with 1 to 5 occurrences of ``${SECRET}``; omit it to
    send the secret as is. ``basic`` expects the secret, after the template,
    in ``username:password`` form.
    """

    type: str
    name: str | None = None
    template: str | None = None


@dataclass
class CredentialVersion:
    """One saved configuration of a credential.

    fingerprint covers the routing, injection and secret value, so two
    versions in the same sandbox group with the same fingerprint are
    equivalent. restored_from_version_id is set when restore created this
    version.
    """

    id: int
    updated_at: datetime
    updated_by: str
    fingerprint: str
    restored_from_version_id: int | None = None


@dataclass
class Credential:
    """A credential that Render adds to matching requests from a group's sandboxes.

    Sandboxes never see the secret value, and the API never returns it.
    domain is the exact hostname the credential applies to. methods and paths
    narrow which requests match; an empty list matches any. In paths, ``*``
    matches one path segment and ``**`` one or more.
    """

    id: str
    domain: str
    enabled: bool
    methods: list[str]
    paths: list[str]
    injection: CredentialInjection
    version: CredentialVersion | None = None


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
