# Typing tests

These files are never executed. They are checked by mypy, and mypy failing
*is* the test failure. They assert that the generated `render_sdk` mirror is
statically transparent: every `render_sdk` symbol type-checks as the
corresponding `render` type.

Run them with:

- `uv run mypy typing_tests`
- `uv run mypy --strict typing_tests/strict`

`warn_unused_ignores` is on for this directory, so each `# type: ignore[code]`
is an assertion that the error genuinely occurs; if it stops occurring, the
run fails.
