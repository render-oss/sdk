# Render SDK for Python

The official Python SDK for Render. Define Workflow tasks, manage task runs, and access experimental platform features like object storage.

**⚠️ Early Access:** This SDK is in early access and subject to breaking changes without notice.

## Installation

```bash
pip install render_sdk
```

## Usage

### Defining Tasks

Use the `Workflows` class to define and register tasks:

```python
from render_sdk import Workflows

app = Workflows()

@app.task
def square(a: int) -> int:
    """Square a number."""
    return a * a


@app.task
async def add_squares(a: int, b: int) -> int:
    """Add the squares of two numbers."""
    result1 = await square(a)
    result2 = await square(b)
    return result1 + result2
```

You can also specify task parameters like `retry`, `timeout`, and `plan`:

```python
from render_sdk import Retry, Workflows

app = Workflows(
    default_retry=Retry(max_retries=3, wait_duration_ms=1000),
    default_timeout=300,
    default_plan="standard",
)

@app.task(timeout=60, plan="starter")
def quick_task(x: int) -> int:
    return x + 1

@app.task(retry=Retry(max_retries=5, wait_duration_ms=2000, backoff_scaling=2.0))
def retryable_task(x: int) -> int:
    return x * 2
```

You can combine tasks from multiple modules using `Workflows.from_workflows()`:

```python
from tasks_a import app as app_a
from tasks_b import app as app_b

combined = Workflows.from_workflows(app_a, app_b)
```

### Running the Local Task Server

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

### Running Tasks

Use the `Render` client to run tasks and monitor their status:

```python
from render_sdk import Render
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import TaskRunError

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

#### Async Usage

For async contexts (e.g. FastAPI), use `RenderAsync`:

```python
import asyncio
from render_sdk import RenderAsync

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

### Object Storage

```python
from render_sdk import Render

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

### Key Value

The Key Value API provides a Redis client backed by Render's managed Key Value service. It supports automatic instance provisioning and configuration sync.

Requires the [`redis`](https://pypi.org/project/redis/) package:

```bash
pip install redis
```

The Key Value provider is async-only and must be used with `RenderAsync`:

#### Basic usage

You can look up an instance by name and the SDK will create it if it doesn't exist. Note that the workspace ID needs to be set, either through the `RENDER_WORKSPACE_ID` environment variable or by passing the `owner_id` explicitly when calling the SDK:

```python
import asyncio
from render_sdk import RenderAsync
from render_sdk.experimental.key_value import NameOwnerIdOptions

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

#### Look up by service ID

If you already have a Render Key Value service ID, pass it directly to skip the name lookup:

```python
from render_sdk.experimental.key_value import ServiceIdOptions

redis = await render.experimental.key_value.new_client(
    ServiceIdOptions(service_id="redis-xxxxxxxxxxxx")
)
```

#### Auto-provisioning with configuration

Pass an `auto_provision` configuration to control the plan and eviction policy. If the instance doesn't exist it will be created; if it exists but its settings differ they will be updated:

```python
from render_sdk.experimental.key_value import InstanceConfiguration, NameOwnerIdOptions

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

#### Connection info only

Use `connection_info` when you need the host and port rather than a ready-made client:

```python
info = await render.experimental.key_value.connection_info(
    NameOwnerIdOptions(name="my-cache")
)
print(f"redis://{info.host}:{info.port}")
```

#### Local development

When `RENDER_USE_LOCAL_DEV=true` is set, the client connects to a local Valkey instance instead of the Render API. The easiest option for getting a local instance running is to use the [official Valkey Docker image](https://hub.docker.com/r/valkey/valkey):

```bash
docker run -p 6379:6379 valkey/valkey
```

When using the SDK in local development mode, the host and port default to `localhost:6379`. They can be overridden with the environment variables `RENDER_LOCAL_REDIS_HOST` and `RENDER_LOCAL_REDIS_PORT`.

## Environment Variables

- `RENDER_API_KEY` - Your Render API key (required)
- `RENDER_WORKSPACE_ID` - Default owner ID for object storage (workspace team ID, e.g. `tea-xxxxx`)
- `RENDER_REGION` - Default region for object storage (e.g. `oregon`, `frankfurt`)
- `RENDER_USE_LOCAL_DEV` - Enable local development mode (`true`/`false`)
- `RENDER_LOCAL_DEV_URL` - Local development URL (default: `http://localhost:8120`)
- `RENDER_SDK_MODE` - Task execution mode (`run` or `register`)
- `RENDER_SDK_SOCKET_PATH` - Unix socket path for task communication
- `RENDER_LOCAL_REDIS_HOST` - Custom host for local Redis / Valkey instance (default: `localhost`) (requires `RENDER_USE_LOCAL_DEV=true`)
- `RENDER_LOCAL_REDIS_PORT` - Custom port for local Redis / Valkey instance (default: `6379`) (requires `RENDER_USE_LOCAL_DEV=true`)

## Features

- **REST API Client**: Run, monitor, cancel, and list task runs
- **Task Definition**: Decorator-based task registration with the `Workflows` class
- **Server-Sent Events**: Real-time streaming of task run events
- **Sync & Async**: Synchronous `Render` client (default) and async `RenderAsync` variant
- **Retry Configuration**: Configurable retry behavior with exponential backoff
- **Subtask Execution**: Execute tasks from within other tasks
- **Task Composition**: Combine tasks from multiple modules with `Workflows.from_workflows()`
- **Object Storage**: Experimental object storage API with upload, download, and list
- **Key Value**: Experimental Render Key value client with auto-provisioning and configuration sync

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
