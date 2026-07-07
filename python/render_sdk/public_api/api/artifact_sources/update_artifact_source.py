from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact_source import ArtifactSource
from ...models.artifact_source_patch_input import ArtifactSourcePATCHInput
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    artifact_source_id: str,
    *,
    body: ArtifactSourcePATCHInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/artifact-sources/{artifact_source_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ArtifactSource, Error]]:
    if response.status_code == 200:
        response_200 = ArtifactSource.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ArtifactSource, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    artifact_source_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePATCHInput,
) -> Response[Union[ArtifactSource, Error]]:
    """Update an artifact source

     Update a shared artifact source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the artifact source's
    underlying identity:
    - `image` on a git-backed artifact source switches it to image-backed
    - `git` on an image-backed artifact source switches it to git-backed
    - `git` on an artifact source that's already git-backed is a pure
      patch onto the existing config

    Args:
        artifact_source_id (str):
        body (ArtifactSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtifactSource, Error]]
    """

    kwargs = _get_kwargs(
        artifact_source_id=artifact_source_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artifact_source_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePATCHInput,
) -> Optional[Union[ArtifactSource, Error]]:
    """Update an artifact source

     Update a shared artifact source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the artifact source's
    underlying identity:
    - `image` on a git-backed artifact source switches it to image-backed
    - `git` on an image-backed artifact source switches it to git-backed
    - `git` on an artifact source that's already git-backed is a pure
      patch onto the existing config

    Args:
        artifact_source_id (str):
        body (ArtifactSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtifactSource, Error]
    """

    return sync_detailed(
        artifact_source_id=artifact_source_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    artifact_source_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePATCHInput,
) -> Response[Union[ArtifactSource, Error]]:
    """Update an artifact source

     Update a shared artifact source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the artifact source's
    underlying identity:
    - `image` on a git-backed artifact source switches it to image-backed
    - `git` on an image-backed artifact source switches it to git-backed
    - `git` on an artifact source that's already git-backed is a pure
      patch onto the existing config

    Args:
        artifact_source_id (str):
        body (ArtifactSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtifactSource, Error]]
    """

    kwargs = _get_kwargs(
        artifact_source_id=artifact_source_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artifact_source_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtifactSourcePATCHInput,
) -> Optional[Union[ArtifactSource, Error]]:
    """Update an artifact source

     Update a shared artifact source. Each top-level field is a true patch,
    unset fields are left unchanged.

    Supplying `git` or `image` can change the artifact source's
    underlying identity:
    - `image` on a git-backed artifact source switches it to image-backed
    - `git` on an image-backed artifact source switches it to git-backed
    - `git` on an artifact source that's already git-backed is a pure
      patch onto the existing config

    Args:
        artifact_source_id (str):
        body (ArtifactSourcePATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtifactSource, Error]
    """

    return (
        await asyncio_detailed(
            artifact_source_id=artifact_source_id,
            client=client,
            body=body,
        )
    ).parsed
