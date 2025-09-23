from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.maintenance_run_with_resource import MaintenanceRunWithResource
from ...types import Response


def _get_kwargs(
    maintenance_run_param: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/maintenance/{maintenance_run_param}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, MaintenanceRunWithResource]]:
    if response.status_code == 200:
        response_200 = MaintenanceRunWithResource.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Union[Error, MaintenanceRunWithResource]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, MaintenanceRunWithResource]]:
    """Retrieve maintenance run

     Retrieve the maintenance run with the provided ID.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MaintenanceRunWithResource]]
    """

    kwargs = _get_kwargs(
        maintenance_run_param=maintenance_run_param,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, MaintenanceRunWithResource]]:
    """Retrieve maintenance run

     Retrieve the maintenance run with the provided ID.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MaintenanceRunWithResource]
    """

    return sync_detailed(
        maintenance_run_param=maintenance_run_param,
        client=client,
    ).parsed


async def asyncio_detailed(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, MaintenanceRunWithResource]]:
    """Retrieve maintenance run

     Retrieve the maintenance run with the provided ID.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, MaintenanceRunWithResource]]
    """

    kwargs = _get_kwargs(
        maintenance_run_param=maintenance_run_param,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, MaintenanceRunWithResource]]:
    """Retrieve maintenance run

     Retrieve the maintenance run with the provided ID.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, MaintenanceRunWithResource]
    """

    return (
        await asyncio_detailed(
            maintenance_run_param=maintenance_run_param,
            client=client,
        )
    ).parsed
