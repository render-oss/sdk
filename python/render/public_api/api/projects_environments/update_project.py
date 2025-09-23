from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.project import Project
from ...models.project_patch_input import ProjectPATCHInput
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: ProjectPATCHInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/projects/{project_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, Project]]:
    if response.status_code == 200:
        response_200 = Project.from_dict(response.json())

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
) -> Response[Union[Error, Project]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ProjectPATCHInput,
) -> Response[Union[Error, Project]]:
    """Update project

     Update the details of a project.

    To update the details of a particular _environment_ in the project, instead use the [Update
    environment](https://api-docs.render.com/reference/update-environment) endpoint.

    Args:
        project_id (str):
        body (ProjectPATCHInput): Input type for updating a project

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Project]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ProjectPATCHInput,
) -> Optional[Union[Error, Project]]:
    """Update project

     Update the details of a project.

    To update the details of a particular _environment_ in the project, instead use the [Update
    environment](https://api-docs.render.com/reference/update-environment) endpoint.

    Args:
        project_id (str):
        body (ProjectPATCHInput): Input type for updating a project

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Project]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ProjectPATCHInput,
) -> Response[Union[Error, Project]]:
    """Update project

     Update the details of a project.

    To update the details of a particular _environment_ in the project, instead use the [Update
    environment](https://api-docs.render.com/reference/update-environment) endpoint.

    Args:
        project_id (str):
        body (ProjectPATCHInput): Input type for updating a project

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Project]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ProjectPATCHInput,
) -> Optional[Union[Error, Project]]:
    """Update project

     Update the details of a project.

    To update the details of a particular _environment_ in the project, instead use the [Update
    environment](https://api-docs.render.com/reference/update-environment) endpoint.

    Args:
        project_id (str):
        body (ProjectPATCHInput): Input type for updating a project

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Project]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
