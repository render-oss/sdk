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
