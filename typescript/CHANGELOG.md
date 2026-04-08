# Changelog

All notable changes to the `@renderinc/sdk` TypeScript SDK will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.5.1] - 2026-04-07

### Fixed

- (Workflows) Increased retry window from ~2 minutes to ~5 minutes for better resilience to transient failures
- (Workflows) Omit private fields from `TaskRunResult`

## [0.5.0] - 2026-03-05

### Added

- `SUCCEEDED` workflows task run status for forward-compatibility with upcoming status rename
- `TaskRunWithCursor` type export for paginated list responses

### Changed

- **Breaking:** Workflows `taskIdentifier` parameter renamed to `taskSlug` in `startTask()` and `runTask()`
- **Breaking:** Workflows `listTaskRuns()` now returns `TaskRunWithCursor[]` (use `.taskRun` to access the `TaskRun`)

### Fixed

- Object storage: auto-calculate size for string inputs in `put()`, removing need for callers to provide it
- Object storage: replace generic "Unknown error" with typed `ClientError`/`ServerError` including HTTP status codes

## [0.4.1] - 2026-02-25

### Fixed

- Treat `CANCELED` as a terminal task run status to prevent hanging on canceled tasks for workflows

## [0.4.0] - 2026-02-20

### Added

- `startTask()` method that decouples task invocation from event streaming for workflows
- `taskRunEvents()` method on `WorkflowsClient` for streaming run events from workflows
- Automatic retries with exponential backoff for transient errors and rate limits for workflows
- Accept `RENDER_OWNER_ID` and `RENDER_REGION` environment variables for object storage

### Changed

- Updated README with Bun installation instructions

## [0.3.0] - 2026-02-11

### Added
- Added `list()` method to `ObjectClient` and `ScopedObjectClient` with cursor-based pagination
- Added Bun runtime compatibility for object storage uploads

### Fixed
- Fixed `Content-Length` calculation in workflows UDS client for correct multi-byte UTF-8 handling
- Improved validation of object file sizes

## [0.2.1] - 2026-01-29

### Changed
- Updated package name in README from @render/sdk to @renderinc/sdk
- Renamed experimental blob storage API to object storage (Blob* -> Object*)
- Switched internal workflows task communication from SSE to HTTP requests

## [0.2.0] - 2026-01-26

### Added
- Add experimental blob storage API with `BlobClient` and `ScopedBlobClient`
- Add plan support for task execution
- Add per-task timeout override via `timeoutSeconds` option

### Changed
- Auto-start task server on task registration (no need to call `startTaskServer()` manually)
- Rename `wait_duration` to `wait_duration_ms` for cross-SDK consistency
- Move generated API schema to `generated/` directory

## [0.1.0] - 2025-12-15

### Added
- Add initial TypeScript SDK for Render Workflows
- Add task registration and execution via `@renderinc/sdk/workflows`
- Add `TaskContext` for task metadata and subtask execution
- Add configurable retry policies with exponential backoff
- Add generated OpenAPI types for full type safety
