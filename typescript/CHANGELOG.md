# Changelog

All notable changes to the `@renderinc/sdk` TypeScript SDK will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

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
