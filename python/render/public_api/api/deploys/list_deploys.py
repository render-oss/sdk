import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deploy_status import DeployStatus
from ...models.deploy_with_cursor import DeployWithCursor
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    status: list[DeployStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_status: list[str] | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    json_created_before: str | Unset = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    json_updated_before: str | Unset = UNSET
    if not isinstance(updated_before, Unset):
        json_updated_before = updated_before.isoformat()
    params["updatedBefore"] = json_updated_before

    json_updated_after: str | Unset = UNSET
    if not isinstance(updated_after, Unset):
        json_updated_after = updated_after.isoformat()
    params["updatedAfter"] = json_updated_after

    json_finished_before: str | Unset = UNSET
    if not isinstance(finished_before, Unset):
        json_finished_before = finished_before.isoformat()
    params["finishedBefore"] = json_finished_before

    json_finished_after: str | Unset = UNSET
    if not isinstance(finished_after, Unset):
        json_finished_after = finished_after.isoformat()
    params["finishedAfter"] = json_finished_after

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services/{service_id}/deploys".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[DeployWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemasdeploy_list_item_data in _response_200:
            componentsschemasdeploy_list_item = DeployWithCursor.from_dict(componentsschemasdeploy_list_item_data)

            response_200.append(componentsschemasdeploy_list_item)

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
) -> Response[Error | list[DeployWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    status: list[DeployStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[DeployWithCursor]]:
    """List deploys

     List deploys matching the provided filters. If no filters are provided, all deploys for the service
    are returned.

    Args:
        service_id (str):
        status (list[DeployStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[DeployWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        status=status,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        finished_before=finished_before,
        finished_after=finished_after,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    status: list[DeployStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[DeployWithCursor] | None:
    """List deploys

     List deploys matching the provided filters. If no filters are provided, all deploys for the service
    are returned.

    Args:
        service_id (str):
        status (list[DeployStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[DeployWithCursor]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        status=status,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        finished_before=finished_before,
        finished_after=finished_after,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    status: list[DeployStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[DeployWithCursor]]:
    """List deploys

     List deploys matching the provided filters. If no filters are provided, all deploys for the service
    are returned.

    Args:
        service_id (str):
        status (list[DeployStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[DeployWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        status=status,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        finished_before=finished_before,
        finished_after=finished_after,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    status: list[DeployStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[DeployWithCursor] | None:
    """List deploys

     List deploys matching the provided filters. If no filters are provided, all deploys for the service
    are returned.

    Args:
        service_id (str):
        status (list[DeployStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[DeployWithCursor]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            status=status,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            finished_before=finished_before,
            finished_after=finished_after,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
