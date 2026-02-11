# Changelog

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
