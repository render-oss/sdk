# Render SDK for Python

The official Python SDK for Render. Define Workflow tasks and flows, manage task runs and flow runs, and access experimental platform features like object storage.

## Features

- **REST API Client**: Run, monitor, cancel, and list task runs and flow runs
- **Task Definition**: Decorator-based task registration with the `Workflows` class
- **Durable Flows**: Flows that replay after a crash, with steps that retry in-process
- **Server-Sent Events**: Real-time streaming of task run events
- **Sync & Async**: Synchronous `Render` client (default) and async `RenderAsync` variant
- **Retry Configuration**: Configurable retry behavior with exponential backoff
- **Subtask Execution**: Execute tasks from within other tasks
- **Task Composition**: Combine tasks from multiple modules with `Workflows.from_workflows()`
- **Object Storage**: Experimental object storage API with upload, download, and list
- **Key Value**: Experimental Render Key value client with auto-provisioning and configuration sync

## Installation

```bash
pip install render
```

Or with uv:

```bash
uv add render
```

## Quick Start

### REST API Client

Use the `Render` client to run tasks and flows and monitor their status:

```python
from render import Render
from render.client import ListTaskRunsParams
from render.client.errors import TaskRunError

render = Render()  # Uses RENDER_API_KEY from the environment

# run_task() starts a task and waits for completion in one call.
try:
    result = render.workflows.run_task("my-workflow/my-task", [3, 4])
    print(result.results)
except TaskRunError as e:
    print(f"Task failed: {e}")

# start_task() starts a task without waiting for the result.
task_run = render.workflows.start_task("my-workflow/my-task", [3, 4])
print(f"Task started: {task_run.id}")

# Get task run details by ID
details = render.workflows.get_task_run(task_run.id)
print(f"Status: {details.status}")

# Cancel a running task
render.workflows.cancel_task_run(task_run.id)

# Stream task run events
for event in render.workflows.task_run_events([task_run.id]):
    print(f"{event.id} status={event.status}")

# List recent task runs
runs = render.workflows.list_task_runs(ListTaskRunsParams(limit=10))
```

#### Idempotency Keys

Pass an `idempotency_key` to make starting a run safe to retry. Repeating a call
with the same key within 24 hours returns the run the first call started instead
of starting another one, so a client that retries after a timeout does not run
the task twice. Keys are scoped to a workflow.

```python
task_run = render.workflows.start_task(
    "my-workflow/charge", [order_id], idempotency_key=f"charge-{order_id}"
)
```

#### Async Usage

For async contexts (e.g. FastAPI), use `RenderAsync`:

```python
import asyncio
from render import RenderAsync

async def main():
    render = RenderAsync()

    result = await render.workflows.run_task("my-workflow/my-task", [3, 4])
    print(result.results)

    # start_task() returns an awaitable task run
    task_run = await render.workflows.start_task("my-workflow/my-task", [3, 4])
    result = await task_run  # wait when ready

    # Stream task run events
    async for event in render.workflows.task_run_events([task_run.id]):
        print(f"{event.id} status={event.status}")

asyncio.run(main())
```

#### Running Flows

The client starts, inspects, lists and cancels flow runs the same way it does
task runs. A flow slug has the format `workflow-slug/flow-name`. Append
`:version` to run a specific version; otherwise the latest version runs.

```python
from render import Render
from render.client import ListFlowRunsParams
from render.client.errors import FlowRunError

render = Render()  # Uses RENDER_API_KEY from the environment

# run_flow() starts a flow run and waits for it to finish in one call.
try:
    details = render.workflows.run_flow(
        "my-workflow/fulfill_order", ["ord_123", 4200, "customer@example.com"]
    )
    print(details.results)
except FlowRunError as e:
    print(f"Flow run {e.flow_run_id} did not succeed: {e}")

# start_flow() starts a flow run without waiting for it to finish.
flow_run = render.workflows.start_flow(
    "my-workflow/fulfill_order",
    ["ord_123", 4200, "customer@example.com"],
    idempotency_key="fulfill-ord_123",
)
print(f"Flow started: {flow_run.id}")

# Get flow run details by ID
details = render.workflows.get_flow_run(flow_run.id)
print(f"Status: {details.status}")

# Cancel a running flow
render.workflows.cancel_flow_run(flow_run.id)

# List recent failed flow runs
runs = render.workflows.list_flow_runs(ListFlowRunsParams(limit=10, status=["failed"]))
```

`run_flow` checks the run's status with backoff (1 second, doubling up to 60)
until it finishes, and keeps waiting while the run is paused. It returns the
details of a succeeded run and raises `FlowRunError` if the run fails or is
canceled; the error's `details` carry the final status and `error`. It has no
deadline. `start_flow` returns after the run is created; the details from
`get_flow_run` carry the run's `results`, `error` and `attempts`.

`RenderAsync` has the same methods as coroutines:

```python
details = await render.workflows.run_flow("my-workflow/fulfill_order", [...])
flow_run = await render.workflows.start_flow("my-workflow/fulfill_order", [...])
details = await render.workflows.get_flow_run(flow_run.id)
```

### Task Definition

Use the `Workflows` class to define and register tasks. Every task takes a
`TaskContext` as its first parameter, followed by its inputs:

```python
from render import TaskContext, Workflows

app = Workflows()

@app.task
def square(ctx: TaskContext, a: int) -> int:
    """Square a number."""
    return a * a


@app.task
async def add_squares(ctx: TaskContext, a: int, b: int) -> int:
    """Add the squares of two numbers."""
    # .run runs the task on its own compute
    result1 = await ctx.run(square, a)
    result2 = await ctx.run(square, b)
    return result1 + result2
```

Run several tasks at once with `asyncio.gather`:

```python
import asyncio

@app.task
async def sum_squares(ctx: TaskContext, values: list[int]) -> int:
    squares = await asyncio.gather(*(ctx.run(square, v) for v in values))
    return sum(squares)
```

You can also specify task parameters like `retry`, `timeout`, and `plan`:

```python
from render import Retry, TaskContext, Workflows

app = Workflows(
    default_retry=Retry(max_retries=3, wait_duration_ms=1000),
    default_timeout=300,
    default_plan="standard",
)

@app.task(timeout=60, plan="starter")
def quick_task(ctx: TaskContext, x: int) -> int:
    return x + 1

@app.task(retry=Retry(max_retries=5, wait_duration_ms=2000, backoff_scaling=2.0))
def retryable_task(ctx: TaskContext, x: int) -> int:
    return x * 2
```

You can combine tasks from multiple modules using `Workflows.from_workflows()`:

```python
from tasks_a import app as app_a
from tasks_b import app as app_b

combined = Workflows.from_workflows(app_a, app_b)
```

#### Task run IDs

The task context exposes a read-only `ctx.metadata` object with
`task_run_id`, `root_task_run_id`, and `parent_task_run_id` fields. The SDK reads
them from the initial input response and keeps them for that execution, so
accessing metadata does not make a network request.

For a root run, `ctx.metadata.root_task_run_id` equals
`ctx.metadata.task_run_id` and `ctx.metadata.parent_task_run_id` is `None`.
IDs are `None` when unavailable.

### Durable Flows

A flow is a task that resumes after a crash. Register one with `@app.flow`.
Each `ctx` call in a flow is a durable **step**, and the SDK records its
result. After a crash, the flow reruns from the top, and `ctx` calls for
finished steps return the recorded results instead of running again.

A flow is a sync function that takes a `FlowContext` as its first parameter.
`ctx.step(name, fn, *args, retry=...)` runs `fn` inline, in the flow's process,
and returns its result. Without `retry`, a step makes one attempt.

```python
import uuid

from render import FlowContext, Retry, Workflows

app = Workflows()


# A plain function. From a flow, it runs inline as a step.
def charge_card(order_id: str, total: int) -> dict:
    return payments.charge(order_id, total)


@app.flow
def fulfill_order(ctx: FlowContext, order_id: str, total: int, email: str) -> dict:
    charge = ctx.step(
        "charge",
        charge_card,
        order_id,
        total,
        retry=Retry(max_retries=3, wait_duration_ms=1000),
    )
    invoice = ctx.step("invoice", create_invoice, order_id)
    receipt_id = ctx.step("receipt_id", lambda: str(uuid.uuid4()))
    ctx.step("send", send_receipt, email, invoice["id"], receipt_id)
    return {"charge": charge["id"], "invoice": invoice["id"]}
```

Rules for flow code:
- **Be deterministic.** A replay must make the same `ctx` calls in the same
  order with the same inputs. Put I/O, clocks, random values and anything else
  non-deterministic inside a step.
- **Run one step at a time.** Parallel steps are not supported yet.
- **Steps are sync functions and make no `ctx` calls.** A step's arguments and
  result are recorded as JSON.
- **Set retries on steps, not flows.** Flows take no retry policy: they replay
  after infrastructure failures instead.
- **If a step fails for good, the run fails**, even if the flow catches the
  error. Raise `TerminalFlowError` from a step to fail it without retrying.
- **Don't pass secrets through step inputs or outputs.** Render stores them.
- `ctx.invoke` and `ctx.sleep` are not supported yet, so flows can't run
  registered tasks. Call the task's plain function as a step instead.

For limits, supported regions and how flow runs recover, see the
[Workflows documentation](https://render.com/docs/workflows).

### Run the Local Task Server

For local development, use the Render CLI:

```bash
render workflows dev -- <start command>
```

For example:

```bash
render workflows dev -- python main.py
```

To interact with tasks registered to the local task server, run CLI commands with the `--local` flag in another terminal. For example:

```bash
render workflows tasks start <task name> --local
```

## Environment Variables

- `RENDER_API_KEY` - Your Render API key
- `RENDER_WORKSPACE_ID` - Default owner ID for object storage (workspace team ID, e.g. `tea-xxxxx`)
- `RENDER_REGION` - Default region for object storage (e.g. `oregon`, `frankfurt`)
- `RENDER_USE_LOCAL_DEV` - Enable local development mode (`true`/`false`)
- `RENDER_LOCAL_DEV_URL` - Local development URL (default: `http://localhost:8120`)
- `RENDER_SDK_MODE` - Task execution mode (`run` or `register`)
- `RENDER_SDK_SOCKET_PATH` - Unix socket path for task communication
- `RENDER_LOCAL_REDIS_HOST` - Custom host for local Redis / Valkey instance (default: `localhost`) (requires `RENDER_USE_LOCAL_DEV=true`)
- `RENDER_LOCAL_REDIS_PORT` - Custom port for local Redis / Valkey instance (default: `6379`) (requires `RENDER_USE_LOCAL_DEV=true`)

## Object Storage

```python
from render import Render

render = Render()  # Uses RENDER_API_KEY, RENDER_WORKSPACE_ID, RENDER_REGION from environment

# Upload an object (no need to pass owner_id/region when env vars are set)
render.experimental.storage.objects.put(
    key="path/to/file.png",
    data=b"binary content",
    content_type="image/png",
)

# Download
obj = render.experimental.storage.objects.get(key="path/to/file.png")

# List
response = render.experimental.storage.objects.list()
```

## Key Value

The Key Value API provides a Redis client backed by Render's managed Key Value service. It supports automatic instance provisioning and configuration sync.

Requires the [`redis`](https://pypi.org/project/redis/) package:

```bash
pip install redis
```

The Key Value provider is async-only and must be used with `RenderAsync`:

### Basic usage

You can look up an instance by name and the SDK will create it if it doesn't exist. Note that the workspace ID needs to be set, either through the `RENDER_WORKSPACE_ID` environment variable or by passing the `owner_id` explicitly when calling the SDK:

```python
import asyncio
from render import RenderAsync
from render.experimental.key_value import NameOwnerIdOptions

async def main():
    render = RenderAsync()

    # Returns a configured redis.asyncio.Redis client
    redis = await render.experimental.key_value.new_client(
        NameOwnerIdOptions(
            name="my-cache",
            owner_id="tea-abcdefghijklmnopqrst",
        )
    )

    await redis.set("key", "value")
    value = await redis.get("key")

    await redis.aclose()

asyncio.run(main())
```

### Look up by service ID

If you already have a Render Key Value service ID, pass it directly to skip the name lookup:

```python
from render.experimental.key_value import ServiceIdOptions

redis = await render.experimental.key_value.new_client(
    ServiceIdOptions(service_id="redis-xxxxxxxxxxxx")
)
```

### Auto-provisioning with configuration

Pass an `auto_provision` configuration to control the plan and eviction policy. If the instance doesn't exist it will be created; if it exists but its settings differ they will be updated:

```python
from render.experimental.key_value import InstanceConfiguration, NameOwnerIdOptions

redis = await render.experimental.key_value.new_client(
    NameOwnerIdOptions(
        name="my-cache",
        auto_provision=InstanceConfiguration(
            plan="starter",
            maxmemory_policy="allkeys-lru",
        ),
    )
)
```

Set `auto_provision=False` to disable all automatic changes and raise if the instance is not found:

```python
redis = await render.experimental.key_value.new_client(
    NameOwnerIdOptions(name="my-cache", auto_provision=False)
)
```

### Connection info only

Use `connection_info` when you need the host and port rather than a ready-made client:

```python
info = await render.experimental.key_value.connection_info(
    NameOwnerIdOptions(name="my-cache")
)
print(f"redis://{info.host}:{info.port}")
```

### Local development

When `RENDER_USE_LOCAL_DEV=true` is set, the client connects to a local Valkey instance instead of the Render API. The easiest option for getting a local instance running is to use the [official Valkey Docker image](https://hub.docker.com/r/valkey/valkey):

```bash
docker run -p 6379:6379 valkey/valkey
```

When using the SDK in local development mode, the host and port default to `localhost:6379`. They can be overridden with the environment variables `RENDER_LOCAL_REDIS_HOST` and `RENDER_LOCAL_REDIS_PORT`.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and [tox](https://tox.wiki/) for testing across multiple Python versions.

### Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run tox -e coverage

# Run tests across all Python versions
uv run tox

# Run specific Python version
uv run tox -e py313
```

### Code Quality

```bash
# Check formatting and linting
uv run tox -e format
uv run tox -e lint

# Fix formatting issues
uv run tox -e format-fix
uv run tox -e lint-fix

# Run all quality checks
uv run tox -e format,lint
```

### Supported Python Versions

- Python 3.10+
- Tested on Python 3.10, 3.11, 3.12, 3.13, 3.14
