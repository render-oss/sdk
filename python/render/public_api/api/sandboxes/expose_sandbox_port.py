from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_exposed_port import SandboxExposedPort
from ...models.sandbox_port_limit_error import SandboxPortLimitError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    port: int,
    *,
    owner_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/sandboxes/{sandbox_id}/ports/{port}".format(
            sandbox_id=quote(str(sandbox_id), safe=""),
            port=quote(str(port), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | Error | SandboxPortLimitError | SandboxExposedPort | None:
    if response.status_code == 200:
        response_200 = SandboxExposedPort.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:

        def _parse_response_409(data: object) -> Error | SandboxPortLimitError:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_409_type_0 = SandboxPortLimitError.from_dict(data)

                return response_409_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_409_type_1 = Error.from_dict(data)

            return response_409_type_1

        response_409 = _parse_response_409(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | Error | SandboxPortLimitError | SandboxExposedPort]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | Error | SandboxPortLimitError | SandboxExposedPort]:
    """Expose a sandbox port

     Expose a port publicly. Works while the sandbox is creating, running, resuming, suspending or
    suspended; a sandbox without a running VM applies the port when it starts. Returns the same URL if
    already exposed. Changes propagate asynchronously. Render does not check application readiness.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Error | SandboxPortLimitError | SandboxExposedPort]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        port=port,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | Error | SandboxPortLimitError | SandboxExposedPort | None:
    """Expose a sandbox port

     Expose a port publicly. Works while the sandbox is creating, running, resuming, suspending or
    suspended; a sandbox without a running VM applies the port when it starts. Returns the same URL if
    already exposed. Changes propagate asynchronously. Render does not check application readiness.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Error | SandboxPortLimitError | SandboxExposedPort
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        port=port,
        client=client,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | Error | SandboxPortLimitError | SandboxExposedPort]:
    """Expose a sandbox port

     Expose a port publicly. Works while the sandbox is creating, running, resuming, suspending or
    suspended; a sandbox without a running VM applies the port when it starts. Returns the same URL if
    already exposed. Changes propagate asynchronously. Render does not check application readiness.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Error | SandboxPortLimitError | SandboxExposedPort]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        port=port,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    port: int,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | Error | SandboxPortLimitError | SandboxExposedPort | None:
    """Expose a sandbox port

     Expose a port publicly. Works while the sandbox is creating, running, resuming, suspending or
    suspended; a sandbox without a running VM applies the port when it starts. Returns the same URL if
    already exposed. Changes propagate asynchronously. Render does not check application readiness.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Error | SandboxPortLimitError | SandboxExposedPort
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            port=port,
            client=client,
            owner_id=owner_id,
        )
    ).parsed
