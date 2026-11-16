from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.maintenance_run_with_resource import MaintenanceRunWithResource
from ...models.maintenance_state import MaintenanceState
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    resource_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    state: list[MaintenanceState] | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_resource_id: list[str] | Unset = UNSET
    if not isinstance(resource_id, Unset):
        json_resource_id = resource_id

    params["resourceId"] = json_resource_id

    json_owner_id: list[str] | Unset = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_state: list[str] | Unset = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/maintenance",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[MaintenanceRunWithResource] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MaintenanceRunWithResource.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | list[MaintenanceRunWithResource]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    resource_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    state: list[MaintenanceState] | Unset = UNSET,
) -> Response[Error | list[MaintenanceRunWithResource]]:
    """List maintenance runs

     List scheduled and/or recent maintenance runs for specified resources.

    Args:
        resource_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        state (list[MaintenanceState] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[MaintenanceRunWithResource]]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        owner_id=owner_id,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    resource_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    state: list[MaintenanceState] | Unset = UNSET,
) -> Error | list[MaintenanceRunWithResource] | None:
    """List maintenance runs

     List scheduled and/or recent maintenance runs for specified resources.

    Args:
        resource_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        state (list[MaintenanceState] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[MaintenanceRunWithResource]
    """

    return sync_detailed(
        client=client,
        resource_id=resource_id,
        owner_id=owner_id,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    resource_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    state: list[MaintenanceState] | Unset = UNSET,
) -> Response[Error | list[MaintenanceRunWithResource]]:
    """List maintenance runs

     List scheduled and/or recent maintenance runs for specified resources.

    Args:
        resource_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        state (list[MaintenanceState] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[MaintenanceRunWithResource]]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        owner_id=owner_id,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    resource_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    state: list[MaintenanceState] | Unset = UNSET,
) -> Error | list[MaintenanceRunWithResource] | None:
    """List maintenance runs

     List scheduled and/or recent maintenance runs for specified resources.

    Args:
        resource_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        state (list[MaintenanceState] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[MaintenanceRunWithResource]
    """

    return (
        await asyncio_detailed(
            client=client,
            resource_id=resource_id,
            owner_id=owner_id,
            state=state,
        )
    ).parsed
