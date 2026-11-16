import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_with_cursor import AuditLogWithCursor
from ...models.error import Error
from ...models.log_direction import LogDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    owner_id: str,
    *,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_time: str | Unset = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time

    json_end_time: str | Unset = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time

    json_direction: str | Unset = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value

    params["direction"] = json_direction

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/owners/{owner_id}/audit-logs".format(
            owner_id=quote(str(owner_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[AuditLogWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuditLogWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[AuditLogWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[AuditLogWithCursor]]:
    """List workspace audit logs

     Retrieve audit logs for a specific workspace with optional filtering and pagination.

    Args:
        owner_id (str):
        start_time (datetime.datetime | Unset):  Example: 2023-01-01T00:00:00Z.
        end_time (datetime.datetime | Unset):  Example: 2023-12-31T23:59:59Z.
        direction (LogDirection | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[AuditLogWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[AuditLogWithCursor] | None:
    """List workspace audit logs

     Retrieve audit logs for a specific workspace with optional filtering and pagination.

    Args:
        owner_id (str):
        start_time (datetime.datetime | Unset):  Example: 2023-01-01T00:00:00Z.
        end_time (datetime.datetime | Unset):  Example: 2023-12-31T23:59:59Z.
        direction (LogDirection | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[AuditLogWithCursor]
    """

    return sync_detailed(
        owner_id=owner_id,
        client=client,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[AuditLogWithCursor]]:
    """List workspace audit logs

     Retrieve audit logs for a specific workspace with optional filtering and pagination.

    Args:
        owner_id (str):
        start_time (datetime.datetime | Unset):  Example: 2023-01-01T00:00:00Z.
        end_time (datetime.datetime | Unset):  Example: 2023-12-31T23:59:59Z.
        direction (LogDirection | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[AuditLogWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[AuditLogWithCursor] | None:
    """List workspace audit logs

     Retrieve audit logs for a specific workspace with optional filtering and pagination.

    Args:
        owner_id (str):
        start_time (datetime.datetime | Unset):  Example: 2023-01-01T00:00:00Z.
        end_time (datetime.datetime | Unset):  Example: 2023-12-31T23:59:59Z.
        direction (LogDirection | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[AuditLogWithCursor]
    """

    return (
        await asyncio_detailed(
            owner_id=owner_id,
            client=client,
            start_time=start_time,
            end_time=end_time,
            direction=direction,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
