from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.patch_route_response_200 import PatchRouteResponse200
from ...models.route_patch import RoutePatch
from ...types import Response


def _get_kwargs(
    service_id: str,
    *,
    body: RoutePatch,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/services/{service_id}/routes",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, PatchRouteResponse200]]:
    if response.status_code == 200:
        response_200 = PatchRouteResponse200.from_dict(response.json())

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
) -> Response[Union[Error, PatchRouteResponse200]]:
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
    body: RoutePatch,
) -> Response[Union[Error, PatchRouteResponse200]]:
    """Update redirect/rewrite rule priority

     Update the priority for a particular redirect/rewrite rule.

    To apply redirect/rewrite rules to an incoming request, Render starts from the rule with priority
    `0` and applies the first encountered rule that matches the request's path (if any).

    Render increments the priority of other rules by `1` as necessary to make space for the updated
    rule.

    Args:
        service_id (str):
        body (RoutePatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PatchRouteResponse200]]
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
    body: RoutePatch,
) -> Optional[Union[Error, PatchRouteResponse200]]:
    """Update redirect/rewrite rule priority

     Update the priority for a particular redirect/rewrite rule.

    To apply redirect/rewrite rules to an incoming request, Render starts from the rule with priority
    `0` and applies the first encountered rule that matches the request's path (if any).

    Render increments the priority of other rules by `1` as necessary to make space for the updated
    rule.

    Args:
        service_id (str):
        body (RoutePatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PatchRouteResponse200]
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
    body: RoutePatch,
) -> Response[Union[Error, PatchRouteResponse200]]:
    """Update redirect/rewrite rule priority

     Update the priority for a particular redirect/rewrite rule.

    To apply redirect/rewrite rules to an incoming request, Render starts from the rule with priority
    `0` and applies the first encountered rule that matches the request's path (if any).

    Render increments the priority of other rules by `1` as necessary to make space for the updated
    rule.

    Args:
        service_id (str):
        body (RoutePatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, PatchRouteResponse200]]
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
    body: RoutePatch,
) -> Optional[Union[Error, PatchRouteResponse200]]:
    """Update redirect/rewrite rule priority

     Update the priority for a particular redirect/rewrite rule.

    To apply redirect/rewrite rules to an incoming request, Render starts from the rule with priority
    `0` and applies the first encountered rule that matches the request's path (if any).

    Render increments the priority of other rules by `1` as necessary to make space for the updated
    rule.

    Args:
        service_id (str):
        body (RoutePatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, PatchRouteResponse200]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
