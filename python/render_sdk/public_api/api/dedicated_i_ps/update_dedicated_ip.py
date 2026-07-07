from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dedicated_ip import DedicatedIP
from ...models.dedicated_ippatch import DedicatedIPPATCH
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    dedicated_ip_id: str,
    *,
    body: DedicatedIPPATCH,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/dedicated-ips/{dedicated_ip_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DedicatedIP, Error]]:
    if response.status_code == 200:
        response_200 = DedicatedIP.from_dict(response.json())

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

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DedicatedIP, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dedicated_ip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPATCH,
) -> Response[Union[DedicatedIP, Error]]:
    """Update dedicated IP set

     Update the dedicated IP set with the provided ID. All fields are optional. Omitted fields are left
    unchanged. To switch from environment-scoped to workspace-scoped, provide `environmentIds: []`.

    Args:
        dedicated_ip_id (str):
        body (DedicatedIPPATCH): Input for updating a dedicated IP set. All fields are optional.
            Omitted fields are left unchanged. Provide `environmentIds: []` to switch from
            environment-scoped to workspace-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DedicatedIP, Error]]
    """

    kwargs = _get_kwargs(
        dedicated_ip_id=dedicated_ip_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dedicated_ip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPATCH,
) -> Optional[Union[DedicatedIP, Error]]:
    """Update dedicated IP set

     Update the dedicated IP set with the provided ID. All fields are optional. Omitted fields are left
    unchanged. To switch from environment-scoped to workspace-scoped, provide `environmentIds: []`.

    Args:
        dedicated_ip_id (str):
        body (DedicatedIPPATCH): Input for updating a dedicated IP set. All fields are optional.
            Omitted fields are left unchanged. Provide `environmentIds: []` to switch from
            environment-scoped to workspace-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DedicatedIP, Error]
    """

    return sync_detailed(
        dedicated_ip_id=dedicated_ip_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    dedicated_ip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPATCH,
) -> Response[Union[DedicatedIP, Error]]:
    """Update dedicated IP set

     Update the dedicated IP set with the provided ID. All fields are optional. Omitted fields are left
    unchanged. To switch from environment-scoped to workspace-scoped, provide `environmentIds: []`.

    Args:
        dedicated_ip_id (str):
        body (DedicatedIPPATCH): Input for updating a dedicated IP set. All fields are optional.
            Omitted fields are left unchanged. Provide `environmentIds: []` to switch from
            environment-scoped to workspace-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DedicatedIP, Error]]
    """

    kwargs = _get_kwargs(
        dedicated_ip_id=dedicated_ip_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dedicated_ip_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPATCH,
) -> Optional[Union[DedicatedIP, Error]]:
    """Update dedicated IP set

     Update the dedicated IP set with the provided ID. All fields are optional. Omitted fields are left
    unchanged. To switch from environment-scoped to workspace-scoped, provide `environmentIds: []`.

    Args:
        dedicated_ip_id (str):
        body (DedicatedIPPATCH): Input for updating a dedicated IP set. All fields are optional.
            Omitted fields are left unchanged. Provide `environmentIds: []` to switch from
            environment-scoped to workspace-scoped.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DedicatedIP, Error]
    """

    return (
        await asyncio_detailed(
            dedicated_ip_id=dedicated_ip_id,
            client=client,
            body=body,
        )
    ).parsed
