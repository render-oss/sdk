# Render Workflows Go SDK

A Go SDK for defining and executing tasks in the Render Workflows system.

**⚠️ Early Access:** This SDK is in early access and subject to breaking changes without notice.

## Task metadata

The task context exposes `ctx.Metadata()`, which returns the task run IDs from
the initial input response. It does not make network requests.

```go
metadata := ctx.Metadata()
fmt.Println(metadata.TaskRunID)
fmt.Println(metadata.RootTaskRunID)
fmt.Println(metadata.ParentTaskRunID)
```

For a root run, `RootTaskRunID` equals `TaskRunID` and `ParentTaskRunID` is
empty.

## Development

### Generating the OpenAPI spec

```bash
oapi-codegen -config oapi-generate.yaml ../openapi/openapi.yaml
```
