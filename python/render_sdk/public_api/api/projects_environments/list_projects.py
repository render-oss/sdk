import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project_with_cursor import ProjectWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, list[str]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    json_updated_before: Union[Unset, str] = UNSET
    if not isinstance(updated_before, Unset):
        json_updated_before = updated_before.isoformat()
    params["updatedBefore"] = json_updated_before

    json_updated_after: Union[Unset, str] = UNSET
    if not isinstance(updated_after, Unset):
        json_updated_after = updated_after.isoformat()
    params["updatedAfter"] = json_updated_after

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["ProjectWithCursor"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectWithCursor.from_dict(response_200_item_data)

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["ProjectWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["ProjectWithCursor"]]]:
    """List projects

     List projects matching the provided filters. If no filters are provided, all projects are returned.

    Args:
        name (Union[Unset, list[str]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['ProjectWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["ProjectWithCursor"]]]:
    """List projects

     List projects matching the provided filters. If no filters are provided, all projects are returned.

    Args:
        name (Union[Unset, list[str]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['ProjectWithCursor']]
    """

    return sync_detailed(
        client=client,
        name=name,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["ProjectWithCursor"]]]:
    """List projects

     List projects matching the provided filters. If no filters are provided, all projects are returned.

    Args:
        name (Union[Unset, list[str]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['ProjectWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["ProjectWithCursor"]]]:
    """List projects

     List projects matching the provided filters. If no filters are provided, all projects are returned.

    Args:
        name (Union[Unset, list[str]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['ProjectWithCursor']]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            owner_id=owner_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
