# Render Tasks Python SDK

A Python SDK for defining and executing tasks in the Render workflow system.

## Installation

```bash
pip install render-tasks
```

## Usage

### Defining Tasks

Use the `@task` decorator to define tasks:

```python
from render_tasks import task, TaskContext

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
from render_tasks import start

if __name__ == "__main__":
    start()
```

## Features

- Decorator-based task registration
- Type-safe task execution
- Retry configuration support
- Environment-based configuration
- Generated client for SDK server communication
