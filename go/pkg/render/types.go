package render

// Re-export commonly used types from the generated client
// This allows users to avoid importing internal packages

import (
	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	workflows "github.com/render-oss/sdk/go/pkg/render/internal/client/workflows"
)

// Types from workflows package
type (
	TaskIdentifier = workflows.TaskIdentifier
	TaskData       = workflows.TaskData
	TaskRun        = workflows.TaskRun
	TaskRunDetails = workflows.TaskRunDetails
	TaskRunStatus  = workflows.TaskRunStatus
	RunTask        = workflows.RunTask
)

// Types from client package
type (
	ListTaskRunsParams = client.ListTaskRunsParams
	LimitParam         = client.LimitParam
	CursorParam        = client.CursorParam
	OwnerIdParam       = client.OwnerIdParam
)

// Constants for TaskRunStatus
const (
	TaskRunStatusPending   = workflows.Pending
	TaskRunStatusRunning   = workflows.Running
	TaskRunStatusCompleted = workflows.Completed
	TaskRunStatusFailed    = workflows.Failed
)
