# Changelog

## [0.6.0] - 2026-03-05

### Added

- `SUCCEEDED` workflow task run status for forward-compatibility with upcoming status rename

### Changed

- **Breaking:** Workflows `TaskIdentifier` type renamed to `TaskSlug`
- **Breaking:** Workflows `task_identifier` parameter renamed to `task_slug` in `run_task()` and `start_task()`
- **Breaking:** Workflows `list_task_runs()` now returns `list[TaskRunWithCursor]` (use `.task_run` to access the `TaskRun`)

## [0.5.0] - 2026-02-25

### Added

- Synchronous `Render` client for use with Flask, Django, and other sync frameworks
- `start_task()` method for fire-and-forget and deferred-wait task invocation patterns for workflows

### Changed

- **Breaking:** `Render` is now the synchronous client; use `RenderAsync` for async
- **Breaking:** `run_task()` now starts and waits for completion, returning `TaskRunDetails`; use `start_task()` for the previous `run_task()` behavior for workflows
- **Breaking:** Renamed workflows task-level `timeout` parameter to `timeout_seconds`
- Migrated from Poetry to uv for dependency management and builds

### Fixed

- Treat `CANCELED` as a terminal task run status to prevent hanging on canceled tasks for workflows

## [0.4.0] - 2026-02-20

### Added

- E2E tests for object storage
- Automatic retries with exponential backoff for transient errors and rate limits for workflows

### Changed

- **Breaking:** Moved `client.stream_task_run_events()` to `workflows.task_run_events()`
- Accept `RENDER_OWNER_ID` and `RENDER_REGION` environment variables for object storage
- Updated README and workflows example code

### Fixed

- **Breaking:** Remove `auto_start` to avoid `atexit` conflicts for workflows task definition
- Fix `render-workflows` CLI wrapper when used as Render service start command

## [0.3.0] - 2026-02-11

### Added

- Cursor-based pagination support for list objects (`hasNext`, `nextCursor` fields)

### Changed

- Sanitize storage error messages to hide provider details
- Updated README with `@app.task()` pattern

### Fixed

- Object file streaming uploads
- Better detection and handling of error messages
- Removed client-side region validation for forward compatibility
- Removed timeouts on httpx get/put from presigned URLs
- Raise `ClientError` when uploading objects larger than server allows
- Allow uploading streams of size 0

## [0.2.0] - 2026-02-02

### Added

- `Workflows` class for defining and registering tasks (`from render_sdk import Workflows`)
- `Render` class as primary entry point for REST API access
- `timeout_seconds` parameter for specifying timeout during task definition
- `plan` parameter for specifying resource plan during task definition
- `render-workflows` CLI command for running workflow applications
- Experimental object storage API
- `list()` method for object storage with cursor pagination

### Changed

- Regenerated API clients from latest OpenAPI spec

### Fixed

- Renamed `wait_duration` to `wait_duration_ms` in retry config
