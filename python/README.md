# Render Workflows Python SDK

A Python SDK for defining and executing tasks in the Render Workflows system.

**⚠️ Early Access:** This SDK is in early access and subject to breaking changes without notice.

## Installation

```bash
pip install render_sdk
```

## Usage

### Defining Tasks

Use the `@task` decorator to define tasks:

```python
from render_sdk.workflows import task

@task
def square(a: int) -> int:
    return a * a

@task
def add_squares(a: int, b: int) -> int:
    result1 = ctx.execute_task(square, a)
    result2 = ctx.execute_task(square, b)
    return result1 + result2
```

### Running the Task Server

```python
from render_sdk.workflows import start

if __name__ == "__main__":
    start()
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
