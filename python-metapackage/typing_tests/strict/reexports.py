"""Every documented public symbol imports through render_sdk under --strict.

``--strict`` enables ``--no-implicit-reexport``, so each import below only
type-checks because the generated stubs re-export explicitly
(``from render... import name as name`` plus a literal ``__all__``). This file
is the empirical proof that the mirror survives strict consumers.

Never executed. See README.md in the parent directory.
"""

from render_sdk import (
    Options,
    Render,
    RenderAsync,
    Retry,
    TaskContext,
    Workflows,
    __version__,
    start,
    task,
)
from render_sdk.client import (
    Client,
    ListTaskRunsParams,
    TaskData,
    TaskRun,
    TaskRunStatus,
    TaskSlug,
    WorkflowsService,
)
from render_sdk.client.errors import (
    ClientError,
    RateLimitError,
    RenderError,
    ServerError,
    TaskRunError,
    TimeoutError,
)
from render_sdk.experimental.key_value import (
    ConnectionInfo,
    InstanceConfiguration,
    KeyValueApi,
    KeyValueProvider,
    NameOwnerIdOptions,
    ServiceIdOptions,
)
from render_sdk.experimental.key_value import (
    Options as KeyValueOptions,
)
from render_sdk.experimental.sandbox import (
    Sandbox,
    SandboxClient,
    SandboxExecEvent,
    SandboxExecExit,
    SandboxExecOutput,
    SandboxList,
    SandboxNotFoundError,
)
from render_sdk.public_api import AuthenticatedClient

__all__ = [
    "AuthenticatedClient",
    "Client",
    "ClientError",
    "ConnectionInfo",
    "InstanceConfiguration",
    "KeyValueApi",
    "KeyValueOptions",
    "KeyValueProvider",
    "ListTaskRunsParams",
    "NameOwnerIdOptions",
    "Options",
    "RateLimitError",
    "Render",
    "RenderAsync",
    "RenderError",
    "Retry",
    "Sandbox",
    "SandboxClient",
    "SandboxExecEvent",
    "SandboxExecExit",
    "SandboxExecOutput",
    "SandboxList",
    "SandboxNotFoundError",
    "ServerError",
    "ServiceIdOptions",
    "TaskContext",
    "TaskData",
    "TaskRun",
    "TaskRunError",
    "TaskRunStatus",
    "TaskSlug",
    "TimeoutError",
    "Workflows",
    "WorkflowsService",
    "__version__",
    "start",
    "task",
]


# --- fully-typed usage: strict mode rejects Any leaking out of the mirror ----


def sdk_version() -> str:
    return __version__


def make_workflows() -> Workflows:
    return Workflows()


def make_sync_client() -> Render:
    return Render()


def make_async_client() -> RenderAsync:
    return RenderAsync()


def retry_wait(retry: Retry) -> int:
    return retry.wait_duration_ms


def options_plan(options: Options) -> str | None:
    return options.plan


def task_run_status(run: TaskRun) -> TaskRunStatus:
    return run.status


def kv_instance_name(kv_options: NameOwnerIdOptions) -> str:
    return kv_options.name


def sandbox_id(box: Sandbox) -> str:
    return box.id


def describe_error(err: TaskRunError) -> str:
    return str(err)


def use_context(ctx: TaskContext) -> TaskContext:
    return ctx
