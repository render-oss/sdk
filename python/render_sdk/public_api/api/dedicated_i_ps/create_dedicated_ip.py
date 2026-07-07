from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dedicated_ip import DedicatedIP
from ...models.dedicated_ippost import DedicatedIPPOST
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: DedicatedIPPOST,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/dedicated-ips",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DedicatedIP, Error]]:
    if response.status_code == 201:
        response_201 = DedicatedIP.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

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
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPOST,
) -> Response[Union[DedicatedIP, Error]]:
    """Create dedicated IP set

     Create a dedicated IP set. Provisioning an IP set is asynchronous. The response returns immediately
    with `status: CREATING` and `ips: []`. When provisioning completes, status changes to `RUNNING` and
    `ips` contains your assigned addresses.

    If `environmentIds` is omitted or empty, this IP set applies to all services in the workspace in the
    selected region. Otherwise, it applies only to services in the listed environments in that region.

    Args:
        body (DedicatedIPPOST): Input for creating a dedicated IP set.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DedicatedIP, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPOST,
) -> Optional[Union[DedicatedIP, Error]]:
    """Create dedicated IP set

     Create a dedicated IP set. Provisioning an IP set is asynchronous. The response returns immediately
    with `status: CREATING` and `ips: []`. When provisioning completes, status changes to `RUNNING` and
    `ips` contains your assigned addresses.

    If `environmentIds` is omitted or empty, this IP set applies to all services in the workspace in the
    selected region. Otherwise, it applies only to services in the listed environments in that region.

    Args:
        body (DedicatedIPPOST): Input for creating a dedicated IP set.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DedicatedIP, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPOST,
) -> Response[Union[DedicatedIP, Error]]:
    """Create dedicated IP set

     Create a dedicated IP set. Provisioning an IP set is asynchronous. The response returns immediately
    with `status: CREATING` and `ips: []`. When provisioning completes, status changes to `RUNNING` and
    `ips` contains your assigned addresses.

    If `environmentIds` is omitted or empty, this IP set applies to all services in the workspace in the
    selected region. Otherwise, it applies only to services in the listed environments in that region.

    Args:
        body (DedicatedIPPOST): Input for creating a dedicated IP set.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DedicatedIP, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: DedicatedIPPOST,
) -> Optional[Union[DedicatedIP, Error]]:
    """Create dedicated IP set

     Create a dedicated IP set. Provisioning an IP set is asynchronous. The response returns immediately
    with `status: CREATING` and `ips: []`. When provisioning completes, status changes to `RUNNING` and
    `ips` contains your assigned addresses.

    If `environmentIds` is omitted or empty, this IP set applies to all services in the workspace in the
    selected region. Otherwise, it applies only to services in the listed environments in that region.

    Args:
        body (DedicatedIPPOST): Input for creating a dedicated IP set.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DedicatedIP, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
