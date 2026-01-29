from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.validate_blueprint_request import ValidateBlueprintRequest
from ...models.validate_blueprint_response import ValidateBlueprintResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ValidateBlueprintRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/blueprints/validate",
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, ValidateBlueprintResponse]]:
    if response.status_code == 200:
        response_200 = ValidateBlueprintResponse.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ValidateBlueprintResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ValidateBlueprintRequest,
) -> Response[Union[Error, ValidateBlueprintResponse]]:
    """Validate Blueprint

     Validate a `render.yaml` Blueprint file without creating or modifying any resources. This endpoint
    checks the syntax and structure of the Blueprint, validates that all required fields are present,
    and returns a plan indicating the resources that would be created.

    Requests to this endpoint use `Content-Type: multipart/form-data`. The provided Blueprint file
    cannot exceed 10MB in size.

    Args:
        body (ValidateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ValidateBlueprintResponse]]
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
    body: ValidateBlueprintRequest,
) -> Optional[Union[Error, ValidateBlueprintResponse]]:
    """Validate Blueprint

     Validate a `render.yaml` Blueprint file without creating or modifying any resources. This endpoint
    checks the syntax and structure of the Blueprint, validates that all required fields are present,
    and returns a plan indicating the resources that would be created.

    Requests to this endpoint use `Content-Type: multipart/form-data`. The provided Blueprint file
    cannot exceed 10MB in size.

    Args:
        body (ValidateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ValidateBlueprintResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ValidateBlueprintRequest,
) -> Response[Union[Error, ValidateBlueprintResponse]]:
    """Validate Blueprint

     Validate a `render.yaml` Blueprint file without creating or modifying any resources. This endpoint
    checks the syntax and structure of the Blueprint, validates that all required fields are present,
    and returns a plan indicating the resources that would be created.

    Requests to this endpoint use `Content-Type: multipart/form-data`. The provided Blueprint file
    cannot exceed 10MB in size.

    Args:
        body (ValidateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ValidateBlueprintResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ValidateBlueprintRequest,
) -> Optional[Union[Error, ValidateBlueprintResponse]]:
    """Validate Blueprint

     Validate a `render.yaml` Blueprint file without creating or modifying any resources. This endpoint
    checks the syntax and structure of the Blueprint, validates that all required fields are present,
    and returns a plan indicating the resources that would be created.

    Requests to this endpoint use `Content-Type: multipart/form-data`. The provided Blueprint file
    cannot exceed 10MB in size.

    Args:
        body (ValidateBlueprintRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ValidateBlueprintResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
