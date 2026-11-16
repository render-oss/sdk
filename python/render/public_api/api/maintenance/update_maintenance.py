from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.maintenance_run_patch import MaintenanceRunPATCH
from ...types import Response


def _get_kwargs(
    maintenance_run_id: str,
    *,
    body: MaintenanceRunPATCH,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/maintenance/{maintenance_run_id}".format(
            maintenance_run_id=quote(str(maintenance_run_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Any | Error | None:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    maintenance_run_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MaintenanceRunPATCH,
) -> Response[Any | Error]:
    """Update maintenance run

     Update the maintenance run with the provided ID.

    Updates from this endpoint are asynchronous. To check your update's status, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    Args:
        maintenance_run_id (str):  Example: mrn-cph1rs3idesc73a2b2mg.
        body (MaintenanceRunPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        maintenance_run_id=maintenance_run_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    maintenance_run_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MaintenanceRunPATCH,
) -> Any | Error | None:
    """Update maintenance run

     Update the maintenance run with the provided ID.

    Updates from this endpoint are asynchronous. To check your update's status, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    Args:
        maintenance_run_id (str):  Example: mrn-cph1rs3idesc73a2b2mg.
        body (MaintenanceRunPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        maintenance_run_id=maintenance_run_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    maintenance_run_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MaintenanceRunPATCH,
) -> Response[Any | Error]:
    """Update maintenance run

     Update the maintenance run with the provided ID.

    Updates from this endpoint are asynchronous. To check your update's status, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    Args:
        maintenance_run_id (str):  Example: mrn-cph1rs3idesc73a2b2mg.
        body (MaintenanceRunPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        maintenance_run_id=maintenance_run_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    maintenance_run_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MaintenanceRunPATCH,
) -> Any | Error | None:
    """Update maintenance run

     Update the maintenance run with the provided ID.

    Updates from this endpoint are asynchronous. To check your update's status, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    Args:
        maintenance_run_id (str):  Example: mrn-cph1rs3idesc73a2b2mg.
        body (MaintenanceRunPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            maintenance_run_id=maintenance_run_id,
            client=client,
            body=body,
        )
    ).parsed
