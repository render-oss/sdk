from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blueprint import Blueprint
from ...models.blueprint_patch import BlueprintPATCH
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    blueprint_id: str,
    *,
    body: BlueprintPATCH,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/blueprints/{blueprint_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Blueprint, Error]]:
    if response.status_code == 200:
        response_200 = Blueprint.from_dict(response.json())

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
) -> Response[Union[Blueprint, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    blueprint_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlueprintPATCH,
) -> Response[Union[Blueprint, Error]]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Blueprint, Error]]
    """

    kwargs = _get_kwargs(
        blueprint_id=blueprint_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    blueprint_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlueprintPATCH,
) -> Optional[Union[Blueprint, Error]]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Blueprint, Error]
    """

    return sync_detailed(
        blueprint_id=blueprint_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    blueprint_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlueprintPATCH,
) -> Response[Union[Blueprint, Error]]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Blueprint, Error]]
    """

    kwargs = _get_kwargs(
        blueprint_id=blueprint_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    blueprint_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlueprintPATCH,
) -> Optional[Union[Blueprint, Error]]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Blueprint, Error]
    """

    return (
        await asyncio_detailed(
            blueprint_id=blueprint_id,
            client=client,
            body=body,
        )
    ).parsed
