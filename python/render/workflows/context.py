"""Execution context handed to every task."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ParamSpec, Protocol, TypeVar

if TYPE_CHECKING:
    from render.workflows.client import UDSClient
    from render.workflows.task import TaskDefinition

P = ParamSpec("P")
R = TypeVar("R")


class TaskContext(Protocol):
    """
    The first argument of every task.

    The context is how a task reaches the rest of the workflow system.
    """

    async def run(
        self, task: TaskDefinition[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        """
        Run another task on its own compute and wait for its result.

        Args:
            task: The task to run.
            *args: Positional inputs for the task.
            **kwargs: Named inputs for the task. Cannot be combined with *args.

        Returns:
            The task's return value.

        Raises:
            TaskRunError: If the task run fails.
        """
        ...


class WorkflowTaskContext(TaskContext):
    """The TaskContext handed to tasks by the workflow runtime."""

    def __init__(self, client: UDSClient) -> None:
        self._client = client

    async def run(
        self, task: TaskDefinition[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        return await self._client.run_subtask(
            task.name, _encode_input(task.name, args, kwargs)
        )


def _encode_input(
    task_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> list[Any] | dict[str, Any]:
    """
    Shape call arguments into the wire format.

    Positional arguments travel as a list, named parameters as a dict; the two
    cannot be mixed because the receiving end has no way to merge them.
    """
    if args and kwargs:
        raise ValueError(
            f"Cannot mix positional and keyword arguments when calling "
            f"'{task_name}'. Use either positional arguments "
            f"(e.g., ctx.run(task, arg1, arg2)) or keyword arguments "
            f"(e.g., ctx.run(task, param1=value1)), but not both."
        )

    if kwargs:
        return dict(kwargs)
    return list(args)
