"""What the mirror promises statically: render_sdk symbols ARE the render types.

Every assertion below pins a value obtained through ``render_sdk`` against the
type it originates from in ``render``. If the generated stubs ever drift from
the real package, mypy fails here.

Never executed. See README.md in this directory.
"""

from render.client.errors import TaskRunError as RealTaskRunError
from render.experimental.key_value import NameOwnerIdOptions as RealNameOwnerIdOptions
from render.public_api import AuthenticatedClient as RealAuthenticatedClient
from render.render import Render as RealRender
from render.render_async import RenderAsync as RealRenderAsync
from render.workflows._callback_models import InputResponse as RealInputResponse
from render.workflows.app import Workflows as RealWorkflows
from render.workflows.task import Options as RealOptions
from render.workflows.task import Retry as RealRetry
from typing_extensions import assert_type

import render_sdk
import render_sdk.client.errors
from render_sdk.experimental.key_value import NameOwnerIdOptions
from render_sdk.public_api import AuthenticatedClient
from render_sdk.workflows import NotAThing  # type: ignore[attr-defined]  # noqa: F401
from render_sdk.workflows._callback_models import InputResponse

# --- top-level names are the real classes ------------------------------------

w = render_sdk.Workflows()
assert_type(w, RealWorkflows)

retry = render_sdk.Retry(max_retries=2, wait_duration_ms=100)
assert_type(retry, RealRetry)

options = render_sdk.Options(retry=retry, timeout_seconds=30, plan="starter")
assert_type(options, RealOptions)


def _consumes_real_workflows(app: RealWorkflows) -> None:
    del app


def _consumes_mirror_workflows(app: render_sdk.Workflows) -> None:
    del app


def workflows_flow_in_both_directions() -> None:
    """A value built under either name satisfies an annotation under the other."""
    _consumes_real_workflows(render_sdk.Workflows())
    _consumes_mirror_workflows(RealWorkflows())


# --- lazy top-level names (module __getattr__ in the real package) -----------

r = render_sdk.Render()
assert_type(r, RealRender)
render_cls: type[RealRender] = render_sdk.Render

ra = render_sdk.RenderAsync()
assert_type(ra, RealRenderAsync)
render_async_cls: type[RealRenderAsync] = render_sdk.RenderAsync


# --- deep and private modules -------------------------------------------------

resp = InputResponse(task_name="t", input_="{}")
assert_type(resp, RealInputResponse)

_placeholder = "not-a-secret"
authed = AuthenticatedClient(base_url="https://api.render.com", token=_placeholder)
assert_type(authed, RealAuthenticatedClient)

kv_options = NameOwnerIdOptions(name="my-instance")
assert_type(kv_options, RealNameOwnerIdOptions)


# --- exceptions caught via render_sdk are the render exceptions --------------


def _expects_real_error(err: RealTaskRunError) -> None:
    del err


def task_run_error_is_the_real_type() -> None:
    try:
        raise render_sdk.client.errors.TaskRunError("boom")
    except render_sdk.client.errors.TaskRunError as e:
        assert_type(e, RealTaskRunError)
        _expects_real_error(e)


# --- negative assertions ------------------------------------------------------
# The stubs re-export explicitly, so names that do not exist in the real
# package are rejected. warn_unused_ignores turns each ignore into an
# assertion that the error genuinely occurs. (See also the NotAThing import
# in the block at the top of this file.)

_missing = render_sdk.NoSuchName  # type: ignore[attr-defined]
