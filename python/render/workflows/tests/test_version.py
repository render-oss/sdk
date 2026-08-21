"""Guard against version drift between render.__version__ and pyproject.toml.

The two values are maintained separately and once diverged for months
(__version__ reported 0.8.0 while the distribution was published as 1.0.0).
importlib.metadata reads the installed dist-info, which comes from
pyproject.toml, so this test fails whenever one is bumped without the other.
"""

import importlib.metadata

import render


def test_version_matches_distribution_metadata() -> None:
    assert render.__version__ == importlib.metadata.version("render")
