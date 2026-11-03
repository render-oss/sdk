"""What FlowContext.invoke and step promise to callers, asserted against mypy.

Never executed. See README.md in this directory.
"""

from typing_extensions import assert_type

from render import FlowContext, Retry, TaskContext, Workflows

app = Workflows()


@app.task
def charge(ctx: TaskContext, order_id: str) -> str:
    return order_id


def sync_step(order_id: str, total: int, express: bool) -> dict[str, int]:
    return {order_id: total}


def sum_totals(totals: list[float]) -> float:
    return sum(totals)


def steps_return_their_results(ctx: FlowContext) -> None:
    retry = Retry(max_retries=3, wait_duration_ms=100)
    assert_type(
        ctx.step("sync_step", sync_step, "o-1", 30, True, retry=retry),
        dict[str, int],
    )
    assert_type(ctx.step("total", sum_totals, [1.5, 2.0]), float)
    assert_type(ctx.step("x", lambda: "x", retry=retry), str)


def a_registered_task_runs_through_invoke(ctx: FlowContext) -> None:
    assert_type(ctx.invoke(charge, "o-1"), str)
    ctx.invoke(sync_step, "o-1", 30, True)  # type: ignore[arg-type]
    ctx.step("charge", charge, "o-1")  # type: ignore[arg-type]


def metadata_is_typed_and_read_only(ctx: FlowContext) -> None:
    assert_type(ctx.metadata.flow_run_id, str)
    ctx.metadata.flow_run_id = "frn-other"  # type: ignore[misc]
