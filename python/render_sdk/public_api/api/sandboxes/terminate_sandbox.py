from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    sandbox_id: str,
    *,
    owner_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/terminate",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: str,
) -> Response[Union[Any, Error]]:
    """Terminate sandbox

     Terminate the sandbox with the provided ID. Idempotent: returns 204 from any
    state, including `terminated`. Terminating a `creating` sandbox cancels
    boot/setup immediately.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: str,
) -> Optional[Union[Any, Error]]:
    """Terminate sandbox

     Terminate the sandbox with the provided ID. Idempotent: returns 204 from any
    state, including `terminated`. Terminating a `creating` sandbox cancels
    boot/setup immediately.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: str,
) -> Response[Union[Any, Error]]:
    """Terminate sandbox

     Terminate the sandbox with the provided ID. Idempotent: returns 204 from any
    state, including `terminated`. Terminating a `creating` sandbox cancels
    boot/setup immediately.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: str,
) -> Optional[Union[Any, Error]]:
    """Terminate sandbox

     Terminate the sandbox with the provided ID. Idempotent: returns 204 from any
    state, including `terminated`. Terminating a `creating` sandbox cancels
    boot/setup immediately.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            owner_id=owner_id,
        )
    ).parsed
