#!/usr/bin/env python3
"""Generate sync variants of async source files.

Usage:
    python scripts/unasync.py          # Generate sync files
    python scripts/unasync.py --check  # Check that generated files are up to date
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Root of the Python SDK
SDK_ROOT = Path(__file__).resolve().parent.parent

# (async source, generated sync target)
FILE_PAIRS = [
    (
        SDK_ROOT / "render_sdk" / "experimental" / "object" / "api.py",
        SDK_ROOT / "render_sdk" / "experimental" / "object" / "api_sync.py",
    ),
    (
        SDK_ROOT / "render_sdk" / "experimental" / "object" / "client.py",
        SDK_ROOT / "render_sdk" / "experimental" / "object" / "client_sync.py",
    ),
]

# Simple string replacements applied line-by-line
SYNTAX_REPLACEMENTS = [
    ("async def ", "def "),
    ("await ", ""),
    ("async for ", "for "),
    ("async with ", "with "),
    ("AsyncIterator", "Iterator"),
    ("asyncio_detailed", "sync_detailed"),
    ("httpx.AsyncClient", "httpx.Client"),
    ("aiter_bytes", "iter_bytes"),
    ("_file_to_async_iterable", "_file_to_iterable"),
    # Import path renames
    (
        "from render_sdk.experimental.object.api import",
        "from render_sdk.experimental.object.api_sync import",
    ),
    (
        "from render_sdk.client.util import",
        "from render_sdk.client.util_sync import",
    ),
    # Docstring fixups (artifacts of mechanical transformation)
    ("to an async byte iterator", "to a byte iterator"),
    ("or an async byte iterator", "or a byte iterator"),
    ("or async byte iterator", "or byte iterator"),
]

# Class renames use word-boundary regex to prevent substring matching
# (e.g. ObjectClient inside ScopedObjectClient).
CLASS_RENAMES = [
    ("ScopedObjectClient", "SyncScopedObjectClient"),
    ("ObjectClient", "SyncObjectClient"),
    ("ObjectApi", "SyncObjectApi"),
]

HEADER = (
    "# Auto-generated sync version. "
    "Do not edit \u2014 run scripts/unasync.py instead.\n\n"
)


def transform(source: str) -> str:
    """Apply unasync transformations to source code."""
    lines = source.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        for old, new in SYNTAX_REPLACEMENTS:
            line = line.replace(old, new)
        for old, new in CLASS_RENAMES:
            line = re.sub(r"\b" + re.escape(old) + r"\b", new, line)
        out.append(line)
    return HEADER + "".join(out)


def _format_with_ruff(path: Path) -> None:
    """Run ruff lint --fix + format on a file in place."""
    subprocess.run(  # noqa: S603
        ["ruff", "check", "--fix", "--quiet", str(path)],  # noqa: S607
        check=False,
    )
    subprocess.run(  # noqa: S603
        ["ruff", "format", "--quiet", str(path)],  # noqa: S607
        check=False,
    )


def _generate_and_format(src: Path) -> str:
    """Transform source and return ruff-formatted output."""
    raw = transform(src.read_text())
    # Write to a temp file so ruff can format it
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)
    try:
        _format_with_ruff(tmp_path)
        return tmp_path.read_text()
    finally:
        tmp_path.unlink()


def main() -> int:
    check = "--check" in sys.argv

    errors: list[str] = []
    for src, dst in FILE_PAIRS:
        if not src.exists():
            errors.append(f"Source file not found: {src}")
            continue

        generated = _generate_and_format(src)

        if check:
            if not dst.exists():
                errors.append(f"Generated file missing: {dst}")
            elif dst.read_text() != generated:
                errors.append(f"Generated file out of date: {dst}")
        else:
            dst.write_text(generated)
            print(f"Generated {dst.relative_to(SDK_ROOT)}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    if check:
        print("All generated files are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
