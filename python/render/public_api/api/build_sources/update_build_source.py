from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.build_source import BuildSource
from ...models.build_source_patch_input import BuildSourcePATCHInput
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    build_source_id: str,
    *,
    body: BuildSourcePATCHInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/build-sources/{build_source_id}".format(
            build_source_id=quote(str(build_source_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> BuildSource | Error | None:
    if response.status_code == 200:
        response_200 = BuildSource.from_dict(response.json())

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
    build_source_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePATCHInput,
) -> Response[BuildSource | Error]:
    """Update a build source

     Update a shared build source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the build source's
    underlying identity:
    - `image` on a git-backed build source switches it to image-backed
    - `git` on an image-backed build source switches it to git-backed
    - `git` on a build source that's already git-backed is a pure
      patch onto the existing config

    Args:
        build_source_id (str):
        body (BuildSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuildSource | Error]
    """

    kwargs = _get_kwargs(
        build_source_id=build_source_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    build_source_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePATCHInput,
) -> BuildSource | Error | None:
    """Update a build source

     Update a shared build source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the build source's
    underlying identity:
    - `image` on a git-backed build source switches it to image-backed
    - `git` on an image-backed build source switches it to git-backed
    - `git` on a build source that's already git-backed is a pure
      patch onto the existing config

    Args:
        build_source_id (str):
        body (BuildSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuildSource | Error
    """

    return sync_detailed(
        build_source_id=build_source_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    build_source_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePATCHInput,
) -> Response[BuildSource | Error]:
    """Update a build source

     Update a shared build source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the build source's
    underlying identity:
    - `image` on a git-backed build source switches it to image-backed
    - `git` on an image-backed build source switches it to git-backed
    - `git` on a build source that's already git-backed is a pure
      patch onto the existing config

    Args:
        build_source_id (str):
        body (BuildSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuildSource | Error]
    """

    kwargs = _get_kwargs(
        build_source_id=build_source_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    build_source_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: BuildSourcePATCHInput,
) -> BuildSource | Error | None:
    """Update a build source

     Update a shared build source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the build source's
    underlying identity:
    - `image` on a git-backed build source switches it to image-backed
    - `git` on an image-backed build source switches it to git-backed
    - `git` on a build source that's already git-backed is a pure
      patch onto the existing config

    Args:
        build_source_id (str):
        body (BuildSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuildSource | Error
    """

    return (
        await asyncio_detailed(
            build_source_id=build_source_id,
            client=client,
            body=body,
        )
    ).parsed
