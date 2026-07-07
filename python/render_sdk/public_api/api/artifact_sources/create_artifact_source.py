from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact_source import ArtifactSource
from ...models.artifact_source_post_input import ArtifactSourcePOSTInput
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: ArtifactSourcePOSTInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/artifact-sources",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ArtifactSource, Error]]:
    if response.status_code == 201:
        response_201 = ArtifactSource.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ArtifactSource, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePOSTInput,
) -> Response[Union[ArtifactSource, Error]]:
    """Create an artifact source

     Create an artifact source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the artifact source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the artifact source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    Args:
        body (ArtifactSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtifactSource, Error]]
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
    body: ArtifactSourcePOSTInput,
) -> Optional[Union[ArtifactSource, Error]]:
    """Create an artifact source

     Create an artifact source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the artifact source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the artifact source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    Args:
        body (ArtifactSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtifactSource, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePOSTInput,
) -> Response[Union[ArtifactSource, Error]]:
    """Create an artifact source

     Create an artifact source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the artifact source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the artifact source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    Args:
        body (ArtifactSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtifactSource, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePOSTInput,
) -> Optional[Union[ArtifactSource, Error]]:
    """Create an artifact source

     Create an artifact source that can be linked to one or more
    services in the same workspace.

    Exactly one of `git` or `image` must be set:
    - `git`: the artifact source is git-backed. The code is built in
       the requested `region` (defaults to `oregon`).
    - `image`: the artifact source is image-backed. It points at an
      existing image in an external registry; no build is performed.

    Args:
        body (ArtifactSourcePOSTInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtifactSource, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
