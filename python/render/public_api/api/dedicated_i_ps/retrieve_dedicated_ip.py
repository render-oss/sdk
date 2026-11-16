from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dedicated_ip import DedicatedIP
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    dedicated_ip_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/dedicated-ips/{dedicated_ip_id}".format(
            dedicated_ip_id=quote(str(dedicated_ip_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> DedicatedIP | Error | None:
    if response.status_code == 200:
        response_200 = DedicatedIP.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

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
) -> Response[DedicatedIP | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dedicated_ip_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DedicatedIP | Error]:
    """Retrieve dedicated IP set

     Retrieve the dedicated IP set with the provided ID.

    Args:
        dedicated_ip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DedicatedIP | Error]
    """

    kwargs = _get_kwargs(
        dedicated_ip_id=dedicated_ip_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dedicated_ip_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> DedicatedIP | Error | None:
    """Retrieve dedicated IP set

     Retrieve the dedicated IP set with the provided ID.

    Args:
        dedicated_ip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DedicatedIP | Error
    """

    return sync_detailed(
        dedicated_ip_id=dedicated_ip_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    dedicated_ip_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DedicatedIP | Error]:
    """Retrieve dedicated IP set

     Retrieve the dedicated IP set with the provided ID.

    Args:
        dedicated_ip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DedicatedIP | Error]
    """

    kwargs = _get_kwargs(
        dedicated_ip_id=dedicated_ip_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dedicated_ip_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> DedicatedIP | Error | None:
    """Retrieve dedicated IP set

     Retrieve the dedicated IP set with the provided ID.

    Args:
        dedicated_ip_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DedicatedIP | Error
    """

    return (
        await asyncio_detailed(
            dedicated_ip_id=dedicated_ip_id,
            client=client,
        )
    ).parsed
