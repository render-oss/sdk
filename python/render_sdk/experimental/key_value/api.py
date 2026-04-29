"""Layer 2 API client tailored to Key Value use-cases."""

import os
from http import HTTPStatus

from render_sdk.client.errors import ClientError, ServerError
from render_sdk.public_api.api.key_value import (
    create_key_value,
    list_key_value,
    retrieve_key_value,
    retrieve_key_value_connection_info,
    update_key_value,
)
from render_sdk.public_api.client import AuthenticatedClient
from render_sdk.public_api.models.key_value import KeyValue
from render_sdk.public_api.models.key_value_connection_info import (
    KeyValueConnectionInfo,
)
from render_sdk.public_api.models.key_value_detail import KeyValueDetail
from render_sdk.public_api.models.key_value_patch_input import KeyValuePATCHInput
from render_sdk.public_api.models.key_value_post_input import KeyValuePOSTInput
from render_sdk.public_api.models.maxmemory_policy import MaxmemoryPolicy
from render_sdk.public_api.types import Unset

from .types import KeyValueInstance
from .utils import _format_error_message


def _is_render() -> bool:
    return os.environ.get("RENDER") == "true"


def _unauthorized_error() -> ClientError:
    return ClientError(
        _format_error_message(
            "The provided Render API Token is not authorized.",
            "Please double-check the token is correct.",
        )
    )


def _unexpected_error(operation: str, status_code: int) -> ClientError | ServerError:
    message = f"Unexpected error while {operation}"
    if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        return ServerError(message)
    return ClientError(message)


def _to_instance(detail: KeyValue | KeyValueDetail) -> KeyValueInstance:
    maxmemory_policy = detail.options.maxmemory_policy
    return KeyValueInstance(
        id=detail.id,
        status=detail.status,
        plan=detail.plan,
        maxmemory_policy=(
            None
            if isinstance(maxmemory_policy, Unset)
            else MaxmemoryPolicy(maxmemory_policy)
        ),
        ip_allow_list=list(detail.ip_allow_list),
    )


class KeyValueApi:
    """Layer 2 Key Value API client.

    Wraps the generated OpenAPI operations with typed return values and
    explicit error messages for common failure cases (401, 404).
    For most use cases, prefer :class:`KeyValueClient`.
    """

    def __init__(self, client: "AuthenticatedClient"):
        self.client = client

    async def find_by_id(self, key_value_id: str) -> KeyValueInstance:
        """Look up a Key Value instance by its service ID.

        Args:
            key_value_id: The Render service ID of the Key Value instance.

        Returns:
            KeyValueInstance: Instance state.

        Raises:
            ClientError: If the ID is not found or the API token is unauthorized.
            ServerError: For 5xx server errors.
        """
        response = await retrieve_key_value.asyncio_detailed(
            key_value_id=key_value_id,
            client=self.client,
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise _unauthorized_error()

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ClientError(
                _format_error_message(
                    f"Unable to locate a Key Value with ID {key_value_id}",
                    "Please double-check the ID is correct",
                )
            )

        if not isinstance(response.parsed, KeyValueDetail):
            raise _unexpected_error(
                f"fetching info about Key Value {key_value_id}",
                response.status_code,
            )

        return _to_instance(response.parsed)

    async def find_by_name(self, name: str, owner_id: str) -> KeyValueInstance | None:
        """Look up a Key Value instance by name and owner ID.

        Args:
            name: Name of the Key Value instance.
            owner_id: Owner (workspace or team) ID.

        Returns:
            KeyValueInstance if an instance with that name exists, otherwise None.

        Raises:
            ClientError: If the API token is unauthorized.
            ServerError: For 5xx server errors.
        """
        response = await list_key_value.asyncio_detailed(
            client=self.client,
            name=[name],
            owner_id=[owner_id],
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise _unauthorized_error()

        if not isinstance(response.parsed, list):
            raise _unexpected_error(
                f"fetching information about Key Value named '{name}'",
                response.status_code,
            )

        if len(response.parsed) == 0:
            return None

        # `name` is unique per-workspace and the search looks for exact matches, not
        # partial, so there will only ever be zero or one result in the response
        return _to_instance(response.parsed[0].key_value)

    async def get_connection_info(self, key_value_id: str) -> str:
        """Get the Redis connection URL for a Key Value instance.

        Returns the internal connection string when running on Render, and
        the external connection string otherwise (detected via the ``RENDER``
        environment variable).

        Args:
            key_value_id: The Render service ID of the Key Value instance.

        Returns:
            str: A ``redis://`` or ``rediss://`` connection URL.

        Raises:
            ClientError: If the API token is unauthorized.
            ServerError: For 5xx server errors.
        """
        response = await retrieve_key_value_connection_info.asyncio_detailed(
            key_value_id=key_value_id,
            client=self.client,
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise _unauthorized_error()

        if not isinstance(response.parsed, KeyValueConnectionInfo):
            raise _unexpected_error(
                f"fetching connection information for Key Value {key_value_id}",
                response.status_code,
            )

        if _is_render():
            return response.parsed.internal_connection_string
        return response.parsed.external_connection_string

    async def create_instance(self, details: KeyValuePOSTInput) -> KeyValueInstance:
        """Create a new Key Value instance.

        Args:
            details: Creation parameters (name, owner ID, plan, etc.).

        Returns:
            KeyValueInstance: The newly created instance.

        Raises:
            ClientError: If the API token is unauthorized or the request is invalid.
            ServerError: For 5xx server errors.
        """
        response = await create_key_value.asyncio_detailed(
            client=self.client,
            body=details,
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise _unauthorized_error()

        if not isinstance(response.parsed, KeyValueDetail):
            raise _unexpected_error(
                f"creating new Key Value named '{details.name}'",
                response.status_code,
            )

        return _to_instance(response.parsed)

    async def update_instance(
        self, key_value_id: str, update: KeyValuePATCHInput
    ) -> KeyValueInstance:
        """Update a Key Value instance's configuration.

        Args:
            key_value_id: The Render service ID of the Key Value instance.
            update: Configuration changes to apply.

        Returns:
            KeyValueInstance: The updated instance.

        Raises:
            ClientError: If the API token is unauthorized or the request is invalid.
            ServerError: For 5xx server errors.
        """
        response = await update_key_value.asyncio_detailed(
            key_value_id=key_value_id,
            client=self.client,
            body=update,
        )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise _unauthorized_error()

        if not isinstance(response.parsed, KeyValueDetail):
            raise _unexpected_error(
                f"updating Key Value {key_value_id}",
                response.status_code,
            )

        return _to_instance(response.parsed)
