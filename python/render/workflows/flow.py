"""Durable flows."""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import (
    Concatenate,
    Generic,
    ParamSpec,
    Protocol,
    TypeVar,
)

from render.workflows.context import FlowContext

P = ParamSpec("P")
R = TypeVar("R")


class FlowDefinition(Generic[P, R]):
    """A registered flow."""

    def __init__(
        self,
        func: Callable[Concatenate[FlowContext, P], R],
        name: str,
    ) -> None:
        # Same ordering as TaskDefinition: update_wrapper copies func.__dict__
        # over this object, so the assignments below come after it.
        functools.update_wrapper(self, func)  # type: ignore[arg-type]
        self.func = func
        self.name = name

    def __repr__(self) -> str:
        return f"FlowDefinition(name={self.name!r})"


class BoundFlowDecorator(Protocol):
    """The decorator produced by calling ``Workflows.flow(...)`` with options."""

    def __call__(
        self,
        func: Callable[Concatenate[FlowContext, P], R],
        /,
    ) -> FlowDefinition[P, R]: ...
