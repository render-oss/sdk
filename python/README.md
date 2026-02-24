# Render Workflows Python SDK

A Python SDK for defining and executing tasks in the Render Workflows system.

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

### Running the Task Server

For local development, use the Render CLI:

```bash
render ea tasks dev -- render-workflows main:app
```

The `render-workflows` CLI takes a `module:app` argument pointing to your `Workflows` instance. You can also call `app.start()` directly if needed.

### Running Tasks

Use the `Render` client to run tasks and monitor their status:

```python
import asyncio
from render_sdk import Render
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import RenderError, TaskRunError

async def main():
    render = Render()  # Uses RENDER_API_KEY from environment

    # run_task() starts a task and returns an awaitable handle.
    # The first await starts the task; the second await waits for completion.
    task_run = await render.workflows.run_task("my-workflow/my-task", [3, 4])
    print(f"Task started: {task_run.id}")

    # Wait for the result
    try:
        result = await task_run
        print(result.results)
    except TaskRunError as e:
        print(f"Task failed: {e}")

    # Get task run details by ID
    details = await render.workflows.get_task_run(task_run.id)
    print(f"Status: {details.status}")

    # Cancel a running task
    task_run2 = await render.workflows.run_task("my-workflow/my-task", [5])
    await render.workflows.cancel_task_run(task_run2.id)

    # Stream task run events
    task_run3 = await render.workflows.run_task("my-workflow/my-task", [6])
    async for event in render.workflows.task_run_events([task_run3.id]):
        print(f"{event.id} status={event.status}")
        if event.error:
            print(f"Error: {event.error}")

    # List recent task runs
    runs = await render.workflows.list_task_runs(ListTaskRunsParams(limit=10))

asyncio.run(main())
```

### Object Storage

```python
from render_sdk import Render

render = Render()  # Uses RENDER_API_KEY, RENDER_WORKSPACE_ID, RENDER_REGION from environment

# Upload an object (no need to pass owner_id/region when env vars are set)
await render.experimental.storage.objects.put(
    key="path/to/file.png",
    data=b"binary content",
    content_type="image/png",
)

# Download
obj = await render.experimental.storage.objects.get(key="path/to/file.png")

# List
response = await render.experimental.storage.objects.list()
```

## Environment Variables

- `RENDER_API_KEY` - Your Render API key (required)
- `RENDER_WORKSPACE_ID` - Default owner ID for object storage (workspace team ID, e.g. `tea-xxxxx`)
- `RENDER_REGION` - Default region for object storage (e.g. `oregon`, `frankfurt`)

## Features

- **REST API Client**: Run, monitor, cancel, and list task runs
- **Task Definition**: Decorator-based task registration with the `Workflows` class
- **Server-Sent Events**: Real-time streaming of task run events
- **Async/Await Support**: Fully async API using `asyncio`
- **Retry Configuration**: Configurable retry behavior with exponential backoff
- **Subtask Execution**: Execute tasks from within other tasks
- **Task Composition**: Combine tasks from multiple modules with `Workflows.from_workflows()`
- **Object Storage**: Experimental object storage API with upload, download, and list

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and [tox](https://tox.wiki/) for testing across multiple Python versions.

### Setup

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Testing

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run tox -e coverage

# Run tests across all Python versions
poetry run tox

# Run specific Python version
poetry run tox -e py313
```

### Code Quality

```bash
# Check formatting and linting
poetry run tox -e format
poetry run tox -e lint

# Fix formatting issues
poetry run tox -e format-fix
poetry run tox -e lint-fix

# Run all quality checks
poetry run tox -e format,lint
```

### Supported Python Versions

- Python 3.10+
- Tested on Python 3.10, 3.11, 3.12, 3.13, 3.14
