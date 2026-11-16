from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.git_credentials import GitCredentials
from ...types import Response


def _get_kwargs(
    hosted_repo_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/hosted-repos/{hosted_repo_id}/git-credentials".format(
            hosted_repo_id=quote(str(hosted_repo_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | GitCredentials | None:
    if response.status_code == 200:
        response_200 = GitCredentials.from_dict(response.json())

        return response_200

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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | GitCredentials]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    hosted_repo_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | GitCredentials]:
    """Create git credentials

     Issue a short-lived token for the repository. This token entitles the caller to clone the repository
    and, if supported, to push code as well.

    Args:
        hosted_repo_id (str):  Example: hrp-d04m9b1r0fns73ckp94f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitCredentials]
    """

    kwargs = _get_kwargs(
        hosted_repo_id=hosted_repo_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hosted_repo_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GitCredentials | None:
    """Create git credentials

     Issue a short-lived token for the repository. This token entitles the caller to clone the repository
    and, if supported, to push code as well.

    Args:
        hosted_repo_id (str):  Example: hrp-d04m9b1r0fns73ckp94f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitCredentials
    """

    return sync_detailed(
        hosted_repo_id=hosted_repo_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    hosted_repo_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | GitCredentials]:
    """Create git credentials

     Issue a short-lived token for the repository. This token entitles the caller to clone the repository
    and, if supported, to push code as well.

    Args:
        hosted_repo_id (str):  Example: hrp-d04m9b1r0fns73ckp94f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitCredentials]
    """

    kwargs = _get_kwargs(
        hosted_repo_id=hosted_repo_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hosted_repo_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GitCredentials | None:
    """Create git credentials

     Issue a short-lived token for the repository. This token entitles the caller to clone the repository
    and, if supported, to push code as well.

    Args:
        hosted_repo_id (str):  Example: hrp-d04m9b1r0fns73ckp94f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitCredentials
    """

    return (
        await asyncio_detailed(
            hosted_repo_id=hosted_repo_id,
            client=client,
        )
    ).parsed
