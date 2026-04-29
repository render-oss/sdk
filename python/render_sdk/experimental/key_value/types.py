"""Type definitions for Key Value experimental feature."""

from dataclasses import dataclass
from typing import Literal

from render_sdk.public_api.models.cidr_block_and_description import (
    CidrBlockAndDescription,
)
from render_sdk.public_api.models.database_status import DatabaseStatus
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.maxmemory_policy import MaxmemoryPolicy

__all__ = [
    "ConnectionInfo",
    "InstanceConfiguration",
    "IPAllowListEntry",
    "KeyValueInstance",
    "MaxmemoryPolicy",
    "NameOwnerIdOptions",
    "Options",
    "OwnerId",
    "Plan",
    "ServiceIdOptions",
]

# Excludes "custom", which is a managed plan not available for provisioning
Plan = Literal[
    "free",
    "starter",
    "standard",
    "pro",
    "pro_plus",
]

# Owner ID (format: "tea-xxx" for workspace teams, "own-xxx" for individuals)
OwnerId = str

# IP allow list entry is a CIDR block paired with a description
IPAllowListEntry = CidrBlockAndDescription


@dataclass
class KeyValueInstance:
    """Subset of Key Value instance state needed by the client.

    Returned by all KeyValueApi methods so that client.py and compare.py
    don't depend on the generated KeyValue / KeyValueDetail models directly.

    Attributes:
        id: The Render service ID of the instance.
        status: Current lifecycle status.
        plan: Current billing plan.
        maxmemory_policy: Current eviction policy, or None if unset.
        ip_allow_list: Current IP allow list entries.
    """

    id: str
    status: DatabaseStatus
    plan: KeyValuePlan
    maxmemory_policy: MaxmemoryPolicy | None
    ip_allow_list: list[IPAllowListEntry]


@dataclass
class ConnectionInfo:
    """Parsed connection information for a Key Value instance.

    Attributes:
        host: Hostname of the Key Value instance.
        port: Port number.
        username: Optional username for authentication.
        password: Optional password for authentication.
    """

    host: str
    port: int
    username: str | None = None
    password: str | None = None


@dataclass
class InstanceConfiguration:
    """Configuration settings for an instance, used for automatic provisioning
    and settings sync

    Attributes:
        plan: Desired plan
        maxmemory_policy: Desired eviction policy
        ip_allow_list: Desired IP allowlist for external connections
    """

    plan: Plan | None = None
    maxmemory_policy: MaxmemoryPolicy | None = None
    ip_allow_list: list[IPAllowListEntry] | None = None


@dataclass
class ServiceIdOptions:
    """Options for identifying a Key Value instance by its Render service ID.

    Attributes:
        service_id: The Render service ID of the Key Value instance.
        auto_provision: Instance configuration settings to use for automatic
            provisioning and settings sync. Set to `False` to disable
            automatic instance changes
    """

    service_id: str
    auto_provision: bool | InstanceConfiguration | None = None


@dataclass
class NameOwnerIdOptions:
    """Options for identifying a Key Value instance by name.

    Attributes:
        name: Name of the Key Value instance.
        owner_id: Owner ID of the instance. Must be set here, when initializing the
            Render client, or via the RENDER_WORKSPACE_ID environment variable.
        auto_provision: Instance configuration settings to use for automatic
            provisioning and settings sync. Set to `False` to disable
            automatic instance changes
    """

    name: str
    owner_id: OwnerId | None = None
    auto_provision: bool | InstanceConfiguration | None = None


Options = ServiceIdOptions | NameOwnerIdOptions
