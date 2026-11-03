"""Execution contexts handed to every task and flow."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol, TypeVar

from render.workflows._models.wire import Unset

if TYPE_CHECKING:
    from render.workflows._models.task import InputResponse
    from render.workflows.client import UDSClient
    from render.workflows.task import Retry, TaskDefinition

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class TaskRunMetadata:
    """Run IDs for one task execution.

    IDs are None when unavailable. The root ID is also None when the server
    sends an empty string. Root runs have no parent ID.
    """

    task_run_id: str | None = None
    root_task_run_id: str | None = None
    parent_task_run_id: str | None = None


class TaskContext(Protocol):
    """
    The first argument of every task.

    The context is how a task reaches the rest of the workflow system.
    """

    @property
    def metadata(self) -> TaskRunMetadata:
        """Read-only metadata for this execution, available without a request."""
        ...

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
            TypeError: If ``task`` is a flow.
        """
        ...


@dataclass(frozen=True)
class FlowRunMetadata:
    flow_run_id: str


class FlowContext(Protocol):
    """
    The first argument of every flow.

    Every call on it is a durable step. Flow code must make the same
    ``ctx`` calls in the same order with the same inputs on every replay,
    so put anything non-deterministic, such as I/O, clocks or random values,
    inside a step. Steps run one at a time: each call returns once its
    step finishes.
    """

    @property
    def metadata(self) -> FlowRunMetadata: ...

    def invoke(
        self, task: TaskDefinition[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        """
        Invoke a registered task as its own task run and wait for its result.

        Not supported in flows yet: it raises ``NotImplementedError``.
        Use ``step`` to run a plain function as a step.

        Args:
            task: The task to run.
            *args: Positional inputs for the task.
            **kwargs: Named inputs for the task. Cannot be combined with *args.

        Returns:
            The task's return value.
        """
        ...

    def step(
        self,
        name: str,
        fn: Callable[..., R],
        /,
        *args: Any,
        retry: Retry | None = None,
    ) -> R:
        """
        Run a plain function as an inline step, inside this process.

        Pass the function's arguments positionally, then any options as
        keywords. The function must be sync. It gets no context and can't
        make ``ctx`` calls.

        Args:
            name: The step's name.
            fn: The function to run.
            *args: Positional inputs for the function.
            retry: Retries in-process. Defaults to a single attempt.

        Returns:
            The function's return value.
        """
        ...


class WorkflowTaskContext(TaskContext):
    """The TaskContext handed to tasks by the workflow runtime."""

    def __init__(
        self, client: UDSClient, input_response: InputResponse | None = None
    ) -> None:
        self._client = client
        self._metadata = TaskRunMetadata(
            task_run_id=(
                input_response.task_run_id
                if input_response and not isinstance(input_response.task_run_id, Unset)
                else None
            ),
            root_task_run_id=(
                input_response.root_task_run_id or None
                if input_response
                and not isinstance(input_response.root_task_run_id, Unset)
                else None
            ),
            parent_task_run_id=(
                input_response.parent_task_run_id
                if input_response
                and not isinstance(input_response.parent_task_run_id, Unset)
                else None
            ),
        )

    @property
    def metadata(self) -> TaskRunMetadata:
        return self._metadata

    async def run(
        self, task: TaskDefinition[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        # Imported here because render.workflows.flow imports this module.
        from render.workflows.flow import FlowDefinition

        if isinstance(task, FlowDefinition):
            raise TypeError(f"ctx.run({task.name}): a task can't start a flow")
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
