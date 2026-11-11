import inspect
import json
from datetime import datetime, timezone

import httpx
import pytest

from render.client.errors import ClientError, RateLimitError
from render.experimental.sandbox.client import CredentialClient, SandboxClient
from render.experimental.sandbox.client_sync import SyncSandboxClient
from render.experimental.sandbox.errors import CredentialNotFoundError
from render.experimental.sandbox.types import (
    Credential,
    CredentialInjection,
    CredentialVersion,
)
from render.public_api.client import AuthenticatedClient

VERSION_JSON = {
    "id": 2,
    "updatedAt": "2026-10-01T00:00:00Z",
    "updatedBy": "usr-abc",
    "fingerprint": "fp-2",
}

CREDENTIAL_JSON = {
    "id": "openai",
    "domain": "api.openai.com",
    "enabled": True,
    "methods": ["POST"],
    "paths": ["/v1/**"],
    "injection": {
        "type": "header",
        "name": "Authorization",
        "template": "Bearer ${SECRET}",
    },
    "version": VERSION_JSON,
}

EXPECTED_CREDENTIAL = Credential(
    id="openai",
    domain="api.openai.com",
    enabled=True,
    methods=["POST"],
    paths=["/v1/**"],
    injection=CredentialInjection(
        type="header", name="Authorization", template="Bearer ${SECRET}"
    ),
    version=CredentialVersion(
        id=2,
        updated_at=datetime(2026, 10, 1, tzinfo=timezone.utc),
        updated_by="usr-abc",
        fingerprint="fp-2",
    ),
)

ERROR_404_JSON = {"id": "err-abc", "message": "not found"}


def _client(client_type, handler):
    internal = AuthenticatedClient(
        base_url="https://api.test/v1",
        token="test-token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return client_type(internal, default_owner_id="tea-test")


@pytest.fixture(params=[SandboxClient, SyncSandboxClient], ids=["async", "sync"])
def make_client(request):
    return lambda handler: _client(request.param, handler)


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


def _capture(captured, status, body=None):
    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["body"] = json.loads(request.content) if request.content else None
        if body is None:
            return httpx.Response(status)
        return httpx.Response(status, json=body)

    return handler


def _unreachable(request: httpx.Request) -> httpx.Response:
    raise AssertionError("handler should not be reached")


def test_sandbox_client_exposes_credentials():
    client = _client(SandboxClient, _unreachable)
    assert isinstance(client.credentials, CredentialClient)


# --- create ---


@pytest.mark.asyncio
async def test_create_posts_the_credential_and_returns_it(make_client):
    captured = {}
    client = make_client(_capture(captured, 201, CREDENTIAL_JSON))

    credential = await _resolve(
        client.credentials.create(
            sandbox_group_id="sbg-abc",
            credential_id="openai",
            domain="api.openai.com",
            value="sk-secret",
            injection=CredentialInjection(
                type="header", name="Authorization", template="Bearer ${SECRET}"
            ),
            methods=["POST"],
            paths=["/v1/**"],
            enabled=False,
        )
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials"
    assert captured["body"] == {
        "id": "openai",
        "domain": "api.openai.com",
        "value": "sk-secret",
        "injection": {
            "type": "header",
            "name": "Authorization",
            "template": "Bearer ${SECRET}",
        },
        "methods": ["POST"],
        "paths": ["/v1/**"],
        "enabled": False,
    }
    assert credential == EXPECTED_CREDENTIAL


@pytest.mark.asyncio
async def test_create_omits_filters_and_injection_fields_left_unset(make_client):
    captured = {}
    client = make_client(_capture(captured, 201, CREDENTIAL_JSON))

    await _resolve(
        client.credentials.create(
            sandbox_group_id="sbg-abc",
            credential_id="github",
            domain="api.github.com",
            value="user:token",
            injection=CredentialInjection(type="basic"),
        )
    )

    # enabled is sent as the API's default; methods, paths, name and template
    # are left out so the API applies its own defaults.
    assert captured["body"] == {
        "id": "github",
        "domain": "api.github.com",
        "value": "user:token",
        "injection": {"type": "basic"},
        "enabled": True,
    }


@pytest.mark.asyncio
async def test_create_rejects_an_unknown_injection_type_before_the_request(
    make_client,
):
    client = make_client(_unreachable)

    with pytest.raises(ValueError):
        await _resolve(
            client.credentials.create(
                sandbox_group_id="sbg-abc",
                credential_id="openai",
                domain="api.openai.com",
                value="sk-secret",
                injection=CredentialInjection(type="bearer"),
            )
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [404, 409])
async def test_create_raises_a_plain_client_error_for_a_missing_group_or_duplicate(
    make_client, status
):
    client = make_client(_capture({}, status, {"message": "nope"}))

    with pytest.raises(ClientError) as excinfo:
        await _resolve(
            client.credentials.create(
                sandbox_group_id="sbg-abc",
                credential_id="openai",
                domain="api.openai.com",
                value="sk-secret",
                injection=CredentialInjection(type="header", name="X-Api-Key"),
            )
        )

    assert not isinstance(excinfo.value, CredentialNotFoundError)
    assert excinfo.value.status_code == status


# --- from_id ---


@pytest.mark.asyncio
async def test_from_id_gets_the_credential(make_client):
    captured = {}
    client = make_client(_capture(captured, 200, CREDENTIAL_JSON))

    credential = await _resolve(
        client.credentials.from_id(sandbox_group_id="sbg-abc", credential_id="openai")
    )

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials/openai"
    assert credential == EXPECTED_CREDENTIAL


@pytest.mark.asyncio
async def test_from_id_returns_none_for_a_missing_version_and_injection_fields(
    make_client,
):
    body = {
        **CREDENTIAL_JSON,
        "methods": [],
        "paths": [],
        "injection": {"type": "basic"},
    }
    del body["version"]
    client = make_client(_capture({}, 200, body))

    credential = await _resolve(
        client.credentials.from_id(sandbox_group_id="sbg-abc", credential_id="openai")
    )

    assert credential.version is None
    assert credential.injection == CredentialInjection(type="basic")
    assert credential.methods == []
    assert credential.paths == []


@pytest.mark.asyncio
async def test_from_id_raises_credential_not_found(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(
        CredentialNotFoundError, match="credential openai not found"
    ) as excinfo:
        await _resolve(
            client.credentials.from_id(
                sandbox_group_id="sbg-abc", credential_id="openai"
            )
        )

    assert excinfo.value.status_code == 404


# --- list ---


@pytest.mark.asyncio
async def test_list_returns_every_credential(make_client):
    captured = {}
    second = {**CREDENTIAL_JSON, "id": "stripe", "domain": "api.stripe.com"}
    client = make_client(_capture(captured, 200, [CREDENTIAL_JSON, second]))

    credentials = await _resolve(client.credentials.list(sandbox_group_id="sbg-abc"))

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials"
    assert [c.id for c in credentials] == ["openai", "stripe"]
    assert credentials[0] == EXPECTED_CREDENTIAL
    assert credentials[1].domain == "api.stripe.com"


@pytest.mark.asyncio
async def test_list_raises_a_plain_client_error_for_a_missing_group(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(ClientError) as excinfo:
        await _resolve(client.credentials.list(sandbox_group_id="sbg-abc"))

    assert not isinstance(excinfo.value, CredentialNotFoundError)
    assert excinfo.value.status_code == 404


# --- update ---


@pytest.mark.asyncio
async def test_update_sends_only_the_fields_given(make_client):
    captured = {}
    client = make_client(_capture(captured, 200, CREDENTIAL_JSON))

    credential = await _resolve(
        client.credentials.update(
            sandbox_group_id="sbg-abc", credential_id="openai", enabled=False
        )
    )

    assert captured["method"] == "PATCH"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials/openai"
    assert captured["body"] == {"enabled": False}
    assert credential == EXPECTED_CREDENTIAL


@pytest.mark.asyncio
async def test_create_and_update_treat_a_string_filter_as_one_value(make_client):
    captured = {}
    client = make_client(_capture(captured, 200, CREDENTIAL_JSON))

    await _resolve(
        client.credentials.update(
            sandbox_group_id="sbg-abc",
            credential_id="openai",
            methods="POST",
            paths="/v1/**",
        )
    )

    assert captured["body"] == {"methods": ["POST"], "paths": ["/v1/**"]}


@pytest.mark.asyncio
async def test_update_sends_empty_filters_to_clear_them(make_client):
    captured = {}
    client = make_client(_capture(captured, 200, CREDENTIAL_JSON))

    await _resolve(
        client.credentials.update(
            sandbox_group_id="sbg-abc", credential_id="openai", methods=[], paths=[]
        )
    )

    assert captured["body"] == {"methods": [], "paths": []}


@pytest.mark.asyncio
async def test_update_sends_value_domain_and_injection(make_client):
    captured = {}
    client = make_client(_capture(captured, 200, CREDENTIAL_JSON))

    await _resolve(
        client.credentials.update(
            sandbox_group_id="sbg-abc",
            credential_id="openai",
            value="sk-rotated",
            domain="api.example.com",
            injection=CredentialInjection(type="query", name="key"),
        )
    )

    assert captured["body"] == {
        "value": "sk-rotated",
        "domain": "api.example.com",
        "injection": {"type": "query", "name": "key"},
    }


@pytest.mark.asyncio
async def test_update_raises_credential_not_found(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(CredentialNotFoundError):
        await _resolve(
            client.credentials.update(
                sandbox_group_id="sbg-abc", credential_id="openai", enabled=True
            )
        )


# --- delete ---


@pytest.mark.asyncio
async def test_delete_sends_delete_and_accepts_202(make_client):
    captured = {}
    client = make_client(_capture(captured, 202))

    result = await _resolve(
        client.credentials.delete(sandbox_group_id="sbg-abc", credential_id="openai")
    )

    assert captured["method"] == "DELETE"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials/openai"
    assert result is None


@pytest.mark.asyncio
async def test_delete_raises_a_plain_client_error_for_a_missing_group(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(ClientError) as excinfo:
        await _resolve(
            client.credentials.delete(
                sandbox_group_id="sbg-abc", credential_id="openai"
            )
        )

    assert not isinstance(excinfo.value, CredentialNotFoundError)
    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_raises_rate_limit_error_on_429(make_client):
    client = make_client(_capture({}, 429, {"message": "retry"}))

    with pytest.raises(RateLimitError):
        await _resolve(
            client.credentials.delete(
                sandbox_group_id="sbg-abc", credential_id="openai"
            )
        )


# --- versions ---


@pytest.mark.asyncio
async def test_list_versions_returns_the_versions(make_client):
    captured = {}
    restored = {**VERSION_JSON, "id": 3, "restoredFromVersionId": 1}
    client = make_client(_capture(captured, 200, [restored, VERSION_JSON]))

    versions = await _resolve(
        client.credentials.list_versions(
            sandbox_group_id="sbg-abc", credential_id="openai"
        )
    )

    assert captured["method"] == "GET"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials/openai/versions"
    assert [v.id for v in versions] == [3, 2]
    assert versions[0].restored_from_version_id == 1
    assert versions[1] == EXPECTED_CREDENTIAL.version


@pytest.mark.asyncio
async def test_list_versions_raises_credential_not_found(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(CredentialNotFoundError):
        await _resolve(
            client.credentials.list_versions(
                sandbox_group_id="sbg-abc", credential_id="openai"
            )
        )


@pytest.mark.asyncio
async def test_restore_posts_the_version_and_returns_the_credential(make_client):
    captured = {}
    body = {
        **CREDENTIAL_JSON,
        "version": {**VERSION_JSON, "id": 4, "restoredFromVersionId": 2},
    }
    client = make_client(_capture(captured, 200, body))

    credential = await _resolve(
        client.credentials.restore(
            sandbox_group_id="sbg-abc", credential_id="openai", version_id=2
        )
    )

    assert captured["method"] == "POST"
    assert captured["path"] == "/v1/sandbox-groups/sbg-abc/credentials/openai/restore"
    assert captured["body"] == {"versionId": 2}
    assert credential.version is not None
    assert credential.version.id == 4
    assert credential.version.restored_from_version_id == 2


@pytest.mark.asyncio
async def test_restore_raises_credential_not_found_naming_the_version(make_client):
    client = make_client(_capture({}, 404, ERROR_404_JSON))

    with pytest.raises(CredentialNotFoundError, match="version 7"):
        await _resolve(
            client.credentials.restore(
                sandbox_group_id="sbg-abc", credential_id="openai", version_id=7
            )
        )
