from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_routes_type_item import ListRoutesTypeItem
from ...models.route_with_cursor import RouteWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    type_: Union[Unset, list[ListRoutesTypeItem]] = UNSET,
    source: Union[Unset, list[str]] = UNSET,
    destination: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_type_: Union[Unset, list[str]] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = []
        for type_item_data in type_:
            type_item = type_item_data.value
            json_type_.append(type_item)

    params["type"] = json_type_

    json_source: Union[Unset, list[str]] = UNSET
    if not isinstance(source, Unset):
        json_source = source

    params["source"] = json_source

    json_destination: Union[Unset, list[str]] = UNSET
    if not isinstance(destination, Unset):
        json_destination = destination

    params["destination"] = json_destination

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/services/{service_id}/routes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["RouteWithCursor"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RouteWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["RouteWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, list[ListRoutesTypeItem]] = UNSET,
    source: Union[Unset, list[str]] = UNSET,
    destination: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["RouteWithCursor"]]]:
    """List redirect/rewrite rules

     List a particular service's redirect/rewrite rules that match the provided filters. If no filters
    are provided, all rules for the service are returned.

    Args:
        service_id (str):
        type_ (Union[Unset, list[ListRoutesTypeItem]]):
        source (Union[Unset, list[str]]):
        destination (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['RouteWithCursor']]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        type_=type_,
        source=source,
        destination=destination,
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
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, list[ListRoutesTypeItem]] = UNSET,
    source: Union[Unset, list[str]] = UNSET,
    destination: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["RouteWithCursor"]]]:
    """List redirect/rewrite rules

     List a particular service's redirect/rewrite rules that match the provided filters. If no filters
    are provided, all rules for the service are returned.

    Args:
        service_id (str):
        type_ (Union[Unset, list[ListRoutesTypeItem]]):
        source (Union[Unset, list[str]]):
        destination (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['RouteWithCursor']]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        type_=type_,
        source=source,
        destination=destination,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, list[ListRoutesTypeItem]] = UNSET,
    source: Union[Unset, list[str]] = UNSET,
    destination: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["RouteWithCursor"]]]:
    """List redirect/rewrite rules

     List a particular service's redirect/rewrite rules that match the provided filters. If no filters
    are provided, all rules for the service are returned.

    Args:
        service_id (str):
        type_ (Union[Unset, list[ListRoutesTypeItem]]):
        source (Union[Unset, list[str]]):
        destination (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['RouteWithCursor']]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        type_=type_,
        source=source,
        destination=destination,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, list[ListRoutesTypeItem]] = UNSET,
    source: Union[Unset, list[str]] = UNSET,
    destination: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["RouteWithCursor"]]]:
    """List redirect/rewrite rules

     List a particular service's redirect/rewrite rules that match the provided filters. If no filters
    are provided, all rules for the service are returned.

    Args:
        service_id (str):
        type_ (Union[Unset, list[ListRoutesTypeItem]]):
        source (Union[Unset, list[str]]):
        destination (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['RouteWithCursor']]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            type_=type_,
            source=source,
            destination=destination,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
