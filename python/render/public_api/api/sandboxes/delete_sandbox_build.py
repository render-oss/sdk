from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
    build_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/sandbox-groups/{sandbox_group_id}/builds/{build_id}".format(
            sandbox_group_id=quote(str(sandbox_group_id), safe=""),
            build_id=quote(str(build_id), safe=""),
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

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    build_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Delete sandbox build

     Delete a build of a sandbox image. The build no longer appears in lists and cannot be retrieved or
    used to create sandboxes, including by image name. Repeated requests to delete the build return HTTP
    204.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        build_id (str): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        build_id=build_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    build_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Delete sandbox build

     Delete a build of a sandbox image. The build no longer appears in lists and cannot be retrieved or
    used to create sandboxes, including by image name. Repeated requests to delete the build return HTTP
    204.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        build_id (str): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        build_id=build_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    build_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Delete sandbox build

     Delete a build of a sandbox image. The build no longer appears in lists and cannot be retrieved or
    used to create sandboxes, including by image name. Repeated requests to delete the build return HTTP
    204.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        build_id (str): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        build_id=build_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    build_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Delete sandbox build

     Delete a build of a sandbox image. The build no longer appears in lists and cannot be retrieved or
    used to create sandboxes, including by image name. Repeated requests to delete the build return HTTP
    204.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        build_id (str): The ID of the sandbox build. Example: sbb-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            build_id=build_id,
            client=client,
        )
    ).parsed
