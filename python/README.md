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

    # Execute subtasks
    result1 = await square(a)
    logger.info(f"Square result: {result1}")
    result2 = await square(b)
    logger.info(f"Square result: {result2}")

    return result1 + result2
```

You can also specify task parameters like `timeout` and `plan`:

```python
@app.task(timeout=60, plan="starter")
def quick_task(x: int) -> int:
    return x + 1
```

### Running the Task Server

Run your workflow application using the CLI command:

```bash
render ea tasks dev -- python main.py
```

### Running Tasks

Use the `Render` client to run tasks and monitor their status:

```python
import asyncio
from render_sdk import Render

async def main():
    render = Render()  # Uses RENDER_API_KEY from environment

    # Run a task and wait for the result
    task_run = await render.workflows.run_task("my-workflow/my-task", {"a": 3})
    result = await task_run
    print(result.results)

    # Or stream task run events directly
    task_run = await render.workflows.run_task("my-workflow/my-task", {"a": 3})
    async for event in render.workflows.task_run_events([task_run.id]):
        print(f"{event.id} status={event.status}")
        if event.error:
            print(f"Error: {event.error}")

asyncio.run(main())
```

### Object Storage

```python
from render_sdk import Render

render = Render()  # Uses RENDER_API_KEY, RENDER_WORKSPACE_ID, RENDER_REGION from environment

# Upload an object (no need to pass owner_id/region when env vars are set)
await render.client.experimental.storage.objects.put(
    key="path/to/file.png",
    data=b"binary content",
    content_type="image/png",
)

# Download
obj = await render.client.experimental.storage.objects.get(key="path/to/file.png")

# List
response = await render.client.experimental.storage.objects.list()
```

## Environment Variables

- `RENDER_API_KEY` - Your Render API key (required)
- `RENDER_WORKSPACE_ID` - Default owner ID for object storage (workspace team ID, e.g. `tea-xxxxx`)
- `RENDER_REGION` - Default region for object storage (e.g. `oregon`, `frankfurt`)

## Features

- Decorator-based task registration
- Type-safe task execution
- Retry configuration support
- Environment-based configuration
- Generated client for SDK server communication

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
