from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_credential import SandboxCredential
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandbox-groups/{sandbox_group_id}/credentials",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["SandboxCredential"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SandboxCredential.from_dict(response_200_item_data)

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
) -> Response[Union[Error, list["SandboxCredential"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, list["SandboxCredential"]]]:
    """List sandbox group credentials

     Returns all credentials in the group, sorted by caller-supplied ID.
    Secret values are never returned, including to admins.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxCredential']]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, list["SandboxCredential"]]]:
    """List sandbox group credentials

     Returns all credentials in the group, sorted by caller-supplied ID.
    Secret values are never returned, including to admins.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxCredential']]
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, list["SandboxCredential"]]]:
    """List sandbox group credentials

     Returns all credentials in the group, sorted by caller-supplied ID.
    Secret values are never returned, including to admins.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxCredential']]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, list["SandboxCredential"]]]:
    """List sandbox group credentials

     Returns all credentials in the group, sorted by caller-supplied ID.
    Secret values are never returned, including to admins.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxCredential']]
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            client=client,
        )
    ).parsed
