# Changelog

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
