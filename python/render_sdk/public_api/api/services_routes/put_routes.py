from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.route import Route
from ...models.route_put import RoutePut
from ...types import Response


def _get_kwargs(
    service_id: str,
    *,
    body: list["RoutePut"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/services/{service_id}/routes",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["Route"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Route.from_dict(response_200_item_data)

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
) -> Response[Union[Error, list["Route"]]]:
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
    body: list["RoutePut"],
) -> Response[Union[Error, list["Route"]]]:
    """Update redirect/rewrite rules

     Replace all redirect/rewrite rules for a particular service with the provided list.

    **This deletes all existing redirect/rewrite rules for the service that aren't included in the
    request.**

    Rule priority is assigned according to list order (the first rule in the list has the highest
    priority).

    Args:
        service_id (str):
        body (list['RoutePut']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['Route']]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["RoutePut"],
) -> Optional[Union[Error, list["Route"]]]:
    """Update redirect/rewrite rules

     Replace all redirect/rewrite rules for a particular service with the provided list.

    **This deletes all existing redirect/rewrite rules for the service that aren't included in the
    request.**

    Rule priority is assigned according to list order (the first rule in the list has the highest
    priority).

    Args:
        service_id (str):
        body (list['RoutePut']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['Route']]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["RoutePut"],
) -> Response[Union[Error, list["Route"]]]:
    """Update redirect/rewrite rules

     Replace all redirect/rewrite rules for a particular service with the provided list.

    **This deletes all existing redirect/rewrite rules for the service that aren't included in the
    request.**

    Rule priority is assigned according to list order (the first rule in the list has the highest
    priority).

    Args:
        service_id (str):
        body (list['RoutePut']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['Route']]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["RoutePut"],
) -> Optional[Union[Error, list["Route"]]]:
    """Update redirect/rewrite rules

     Replace all redirect/rewrite rules for a particular service with the provided list.

    **This deletes all existing redirect/rewrite rules for the service that aren't included in the
    request.**

    Rule priority is assigned according to list order (the first rule in the list has the highest
    priority).

    Args:
        service_id (str):
        body (list['RoutePut']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['Route']]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
