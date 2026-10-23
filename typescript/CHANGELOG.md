# Changelog

All notable changes to the `@renderinc/sdk` TypeScript SDK will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- (Sandbox) `sandboxes.create()` accepts `idleTimeoutSeconds`; use `0` to disable automatic idle suspension.

## [1.4.0] - 2026-10-21

### Added

- (Sandbox) `sandboxes.create()` accepts any `plan` string. Returned `Sandbox` values expose `idleTimeoutSeconds`.
- (Sandbox) `exec()`, `upload()`, and `download()` throw `SandboxEndedError` when the sandbox is `terminated` or `errored`, for example because it passed its timeout. The error names the sandbox and its status so callers can tell it apart from a sandbox that is still starting.

### Changed

- (Sandbox) Errors from `create()`, `list()`, `listGroups()`, and `snapshots.list()` name the workspace the SDK used, which makes a stale `RENDER_WORKSPACE_ID` easier to spot.
- (Workflows) Idempotency keys are scoped to the workflow rather than a single workflow version, so the same key resolves to the original run across deploys. This is a documentation change; the SDK sends the key as before.
- **Breaking:** (REST API) Removed the unused `update-sandbox-exec` operation and its request and response types. Error codes include `sandbox_group_suspended` and `sandbox_group_limit_reached`.

### Fixed

- (Sandbox) `SandboxDownload.data` is typed as an `ArrayBuffer`-backed buffer, so it passes to Web and Bun APIs that take `Uint8Array<ArrayBuffer>`, such as `new Blob()` or `Bun.gunzipSync()`, under TypeScript 5.7 and later.

## [1.3.0] - 2026-10-17

### Added

- (Sandbox) `sandboxes.create()` accepts `networkPolicy: { type: "allow-list", rules: [{ domain: "pypi.org" }] }` to restrict outbound traffic. Rules support domain names and wildcard domains such as `*.pypi.org`. A rule's `protocol` defaults to `"https"`. The SDK exports `SandboxNetworkPolicy` and `SandboxEgressRule`.
- (REST API) Generated types include flows, flow runs, run steps, and individual build retrieval.

### Changed

- **Breaking:** (Sandbox) `SandboxCreateInput.networkPolicy` uses `type` instead of `default`. An `allow-list` policy requires `rules`. The other policy types do not accept `rules`.
- **Breaking:** (REST API) Removed Blueprint creation and its request and response types. Build source Git fields use `dockerContext` instead of `baseDir`. Build list entries contain `build` and `cursor` instead of a bare build.
- (REST API) Service creation can omit `runtime` when `buildSourceId` is set. `autoDeploy` is deprecated; use `autoDeployTrigger`. Sandbox status includes `suspending`. Service event list entries include a `cursor`.
- (Workflows) The SDK sends import and startup timestamps with the initial input request. The runtime can use these timestamps to measure SDK import and startup time.

### Fixed

- (Sandbox) `get()`, `list()`, `listGroups()`, `terminate()`, `exec()`, `upload()`, and `download()` throw `ClientError` or `ServerError` when the API returns an error status with an empty body. These responses could previously appear to succeed or cause a later `TypeError`.

## [1.2.0] - 2026-09-23

### Added

- (Workflows) `startTask()` and `runTask()` accept an options object with an `idempotencyKey`, which makes starting a run safe to retry: repeating a call with the same key within 24 hours returns the run the first call started. The third argument still accepts a bare `AbortSignal`
- (Workflows) `ctx.metadata` exposes `taskRunId`, `rootTaskRunId` and `parentTaskRunId` for the running task. The IDs come from the task's initial input, so reading them does not make a network request. For a root run, `rootTaskRunId` equals `taskRunId` and `parentTaskRunId` is `undefined`
- (Sandbox) Snapshot names: `snapshots.create()` accepts `name`, and `sandboxes.create()` accepts `snapshotName` to start from the snapshot that name resolves to. `SandboxCreateInput` takes either `snapshotId` or `snapshotName`, not both
- (Sandbox) The `Sandbox` type is exported, and `sandboxes.create()` is typed to return it

### Changed

- Regenerated the REST API types from the latest OpenAPI schema: blueprint creation, `includePreviews` when listing build sources, and allowed domains on sandbox network policies. `Deploy` no longer has a `buildId` field

### Fixed

- The npm package no longer ships `e2e-helpers` or `.d.ts.map` files
- `js-yaml` is pinned to 4.3.2 or later through an npm override, which resolves GHSA-2883-xcg3-v3hh

## [1.1.0] - 2026-09-10

### Added

- (Sandbox) `sandboxes.listGroups()`, returning `SandboxGroupWithCursor[]` and taking an optional `ownerId`. Alpha guarantees at most one group per workspace, so the array holds zero or one group
- (Sandbox) Sandbox snapshots through `sandboxes.snapshots`, with `create`, `get`, `list` and `delete`
- (Sandbox) Snapshot `kind` in `snapshots.create()`: `filesystem` captures the writable filesystem, `runtime` also captures memory and CPU state; optional `expiresAt`
- (Sandbox) `sandboxes.create()` accepts `snapshotId` to start from a snapshot instead of the base image
- (Sandbox) Snapshot error types `SandboxSnapshotNotFoundError`, `SandboxSnapshotNotReadyError` and `SandboxSnapshotPlanMismatchError`, each exposing the API error `code` when the API sends one
- (Key Value) The size-based plan names (`256mb`, `1g`, `5g`, `10g`, `20g`, `40g`) are accepted by `autoProvision.plan` on `keyValue.connectionInfo()`
- `ClientError` exposes the API error `code` when the response includes one

## [1.0.0]

### Changed

- **Breaking** (Workflows) Tasks now take a `TaskContext` as their first parameter, followed by their inputs
- **Breaking** (Workflows) Subtasks are reached through the context instead of by calling a task directly: `ctx.run(task, input)` runs it on its own compute and resolves with its result
- **Breaking** (Workflows) `task()` returns a `TaskDefinition` rather than a wrapped function. A definition is not callable; use `ctx.run` to schedule it, or its `func` property to invoke it in-process
- **Breaking** (Workflows) `TaskFunction` now takes a `TaskContext` as its first parameter
- **Breaking** (Workflows) Removed `getCurrentContext` and `setCurrentContext` — the context is now passed explicitly

## [0.7.0] - 2026-08-19

### Added

- Experimental Sandbox client
- Sandbox life cycle through `create`, `get`, `list` and `terminate`, filtering a list by one status or several
- Environment variable support in `create()`
- Execution in a Sandbox via streaming `exec`, recording the run command for the execution audit trail
- File transfer to and from a Sandbox with `upload` and `download`

### Changed

- Idempotent subtask submission

### Fixed

- Workflows errors are no longer stringified by the SDK
- Retry the SSE stream on error in `taskRunEvents`
- Void-returning task functions no longer fail

## [0.6.0] - 2026-06-01

### Added

- Experimental Key Value SDK client for provisioning and connecting to Render Key Value (Redis) instances, with automatic provisioning and service configuration sync
- Local development support for Key Value client creation

### Fixed

- Don't error when no API token is set in dev mode
- Preserve JSDoc comments in build output

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
- Renamed experimental blob storage API to object storage (Blob*-> Object*)
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
