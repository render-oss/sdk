package render

// Re-export commonly used types from the generated client
// This allows users to avoid importing internal packages

import (
	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	workflows "github.com/render-oss/sdk/go/pkg/render/internal/client/workflows"
)

// Types from workflows package
type (
	TaskSlug       = workflows.TaskSlug
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
	ListObjectsParams  = client.ListObjectsParams
	Region             = client.Region
)

// Constants for Region
const (
	RegionFrankfurt = client.Frankfurt
	RegionOhio      = client.Ohio
	RegionOregon    = client.Oregon
	RegionSingapore = client.Singapore
	RegionVirginia  = client.Virginia
)

// Constants for TaskRunStatus
const (
	TaskRunStatusPending   = workflows.Pending
	TaskRunStatusRunning   = workflows.Running
	TaskRunStatusCompleted = workflows.Completed
	TaskRunStatusFailed    = workflows.Failed
)
