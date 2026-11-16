from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.workflow_version import WorkflowVersion
from ...types import Response


def _get_kwargs(
    workflow_version_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workflowversions/{workflow_version_id}".format(
            workflow_version_id=quote(str(workflow_version_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | WorkflowVersion | None:
    if response.status_code == 200:
        response_200 = WorkflowVersion.from_dict(response.json())

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
) -> Response[Error | WorkflowVersion]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_version_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkflowVersion]:
    """Retrieve workflow version

     Retrieve the specific workflow service version with the provided ID.

    Args:
        workflow_version_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkflowVersion]
    """

    kwargs = _get_kwargs(
        workflow_version_id=workflow_version_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_version_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkflowVersion | None:
    """Retrieve workflow version

     Retrieve the specific workflow service version with the provided ID.

    Args:
        workflow_version_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkflowVersion
    """

    return sync_detailed(
        workflow_version_id=workflow_version_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workflow_version_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkflowVersion]:
    """Retrieve workflow version

     Retrieve the specific workflow service version with the provided ID.

    Args:
        workflow_version_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkflowVersion]
    """

    kwargs = _get_kwargs(
        workflow_version_id=workflow_version_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_version_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkflowVersion | None:
    """Retrieve workflow version

     Retrieve the specific workflow service version with the provided ID.

    Args:
        workflow_version_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkflowVersion
    """

    return (
        await asyncio_detailed(
            workflow_version_id=workflow_version_id,
            client=client,
        )
    ).parsed
