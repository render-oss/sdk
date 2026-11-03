"""Data models for the workflow callback API.

Only the fields the runner actually exchanges with the SDK server are
modelled here, grouped by the part of the API they belong to. Each model
is a dataclass declaration that inherits its ``to_dict`` from
:class:`~render.workflows._models.wire.Wire`; ``from_dict`` is explicit on
the classes the runner parses off the wire.

The package depends only on the standard library so it can sit on the
worker hot path — defining or running a task does not pull in
``httpx`` or ``attrs``.
"""
