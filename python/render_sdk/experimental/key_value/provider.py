"""High-level Key Value provider with automatic provisioning and configuration sync."""

import asyncio
import re
from typing import TYPE_CHECKING, Any

from render_sdk.client.errors import RenderError
from render_sdk.public_api.models.database_status import DatabaseStatus
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.key_value_post_input import KeyValuePOSTInput
from render_sdk.public_api.types import UNSET

from .api import KeyValueApi
from .compare import compare_instance_configuration
from .types import (
    ConnectionInfo,
    InstanceConfiguration,
    KeyValueInstance,
    NameOwnerIdOptions,
    Options,
    ServiceIdOptions,
)
from .utils import _format_error_message

if TYPE_CHECKING:
    from redis.asyncio import Redis

# Matches redis:// and rediss:// URLs with optional credentials
_CONNECTION_RE = re.compile(
    r"rediss?://((?P<username>[\w.~_-]+):(?P<password>[\w.~_-]+)@)?(?P<host>[\w.~_-]+):(?P<port>[0-9]+)"
)

# Max sleep per iteration; total worst-case wait is ~17 minutes
_MAX_DELAY_SECONDS = 512


class KeyValueProvider:
    """High-level Key Value provider.

    Manages instance discovery, optional auto-provisioning, automatic
    configuration sync, and Redis client construction. Use this when you want
    the SDK to handle instance lifecycle on your behalf.

    Example:
        ```python
        from render_sdk import RenderAsync
        from render_sdk.experimental.key_value import NameOwnerIdOptions

        render = RenderAsync()
        kv = render.experimental.key_value

        # Returns a redis.asyncio.Redis client, provisioning the instance if needed
        redis = await kv.new_client(NameOwnerIdOptions(name="my-cache"))
        await redis.set("hello", "world")

        # Or just get connection details (still provisions the instance if needed)
        info = await kv.connection_info(NameOwnerIdOptions(name="my-cache"))
        print(f"redis://{info.host}:{info.port}")
        ```
    """

    def __init__(self, api: KeyValueApi, default_owner_id: str | None = None):
        """
        Args:
            api: Low-level Key Value API client.
            default_owner_id: Fallback owner ID when options don't supply one.
                Typically set from ``RENDER_WORKSPACE_ID``.
        """
        self._api = api
        self._default_owner_id = default_owner_id

    async def new_client(self, options: Options, **kwargs: Any) -> "Redis":
        """Return a configured ``redis.asyncio.Redis`` client for the instance.

        Looks up the instance by service ID or name, optionally provisions it if
        not found, syncs configuration, then constructs a Redis client from the
        connection URL. Additional keyword arguments are forwarded to
        ``redis.asyncio.Redis.from_url()``.

        Args:
            options: Lookup strategy and optional desired configuration.
                Use :class:`ServiceIdOptions` to look up by service ID, or
                :class:`NameOwnerIdOptions` to look up by name.
            **kwargs: Extra arguments passed through to ``Redis.from_url()``.

        Returns:
            redis.asyncio.Redis: A configured but not yet connected Redis client.

        Raises:
            ImportError: If ``redis`` is not installed.
            RenderError: If the instance cannot be found, provisioned, or reaches
                an unrecoverable state.
            ClientError: For authorization or validation errors from the Render API.
            ServerError: For Render API server errors.
        """
        try:
            import redis.asyncio as redis_asyncio
        except ImportError as exc:
            raise ImportError(
                "redis-py is required for new_client(). "
                "Install it with: pip install redis"
            ) from exc

        url = await self._load_connection_string(options)
        return redis_asyncio.Redis.from_url(url, **kwargs)

    async def connection_info(self, options: Options) -> ConnectionInfo:
        """Return parsed connection details for the Key Value instance.

        Looks up the instance by service ID or name, optionally provisions it if
        not found, and syncs configuration.

        Args:
            options: Lookup strategy and optional desired configuration.
                Use :class:`ServiceIdOptions` to look up by service ID, or
                :class:`NameOwnerIdOptions` to look up by name.

        Returns:
            ConnectionInfo: Parsed host, port, and optional credentials.

        Raises:
            RenderError: If the instance cannot be found, provisioned, or the
                connection string is in an unexpected format.
            ClientError: For authorization or validation errors from the Render API.
            ServerError: For Render API server errors.
        """
        connection_string = await self._load_connection_string(options)
        return _parse_connection_string(connection_string)

    async def _load_connection_string(self, options: Options) -> str:
        if isinstance(options, ServiceIdOptions):
            details = await self._find_instance_by_service_id(options)
        else:
            details = await self._find_instance_by_name_owner_id(options)

        return await self._api.get_connection_info(details.id)

    async def _find_instance_by_service_id(
        self, options: ServiceIdOptions
    ) -> KeyValueInstance:
        details = await self._api.find_by_id(options.service_id)
        return await self._ensure_configuration_up_to_date(options, details)

    async def _find_instance_by_name_owner_id(
        self, options: NameOwnerIdOptions
    ) -> KeyValueInstance:
        owner_id = self._resolve_owner_id(options.owner_id)
        details = await self._api.find_by_name(options.name, owner_id)

        if details is None:
            if options.auto_provision is False:
                raise RenderError(
                    _format_error_message(
                        f"Unable to locate Key Value named '{options.name}'",
                        "Please double-check that the name is correct.\n"
                        "If you would like one to be created automatically, ensure "
                        "that 'auto_provision_enabled' is not set to False.",
                    )
                )

            config = InstanceConfiguration()
            if isinstance(options.auto_provision, InstanceConfiguration):
                config = options.auto_provision
            return await self._provision_new_instance(options.name, owner_id, config)

        return await self._ensure_configuration_up_to_date(options, details)

    async def _provision_new_instance(
        self, name: str, resolved_owner_id: str, config: InstanceConfiguration
    ) -> KeyValueInstance:
        body = KeyValuePOSTInput(
            name=name,
            owner_id=resolved_owner_id,
            plan=(
                KeyValuePlan(config.plan)
                if config.plan is not None
                else KeyValuePlan.FREE
            ),
            maxmemory_policy=(
                config.maxmemory_policy
                if config.maxmemory_policy is not None
                else UNSET
            ),
            ip_allow_list=(
                config.ip_allow_list if config.ip_allow_list is not None else UNSET
            ),
        )
        data = await self._api.create_instance(body)
        return await self._wait_for_instance_available(data.id)

    async def _ensure_configuration_up_to_date(
        self, options: Options, details: KeyValueInstance
    ) -> KeyValueInstance:
        if not isinstance(options.auto_provision, InstanceConfiguration):
            return details

        update = compare_instance_configuration(options.auto_provision, details)

        if update is not None:
            data = await self._api.update_instance(details.id, update)
            return await self._wait_for_instance_available(data.id)

        return details

    async def _wait_for_instance_available(self, key_value_id: str) -> KeyValueInstance:
        """Poll until the instance status is 'available'.

        Uses exponential backoff starting at 1 second, doubling each iteration
        up to a cap of 512 seconds per sleep (~17 minutes total worst case).
        """
        retry_delay = 1.0

        while retry_delay <= _MAX_DELAY_SECONDS:
            try:
                data = await self._api.find_by_id(key_value_id)
            except RenderError as err:
                raise RenderError(
                    _format_error_message(
                        "Unable to look up status of Key Value instance.",
                        "This is most likely a Render error, please try again.",
                    )
                ) from err

            if data.status == DatabaseStatus.AVAILABLE:
                return data
            elif data.status in (
                DatabaseStatus.CREATING,
                DatabaseStatus.CONFIG_RESTART,
                DatabaseStatus.UPDATING_INSTANCE,
                DatabaseStatus.UNAVAILABLE,
            ):
                await asyncio.sleep(retry_delay)
            else:
                raise RenderError(
                    _format_error_message(
                        "The requested Key Value instance is not available.",
                        "Please view the Key Value on dashboard.render.com to verify "
                        "its status.",
                    )
                )

            retry_delay *= 2

        raise RenderError(
            _format_error_message(
                "Timed out waiting for instance to become available.",
                "Please check the Key Value on dashboard.render.com to make sure it is "
                "ready, then try again.",
            )
        )

    def _resolve_owner_id(self, owner_id: str | None) -> str:
        resolved = owner_id or self._default_owner_id
        if not resolved:
            raise RenderError(
                "owner_id is required. Provide it as a parameter or set the "
                "RENDER_WORKSPACE_ID environment variable."
            )
        return resolved


def _parse_connection_string(connection: str) -> ConnectionInfo:
    match = _CONNECTION_RE.search(connection)

    if not match:
        raise RenderError(
            _format_error_message(
                "The Key Value connection string was in an unexpected format",
                "Please confirm you are on the most recent version of the Render SDK",
            )
        )

    return ConnectionInfo(
        username=match.group("username"),
        password=match.group("password"),
        host=match.group("host"),
        port=int(match.group("port")),
    )
