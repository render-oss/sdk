from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.env_var import EnvVar
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    env_group_id: str,
    env_var_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/env-groups/{env_group_id}/env-vars/{env_var_key}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EnvVar, Error]]:
    if response.status_code == 200:
        response_200 = EnvVar.from_dict(response.json())

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


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[EnvVar, Error]]:
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
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[EnvVar, Error]]:
    """Retrieve environment variable

     Retrieve a particular environment variable in a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EnvVar, Error]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[EnvVar, Error]]:
    """Retrieve environment variable

     Retrieve a particular environment variable in a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EnvVar, Error]
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
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[EnvVar, Error]]:
    """Retrieve environment variable

     Retrieve a particular environment variable in a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EnvVar, Error]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[EnvVar, Error]]:
    """Retrieve environment variable

     Retrieve a particular environment variable in a particular environment group.

    Args:
        env_group_id (str):
        env_var_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EnvVar, Error]
    """

    return (
        await asyncio_detailed(
            env_group_id=env_group_id,
            env_var_key=env_var_key,
            client=client,
        )
    ).parsed
