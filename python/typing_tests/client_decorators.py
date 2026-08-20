"""What the UDS client's error decorators promise to preserve, asserted against mypy.

``_retry_transient_errors`` and ``_translate_errors`` wrap every public
``UDSClient`` method. These assertions pin that the wrapped methods keep
their real signatures instead of collapsing to ``Any``.

Never executed. See README.md in this directory.
"""

from typing_extensions import assert_type

from render_sdk.workflows._callback_models import (
    InputResponse,
    RunSubtaskRequest,
    RunSubtaskResponse,
    Tasks,
)
from render_sdk.workflows.client import (
    CallbackRequest,
    Status,
    TaskResultResponse,
    UDSClient,
    _retry_transient_errors,
)

# --- decorated methods ------------------------------------------------------


async def methods_keep_their_return_types(client: UDSClient) -> None:
    """A decorated method resolves to its declared return type, not Any."""
    assert_type(await client.get_input(), InputResponse)
    assert_type(await client.get_task_result("run-id"), TaskResultResponse)
    callback = CallbackRequest(status=Status.SUCCESS)
    assert_type(await client.post_callback(callback), None)
    assert_type(await client.register_tasks(Tasks(tasks=[])), None)
    assert_type(
        await client._start_subtask(RunSubtaskRequest(task_name="t")),
        RunSubtaskResponse,
    )


async def methods_keep_their_parameter_names(client: UDSClient) -> None:
    await client.get_task_result(task_run_id="run-id")
    await client.post_callback(callback_request=CallbackRequest(status=Status.ERROR))


async def methods_reject_bad_calls(client: UDSClient) -> None:
    # Wrong argument type.
    await client.get_task_result(123)  # type: ignore[arg-type]

    # Missing argument.
    await client.get_task_result()  # type: ignore[call-arg]

    # Extra argument.
    await client.get_input("extra")  # type: ignore[call-arg]

    # Wrong result type.
    wrong: str = await client.get_task_result("run-id")  # type: ignore[assignment]
    del wrong


# --- the decorator applied to a standalone function -------------------------


async def _probe(a: int, b: str = "x") -> bool:
    return True


_wrapped = _retry_transient_errors(_probe)


async def the_decorator_preserves_a_standalone_signature() -> None:
    assert_type(await _wrapped(1), bool)
    assert_type(await _wrapped(1, b="y"), bool)
    await _wrapped("not an int")  # type: ignore[arg-type]
