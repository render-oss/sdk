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

	FlowSlug       = workflows.FlowSlug
	FlowInput      = workflows.FlowInput
	FlowRun        = workflows.FlowRun
	FlowRunDetails = workflows.FlowRunDetails
	FlowRunStatus  = workflows.FlowRunStatus
	StartFlowRun   = workflows.StartFlowRun
)

// Types from client package
type (
	ListTaskRunsParams = client.ListTaskRunsParams
	ListFlowRunsParams = client.ListFlowRunsParams
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

// Constants for FlowRunStatus
const (
	FlowRunStatusPending   = workflows.FlowRunStatusPending
	FlowRunStatusRunning   = workflows.FlowRunStatusRunning
	FlowRunStatusPaused    = workflows.FlowRunStatusPaused
	FlowRunStatusSucceeded = workflows.FlowRunStatusSucceeded
	FlowRunStatusFailed    = workflows.FlowRunStatusFailed
	FlowRunStatusCanceled  = workflows.FlowRunStatusCanceled
)
