"""What `ctx.run` promises to infer, asserted against mypy.

Never executed. See README.md in this directory.
"""

from typing import ParamSpec, TypeVar

from typing_extensions import assert_type

from render import Retry, Workflows
from render.workflows import TaskContext, TaskDefinition, task

P = ParamSpec("P")
R = TypeVar("R")

app = Workflows()


# --- sync body -------------------------------------------------------------


@app.task
def sync_bare(ctx: TaskContext, a: int) -> int:
    return a


@app.task(timeout_seconds=60, plan="starter")
def sync_with_options(ctx: TaskContext, a: int) -> int:
    return a


# --- async body ------------------------------------------------------------


@app.task
async def async_bare(ctx: TaskContext, name: str) -> str:
    return name


@app.task(retry=Retry(max_retries=2, wait_duration_ms=100))
async def async_with_options(ctx: TaskContext, name: str) -> str:
    return name


# --- no inputs, and variadic inputs ----------------------------------------


@app.task
async def no_inputs(ctx: TaskContext) -> bool:
    return True


# --- the module-level decorator, used by internal-examples -----------------


@task
def module_level(ctx: TaskContext, a: int) -> int:
    return a


async def run_infers_the_task_result(ctx: TaskContext) -> None:
    """A run resolves to the task's return type, not Any and not Never."""
    assert_type(await ctx.run(sync_bare, 1), int)
    assert_type(await ctx.run(sync_with_options, 1), int)
    assert_type(await ctx.run(async_bare, "x"), str)
    assert_type(await ctx.run(async_with_options, "x"), str)
    assert_type(await ctx.run(no_inputs), bool)
    assert_type(await ctx.run(module_level, 1), int)


async def run_rejects_bad_calls(ctx: TaskContext) -> None:
    """Each ignore below asserts that the call is an error.

    warn_unused_ignores is on for this directory, so an ignore whose error
    stops occurring becomes a failure in its own right.
    """
    # Wrong input type.
    await ctx.run(sync_bare, "not an int")  # type: ignore[arg-type]

    # Too few inputs.
    await ctx.run(sync_bare)  # type: ignore[call-arg]

    # Too many inputs.
    await ctx.run(sync_bare, 1, 2)  # type: ignore[call-arg]

    # Wrong result type. Reported as arg-type: mypy resolves the overload
    # against the expected result before it gets to the assignment.
    wrong: str = await ctx.run(sync_bare, 1)  # type: ignore[arg-type]
    del wrong


def definitions_are_not_callable(ctx: TaskContext) -> None:
    """Scheduling goes through the context; a definition is inert data."""
    sync_bare(ctx, 1)  # type: ignore[operator]


def definition_exposes_its_parts() -> None:
    """The registered name, and the undecorated function for in-process use."""
    assert_type(sync_bare.name, str)


class StandInContext:
    """A test double satisfies TaskContext structurally, without subclassing.

    Note it has to mirror the ParamSpec signature exactly; a looser
    ``*args: object`` stand-in does not conform.
    """

    async def run(
        self, task: TaskDefinition[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        raise NotImplementedError


def a_stand_in_satisfies_the_protocol() -> None:
    ctx: TaskContext = StandInContext()
    del ctx
