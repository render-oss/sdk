from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    env_group_id: str,
    env_var_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/env-groups/{env_group_id}/secret-files/{env_var_key}".format(
            env_group_id=quote(str(env_group_id), safe=""),
            env_var_key=quote(str(env_var_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    env_group_id: str,
    env_var_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Remove secret file

     Remove a particular secret file from a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        env_group_id=env_group_id,
        env_var_key=env_var_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    env_group_id: str,
    env_var_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Remove secret file

     Remove a particular secret file from a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        env_group_id=env_group_id,
        env_var_key=env_var_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    env_group_id: str,
    env_var_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Remove secret file

     Remove a particular secret file from a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        env_group_id=env_group_id,
        env_var_key=env_var_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    env_group_id: str,
    env_var_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Remove secret file

     Remove a particular secret file from a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            env_group_id=env_group_id,
            env_var_key=env_var_key,
            client=client,
        )
    ).parsed
