import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_with_cursor import AuditLogWithCursor
from ...models.error import Error
from ...models.log_direction import LogDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    direction: Union[Unset, LogDirection] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_time: Union[Unset, str] = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time

    json_end_time: Union[Unset, str] = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time

    json_direction: Union[Unset, str] = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value

    params["direction"] = json_direction

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/organizations/{org_id}/audit-logs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["AuditLogWithCursor"]]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["AuditLogWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    direction: Union[Unset, LogDirection] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["AuditLogWithCursor"]]]:
    """List organization audit logs

     Retrieve audit logs for a specific organization with optional filtering and pagination.

    Args:
        org_id (str):
        start_time (Union[Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00Z.
        end_time (Union[Unset, datetime.datetime]):  Example: 2023-12-31T23:59:59Z.
        direction (Union[Unset, LogDirection]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['AuditLogWithCursor']]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
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
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    direction: Union[Unset, LogDirection] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["AuditLogWithCursor"]]]:
    """List organization audit logs

     Retrieve audit logs for a specific organization with optional filtering and pagination.

    Args:
        org_id (str):
        start_time (Union[Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00Z.
        end_time (Union[Unset, datetime.datetime]):  Example: 2023-12-31T23:59:59Z.
        direction (Union[Unset, LogDirection]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['AuditLogWithCursor']]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    direction: Union[Unset, LogDirection] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["AuditLogWithCursor"]]]:
    """List organization audit logs

     Retrieve audit logs for a specific organization with optional filtering and pagination.

    Args:
        org_id (str):
        start_time (Union[Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00Z.
        end_time (Union[Unset, datetime.datetime]):  Example: 2023-12-31T23:59:59Z.
        direction (Union[Unset, LogDirection]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['AuditLogWithCursor']]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    direction: Union[Unset, LogDirection] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["AuditLogWithCursor"]]]:
    """List organization audit logs

     Retrieve audit logs for a specific organization with optional filtering and pagination.

    Args:
        org_id (str):
        start_time (Union[Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00Z.
        end_time (Union[Unset, datetime.datetime]):  Example: 2023-12-31T23:59:59Z.
        direction (Union[Unset, LogDirection]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['AuditLogWithCursor']]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            start_time=start_time,
            end_time=end_time,
            direction=direction,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
