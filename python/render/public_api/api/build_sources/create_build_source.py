from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.build_source import BuildSource
from ...models.build_source_post_input import BuildSourcePOSTInput
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: BuildSourcePOSTInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/build-sources",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> BuildSource | Error | None:
    if response.status_code == 201:
        response_201 = BuildSource.from_dict(response.json())

        return response_201

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[BuildSource | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePOSTInput,
) -> Response[BuildSource | Error]:
    """Create a build source

     Create a build source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the build source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the build source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    `envVars`, `secretFiles`, and `envGroupIds` set the build-time
    environment and are only valid for `git` sources; the request fails
    if any are provided with `image`.

    Args:
        body (BuildSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuildSource | Error]
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
    client: AuthenticatedClient | Client,
    body: BuildSourcePOSTInput,
) -> BuildSource | Error | None:
    """Create a build source

     Create a build source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the build source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the build source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    `envVars`, `secretFiles`, and `envGroupIds` set the build-time
    environment and are only valid for `git` sources; the request fails
    if any are provided with `image`.

    Args:
        body (BuildSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuildSource | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePOSTInput,
) -> Response[BuildSource | Error]:
    """Create a build source

     Create a build source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the build source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the build source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    `envVars`, `secretFiles`, and `envGroupIds` set the build-time
    environment and are only valid for `git` sources; the request fails
    if any are provided with `image`.

    Args:
        body (BuildSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuildSource | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePOSTInput,
) -> BuildSource | Error | None:
    """Create a build source

     Create a build source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the build source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the build source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    `envVars`, `secretFiles`, and `envGroupIds` set the build-time
    environment and are only valid for `git` sources; the request fails
    if any are provided with `image`.

    Args:
        body (BuildSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuildSource | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
