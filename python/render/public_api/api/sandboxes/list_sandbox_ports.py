from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_exposed_port import SandboxExposedPort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    owner_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandboxes/{sandbox_id}/ports".format(
            sandbox_id=quote(str(sandbox_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[SandboxExposedPort] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemassandbox_exposed_ports_item_data in _response_200:
            componentsschemassandbox_exposed_ports_item = SandboxExposedPort.from_dict(
                componentsschemassandbox_exposed_ports_item_data
            )

            response_200.append(componentsschemassandbox_exposed_ports_item)

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | list[SandboxExposedPort]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | list[SandboxExposedPort]]:
    """List exposed sandbox ports

     List configured public ports and their HTTPS URLs. Returns an empty array if no ports are exposed.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxExposedPort]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | list[SandboxExposedPort] | None:
    """List exposed sandbox ports

     List configured public ports and their HTTPS URLs. Returns an empty array if no ports are exposed.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxExposedPort]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | list[SandboxExposedPort]]:
    """List exposed sandbox ports

     List configured public ports and their HTTPS URLs. Returns an empty array if no ports are exposed.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxExposedPort]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | list[SandboxExposedPort] | None:
    """List exposed sandbox ports

     List configured public ports and their HTTPS URLs. Returns an empty array if no ports are exposed.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxExposedPort]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            owner_id=owner_id,
        )
    ).parsed
