from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.env_group import EnvGroup
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    build_source_id: str,
    env_group_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/build-sources/{build_source_id}/env-groups/{env_group_id}".format(
            build_source_id=quote(str(build_source_id), safe=""),
            env_group_id=quote(str(env_group_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> EnvGroup | Error | None:
    if response.status_code == 200:
        response_200 = EnvGroup.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[EnvGroup | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    build_source_id: str,
    env_group_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[EnvGroup | Error]:
    """Link environment group

     Link a particular environment group to a particular build source.

    The build source will have access to the environment variables and secret files in the group at
    build time.

    Args:
        build_source_id (str):
        env_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvGroup | Error]
    """

    kwargs = _get_kwargs(
        build_source_id=build_source_id,
        env_group_id=env_group_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    build_source_id: str,
    env_group_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> EnvGroup | Error | None:
    """Link environment group

     Link a particular environment group to a particular build source.

    The build source will have access to the environment variables and secret files in the group at
    build time.

    Args:
        build_source_id (str):
        env_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvGroup | Error
    """

    return sync_detailed(
        build_source_id=build_source_id,
        env_group_id=env_group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    build_source_id: str,
    env_group_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[EnvGroup | Error]:
    """Link environment group

     Link a particular environment group to a particular build source.

    The build source will have access to the environment variables and secret files in the group at
    build time.

    Args:
        build_source_id (str):
        env_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvGroup | Error]
    """

    kwargs = _get_kwargs(
        build_source_id=build_source_id,
        env_group_id=env_group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    build_source_id: str,
    env_group_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> EnvGroup | Error | None:
    """Link environment group

     Link a particular environment group to a particular build source.

    The build source will have access to the environment variables and secret files in the group at
    build time.

    Args:
        build_source_id (str):
        env_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvGroup | Error
    """

    return (
        await asyncio_detailed(
            build_source_id=build_source_id,
            env_group_id=env_group_id,
            client=client,
        )
    ).parsed
