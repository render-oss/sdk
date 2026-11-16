import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.job_status import JobStatus
from ...models.job_with_cursor import JobWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    status: list[JobStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    started_before: datetime.datetime | Unset = UNSET,
    started_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

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

    json_started_before: str | Unset = UNSET
    if not isinstance(started_before, Unset):
        json_started_before = started_before.isoformat()
    params["startedBefore"] = json_started_before

    json_started_after: str | Unset = UNSET
    if not isinstance(started_after, Unset):
        json_started_after = started_after.isoformat()
    params["startedAfter"] = json_started_after

    json_finished_before: str | Unset = UNSET
    if not isinstance(finished_before, Unset):
        json_finished_before = finished_before.isoformat()
    params["finishedBefore"] = json_finished_before

    json_finished_after: str | Unset = UNSET
    if not isinstance(finished_after, Unset):
        json_finished_after = finished_after.isoformat()
    params["finishedAfter"] = json_finished_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services/{service_id}/jobs".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[JobWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = JobWithCursor.from_dict(response_200_item_data)

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
) -> Response[Error | list[JobWithCursor]]:
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
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    status: list[JobStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    started_before: datetime.datetime | Unset = UNSET,
    started_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
) -> Response[Error | list[JobWithCursor]]:
    """List jobs

     List jobs for the provided service that match the provided filters. If no filters are provided, all
    jobs for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        status (list[JobStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        started_before (datetime.datetime | Unset):
        started_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[JobWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        cursor=cursor,
        limit=limit,
        status=status,
        created_before=created_before,
        created_after=created_after,
        started_before=started_before,
        started_after=started_after,
        finished_before=finished_before,
        finished_after=finished_after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    status: list[JobStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    started_before: datetime.datetime | Unset = UNSET,
    started_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
) -> Error | list[JobWithCursor] | None:
    """List jobs

     List jobs for the provided service that match the provided filters. If no filters are provided, all
    jobs for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        status (list[JobStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        started_before (datetime.datetime | Unset):
        started_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[JobWithCursor]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        cursor=cursor,
        limit=limit,
        status=status,
        created_before=created_before,
        created_after=created_after,
        started_before=started_before,
        started_after=started_after,
        finished_before=finished_before,
        finished_after=finished_after,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    status: list[JobStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    started_before: datetime.datetime | Unset = UNSET,
    started_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
) -> Response[Error | list[JobWithCursor]]:
    """List jobs

     List jobs for the provided service that match the provided filters. If no filters are provided, all
    jobs for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        status (list[JobStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        started_before (datetime.datetime | Unset):
        started_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[JobWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        cursor=cursor,
        limit=limit,
        status=status,
        created_before=created_before,
        created_after=created_after,
        started_before=started_before,
        started_after=started_after,
        finished_before=finished_before,
        finished_after=finished_after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    status: list[JobStatus] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    started_before: datetime.datetime | Unset = UNSET,
    started_after: datetime.datetime | Unset = UNSET,
    finished_before: datetime.datetime | Unset = UNSET,
    finished_after: datetime.datetime | Unset = UNSET,
) -> Error | list[JobWithCursor] | None:
    """List jobs

     List jobs for the provided service that match the provided filters. If no filters are provided, all
    jobs for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        status (list[JobStatus] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        started_before (datetime.datetime | Unset):
        started_after (datetime.datetime | Unset):
        finished_before (datetime.datetime | Unset):
        finished_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[JobWithCursor]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            cursor=cursor,
            limit=limit,
            status=status,
            created_before=created_before,
            created_after=created_after,
            started_before=started_before,
            started_after=started_after,
            finished_before=finished_before,
            finished_after=finished_after,
        )
    ).parsed
