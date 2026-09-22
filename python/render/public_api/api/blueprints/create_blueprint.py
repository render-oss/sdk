from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_blueprint_request import CreateBlueprintRequest
from ...models.create_blueprint_response import CreateBlueprintResponse
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateBlueprintRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/blueprints",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateBlueprintResponse, Error]]:
    if response.status_code == 200:
        response_200 = CreateBlueprintResponse.from_dict(response.json())

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
) -> Response[Union[CreateBlueprintResponse, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlueprintRequest,
) -> Response[Union[CreateBlueprintResponse, Error]]:
    """Create a new Blueprint

     Create a new Blueprint to configure infrastructure as code.
    See [Render Blueprints](https://render.com/docs/infrastructure-as-code) for more information.

    This endpoint finds an existing matching Blueprint or creates one, then creates
    a new Sync. A Blueprint matches when it has the same workspace, repository,
    branch, Blueprint file path, and existing-resource mode. The Blueprint name and
    auto-sync setting do not affect matching.

    A successful response means Render connected to the repository and read the
    Blueprint file. Review the returned Sync to see the resource changes the Blueprint
    would make.

    Args:
        body (CreateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBlueprintResponse, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlueprintRequest,
) -> Optional[Union[CreateBlueprintResponse, Error]]:
    """Create a new Blueprint

     Create a new Blueprint to configure infrastructure as code.
    See [Render Blueprints](https://render.com/docs/infrastructure-as-code) for more information.

    This endpoint finds an existing matching Blueprint or creates one, then creates
    a new Sync. A Blueprint matches when it has the same workspace, repository,
    branch, Blueprint file path, and existing-resource mode. The Blueprint name and
    auto-sync setting do not affect matching.

    A successful response means Render connected to the repository and read the
    Blueprint file. Review the returned Sync to see the resource changes the Blueprint
    would make.

    Args:
        body (CreateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBlueprintResponse, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlueprintRequest,
) -> Response[Union[CreateBlueprintResponse, Error]]:
    """Create a new Blueprint

     Create a new Blueprint to configure infrastructure as code.
    See [Render Blueprints](https://render.com/docs/infrastructure-as-code) for more information.

    This endpoint finds an existing matching Blueprint or creates one, then creates
    a new Sync. A Blueprint matches when it has the same workspace, repository,
    branch, Blueprint file path, and existing-resource mode. The Blueprint name and
    auto-sync setting do not affect matching.

    A successful response means Render connected to the repository and read the
    Blueprint file. Review the returned Sync to see the resource changes the Blueprint
    would make.

    Args:
        body (CreateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBlueprintResponse, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlueprintRequest,
) -> Optional[Union[CreateBlueprintResponse, Error]]:
    """Create a new Blueprint

     Create a new Blueprint to configure infrastructure as code.
    See [Render Blueprints](https://render.com/docs/infrastructure-as-code) for more information.

    This endpoint finds an existing matching Blueprint or creates one, then creates
    a new Sync. A Blueprint matches when it has the same workspace, repository,
    branch, Blueprint file path, and existing-resource mode. The Blueprint name and
    auto-sync setting do not affect matching.

    A successful response means Render connected to the repository and read the
    Blueprint file. Review the returned Sync to see the resource changes the Blueprint
    would make.

    Args:
        body (CreateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBlueprintResponse, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
