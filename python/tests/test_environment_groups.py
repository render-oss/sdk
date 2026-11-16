from datetime import UTC, datetime

import pytest

from render.public_api.models.env_group import EnvGroup
from render.public_api.models.env_var import EnvVar
from render.public_api.models.secret_file import SecretFile
from render.public_api.types import UNSET


@pytest.mark.parametrize(
    "env_vars, expected_env_vars",
    [
        pytest.param(UNSET, UNSET, id="env-vars-omitted"),
        pytest.param([], [], id="env-vars-empty"),
        pytest.param(
            [{"key": "LOG_LEVEL", "value": "debug"}],
            [EnvVar(key="LOG_LEVEL", value="debug")],
            id="env-vars-present",
        ),
    ],
)
@pytest.mark.parametrize(
    "secret_files, expected_secret_files",
    [
        pytest.param(UNSET, UNSET, id="secret-files-omitted"),
        pytest.param([], [], id="secret-files-empty"),
        pytest.param(
            [{"name": "config", "content": "example"}],
            [SecretFile(name="config", content="example")],
            id="secret-files-present",
        ),
    ],
)
def test_env_group_preserves_optional_secret_values(
    env_vars, expected_env_vars, secret_files, expected_secret_files
):
    payload = {
        "id": "evg-test",
        "name": "shared",
        "ownerId": "tea-test",
        "createdAt": "2026-11-16T00:00:00+00:00",
        "updatedAt": "2026-11-16T00:00:00+00:00",
        "serviceLinks": [],
        "environmentId": "env-test",
    }
    if env_vars is not UNSET:
        payload["envVars"] = env_vars
    if secret_files is not UNSET:
        payload["secretFiles"] = secret_files

    group = EnvGroup.from_dict(payload)

    if expected_env_vars is UNSET:
        assert group.env_vars is UNSET
    else:
        assert group.env_vars == expected_env_vars
    if expected_secret_files is UNSET:
        assert group.secret_files is UNSET
    else:
        assert group.secret_files == expected_secret_files
    assert group.to_dict() == payload


@pytest.mark.parametrize("environment_id", [UNSET, "env-test"])
def test_env_group_accepts_secret_values_by_keyword(environment_id):
    timestamp = datetime(2026, 11, 16, tzinfo=UTC)
    group = EnvGroup(
        id="evg-test",
        name="shared",
        owner_id="tea-test",
        created_at=timestamp,
        updated_at=timestamp,
        service_links=[],
        env_vars=[EnvVar(key="LOG_LEVEL", value="debug")],
        secret_files=[SecretFile(name="config", content="example")],
        environment_id=environment_id,
    )

    expected = {
        "id": "evg-test",
        "name": "shared",
        "ownerId": "tea-test",
        "createdAt": "2026-11-16T00:00:00+00:00",
        "updatedAt": "2026-11-16T00:00:00+00:00",
        "serviceLinks": [],
        "envVars": [{"key": "LOG_LEVEL", "value": "debug"}],
        "secretFiles": [{"name": "config", "content": "example"}],
    }
    if environment_id is not UNSET:
        expected["environmentId"] = "env-test"
    assert group.to_dict() == expected
