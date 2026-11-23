from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
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
        "method": "delete",
        "url": "/sandboxes/{sandbox_id}/ports/{port}".format(
            sandbox_id=quote(str(sandbox_id), safe=""),
            port=quote(str(port), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
        response_409 = Error.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Any | Error]:
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
) -> Response[Any | Error]:
    """Hide a sandbox port

     Hide a configured port without waking a suspended sandbox. Ports are hidden by default. Works in any
    status but errored. Succeeds if the port is already closed. While the sandbox has a running VM,
    returns only after routing to the port is revoked and its open connections, including WebSockets and
    streaming responses, are disconnected. If that can't be confirmed, the port stays closed and the
    request fails with a 503; retrying confirms again.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
) -> Any | Error | None:
    """Hide a sandbox port

     Hide a configured port without waking a suspended sandbox. Ports are hidden by default. Works in any
    status but errored. Succeeds if the port is already closed. While the sandbox has a running VM,
    returns only after routing to the port is revoked and its open connections, including WebSockets and
    streaming responses, are disconnected. If that can't be confirmed, the port stays closed and the
    request fails with a 503; retrying confirms again.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
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
) -> Response[Any | Error]:
    """Hide a sandbox port

     Hide a configured port without waking a suspended sandbox. Ports are hidden by default. Works in any
    status but errored. Succeeds if the port is already closed. While the sandbox has a running VM,
    returns only after routing to the port is revoked and its open connections, including WebSockets and
    streaming responses, are disconnected. If that can't be confirmed, the port stays closed and the
    request fails with a 503; retrying confirms again.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
) -> Any | Error | None:
    """Hide a sandbox port

     Hide a configured port without waking a suspended sandbox. Ports are hidden by default. Works in any
    status but errored. Succeeds if the port is already closed. While the sandbox has a running VM,
    returns only after routing to the port is revoked and its open connections, including WebSockets and
    streaming responses, are disconnected. If that can't be confirmed, the port stays closed and the
    request fails with a 503; retrying confirms again.

    Args:
        sandbox_id (str): The ID of the sandbox. Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        port (int):
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            port=port,
            client=client,
            owner_id=owner_id,
        )
    ).parsed
