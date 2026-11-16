from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

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
        "url": "/blueprints/{blueprint_id}".format(
            blueprint_id=quote(str(blueprint_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Blueprint | Error | None:
    if response.status_code == 200:
        response_200 = Blueprint.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Blueprint | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    blueprint_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BlueprintPATCH,
) -> Response[Blueprint | Error]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Blueprint | Error]
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
    client: AuthenticatedClient | Client,
    body: BlueprintPATCH,
) -> Blueprint | Error | None:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Blueprint | Error
    """

    return sync_detailed(
        blueprint_id=blueprint_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    blueprint_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BlueprintPATCH,
) -> Response[Blueprint | Error]:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Blueprint | Error]
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
    client: AuthenticatedClient | Client,
    body: BlueprintPATCH,
) -> Blueprint | Error | None:
    """Update Blueprint

     Update the Blueprint with the provided ID.

    Args:
        blueprint_id (str):  Example: exs-cph1rs3idesc73a2b2mg.
        body (BlueprintPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Blueprint | Error
    """

    return (
        await asyncio_detailed(
            blueprint_id=blueprint_id,
            client=client,
            body=body,
        )
    ).parsed
