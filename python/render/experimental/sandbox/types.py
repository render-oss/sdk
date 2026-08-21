"""Public return and event types for the sandbox client."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Sandbox:
    """A sandbox snapshot returned by create, from_id, and list."""

    id: str
    status: str
    plan: str
    network_policy: str
    region: str
    timeout_seconds: int
    created_at: datetime
    terminated_at: datetime | None = None


@dataclass
class SandboxList:
    """A page of sandboxes with an optional pagination cursor."""

    sandboxes: list[Sandbox] = field(default_factory=list)
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
