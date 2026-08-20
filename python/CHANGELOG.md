# Changelog

## [1.0.0] - 2026-08-20

### Changed

- **Breaking** (Workflows) Tasks now take a `TaskContext` as their first parameter, followed by their inputs
- **Breaking** (Workflows) Subtasks are reached through the context instead of by awaiting a task directly: `await ctx.run(task, input)` runs it on its own compute and returns its result
- **Breaking** (Workflows) `@app.task` returns a `TaskDefinition` rather than a `TaskCallable`. A definition is not callable; use `ctx.run` to schedule it, or its `func` attribute to invoke it in-process
- **Breaking** (Workflows) Registering a task whose first parameter cannot receive a context now raises `ValueError`
- (Workflows) The context parameter is excluded from the parameter schema sent at registration
- (Workflows) `ctx.run` is fully typed: a task's inputs and result are inferred from its function signature, for sync and async bodies alike
- (Workflows) `TaskContext` is a `Protocol`, so a test can supply its own stand-in without subclassing. The runtime implementation is exported as `WorkflowTaskContext`

## [0.8.0] - 2026-08-19

### Added

- Experimental Sandbox client, async and sync
- Sandbox life cycle through `create`, `from_id`, `list` and `terminate`, filtering a list by one status or several
- Environment variable support in `create()`
- Execution in a Sandbox via streaming `exec`, recording the run command for the execution audit trail
- File transfer to and from a Sandbox with `copy_to` and `copy_from`, for files and directories

### Changed

- Idempotent subtask submission
- Moved `openapi-python-client` to dev dependencies

## [0.7.0] - 2026-06-01

### Added

- Experimental Key Value SDK for provisioning and connecting to Render Key Value (Redis) instances, with automatic provisioning and service configuration sync
- Local development support for Key Value client creation

### Changed

- Lazy-load SDK modules to speed up worker cold start
- Hand-rolled the workflows callback API to slim the worker import graph

### Fixed

- Don't error when no API token is set in dev mode

## [0.6.1] - 2026-04-07

### Fixed

- (Workflows) Also retry on `RemoteProtocolError` failures over Unix domain sockets, and use a longer retry window (5 minutes) to survive server restarts
- (Workflows) Coerce dict retry configs to `Retry` instances at task option construction, fixing possible `AttributeError` during registration
- Handle non-JSON error responses (e.g. plain-text 401) in HTTP decorators instead of surfacing a misleading `JSONDecodeError`

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
