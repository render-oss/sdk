from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.postgres_parameter_overrides_wrapper import PostgresParameterOverridesWrapper
from ...models.postgres_put_parameter_overrides_result import PostgresPutParameterOverridesResult
from ...types import Response


def _get_kwargs(
    postgres_id: str,
    *,
    body: PostgresParameterOverridesWrapper,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/postgres/{postgres_id}/parameter-overrides".format(
            postgres_id=quote(str(postgres_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | PostgresPutParameterOverridesResult | None:
    if response.status_code == 200:
        response_200 = PostgresPutParameterOverridesResult.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[Error | PostgresPutParameterOverridesResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostgresParameterOverridesWrapper,
) -> Response[Error | PostgresPutParameterOverridesResult]:
    """Update Postgres parameter overrides

     Update the configuration parameter overrides applied to a Postgres instance by ID.

    Args:
        postgres_id (str):
        body (PostgresParameterOverridesWrapper):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PostgresPutParameterOverridesResult]
    """

    kwargs = _get_kwargs(
        postgres_id=postgres_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostgresParameterOverridesWrapper,
) -> Error | PostgresPutParameterOverridesResult | None:
    """Update Postgres parameter overrides

     Update the configuration parameter overrides applied to a Postgres instance by ID.

    Args:
        postgres_id (str):
        body (PostgresParameterOverridesWrapper):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PostgresPutParameterOverridesResult
    """

    return sync_detailed(
        postgres_id=postgres_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostgresParameterOverridesWrapper,
) -> Response[Error | PostgresPutParameterOverridesResult]:
    """Update Postgres parameter overrides

     Update the configuration parameter overrides applied to a Postgres instance by ID.

    Args:
        postgres_id (str):
        body (PostgresParameterOverridesWrapper):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PostgresPutParameterOverridesResult]
    """

    kwargs = _get_kwargs(
        postgres_id=postgres_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostgresParameterOverridesWrapper,
) -> Error | PostgresPutParameterOverridesResult | None:
    """Update Postgres parameter overrides

     Update the configuration parameter overrides applied to a Postgres instance by ID.

    Args:
        postgres_id (str):
        body (PostgresParameterOverridesWrapper):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PostgresPutParameterOverridesResult
    """

    return (
        await asyncio_detailed(
            postgres_id=postgres_id,
            client=client,
            body=body,
        )
    ).parsed
