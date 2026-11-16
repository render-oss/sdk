"""HTTP transport contracts shared by generated and handwritten clients."""

from email import policy
from email.parser import BytesParser
from io import BytesIO

import httpx2
import pytest

from render import Render, RenderAsync
from render.client.errors import ClientError, ServerError, TimeoutError
from render.public_api.api.blueprints import validate_blueprint
from render.public_api.client import AuthenticatedClient
from render.public_api.models.validate_blueprint_request import ValidateBlueprintRequest
from render.public_api.types import File


@pytest.mark.parametrize(
    "transport_error, sdk_error",
    [
        (httpx2.ReadTimeout, TimeoutError),
        (httpx2.ConnectError, ServerError),
        (httpx2.RequestError, ClientError),
    ],
)
def test_sync_transport_errors_keep_sdk_error_types(transport_error, sdk_error):
    error = transport_error("transport failed")

    def handler(request):
        raise error

    render = Render(token="test-token")
    with httpx2.Client(
        base_url="https://api.test/v1", transport=httpx2.MockTransport(handler)
    ) as client:
        render.client.internal.set_httpx_client(client)

        with pytest.raises(sdk_error, match="get task run") as excinfo:
            render.workflows.get_task_run("trn-test")

    assert excinfo.value.__cause__ is error


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transport_error, sdk_error",
    [
        (httpx2.ReadTimeout, TimeoutError),
        (httpx2.ConnectError, ServerError),
        (httpx2.RequestError, ClientError),
    ],
)
async def test_async_transport_errors_keep_sdk_error_types(transport_error, sdk_error):
    error = transport_error("transport failed")

    def handler(request):
        raise error

    render = RenderAsync(token="test-token")
    async with httpx2.AsyncClient(
        base_url="https://api.test/v1", transport=httpx2.MockTransport(handler)
    ) as client:
        render.client.internal.set_async_httpx_client(client)

        with pytest.raises(sdk_error, match="get task run") as excinfo:
            await render.workflows.get_task_run("trn-test")

    assert excinfo.value.__cause__ is error


@pytest.mark.asyncio
@pytest.mark.parametrize("use_async", [False, True], ids=["sync", "async"])
async def test_blueprint_upload_preserves_multipart_boundary_in_file(use_async):
    payload = b"first line\r\n--+++\r\nstill the same file\r\n"
    received = {}

    def handler(request):
        message = BytesParser(policy=policy.default).parsebytes(
            b"Content-Type: "
            + request.headers["Content-Type"].encode()
            + b"\r\nMIME-Version: 1.0\r\n\r\n"
            + request.content
        )
        for part in message.iter_parts():
            name = part.get_param("name", header="content-disposition")
            received[name] = part.get_payload(decode=True)
        assert request.headers["Authorization"] == "Bearer test-token"
        assert request.extensions["timeout"]["read"] == 5.0
        return httpx2.Response(200, json={"valid": True})

    client = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        timeout=httpx2.Timeout(5.0),
        httpx_args={"transport": httpx2.MockTransport(handler)},
    )
    body = ValidateBlueprintRequest(
        owner_id="tea-test",
        file=File(payload=BytesIO(payload), file_name="render.yaml"),
    )
    if use_async:
        async with client:
            response = await validate_blueprint.asyncio_detailed(
                client=client, body=body
            )
    else:
        with client:
            response = validate_blueprint.sync_detailed(client=client, body=body)

    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed.valid is True
    assert received == {"ownerId": b"tea-test", "file": payload}
