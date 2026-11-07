package render

import (
	"context"
	"fmt"

	"github.com/render-oss/sdk/go/pkg/render/internal/client"
	workflows "github.com/render-oss/sdk/go/pkg/render/internal/client/workflows"
)

// WorkflowsService handles workflow-related API operations
type WorkflowsService struct {
	client *Client
}

type RunTaskOption func(*RunTask)

// WithIdempotencyKey makes starting a task run safe to retry. Repeating a call
// with the same key within 24 hours returns the task run the first call
// started instead of starting another one. Keys are scoped to a single
// workflow version.
func WithIdempotencyKey(key string) RunTaskOption {
	return func(runTask *RunTask) {
		runTask.IdempotencyKey = &key
	}
}

// TaskRunList is a page of task runs. Pass NextCursor as
// ListTaskRunsParams.Cursor to fetch the next page; it is nil when the page is
// empty.
type TaskRunList struct {
	TaskRuns   []TaskRun
	NextCursor *string
}

// RunTask executes a task using the workflows API
// POST /task-runs
func (w *WorkflowsService) RunTask(ctx context.Context, taskSlug TaskSlug, input TaskData, opts ...RunTaskOption) (*TaskRunWithGet, error) {
	runTask := workflows.RunTask{
		Task:  workflows.TaskSlug(taskSlug),
		Input: workflows.TaskData(input),
	}
	for _, opt := range opts {
		opt(&runTask)
	}

	resp, err := w.client.internal.CreateTaskWithResponse(ctx, runTask)
	if err != nil {
		return nil, fmt.Errorf("failed to make run task request: %w", err)
	}

	if resp.StatusCode() != 202 {
		return nil, apiError("run task", resp.StatusCode(), resp.Body)
	}

	if resp.JSON202 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	taskRun := (*TaskRun)(resp.JSON202)
	return &TaskRunWithGet{
		TaskRun: taskRun,
		client:  w,
	}, nil
}

// GetTaskRun gets details about a specific task run
// GET /task-runs/{taskRunId}
func (w *WorkflowsService) GetTaskRun(ctx context.Context, taskRunID string) (*TaskRunDetails, error) {
	resp, err := w.client.internal.GetTaskRunWithResponse(ctx, taskRunID)
	if err != nil {
		return nil, fmt.Errorf("failed to make get task run request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("get task run", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return (*TaskRunDetails)(resp.JSON200), nil
}

// CancelTaskRun cancels a running task
// DELETE /task-runs/{taskRunId}
func (w *WorkflowsService) CancelTaskRun(ctx context.Context, taskRunID string) error {
	resp, err := w.client.internal.CancelTaskRunWithResponse(ctx, taskRunID)
	if err != nil {
		return fmt.Errorf("failed to make cancel task run request: %w", err)
	}

	if resp.StatusCode() != 204 {
		return apiError("cancel task run", resp.StatusCode(), resp.Body)
	}

	return nil
}

// ListTaskRuns lists task runs with optional filtering
// GET /task-runs
func (w *WorkflowsService) ListTaskRuns(ctx context.Context, params *ListTaskRunsParams) (*TaskRunList, error) {
	resp, err := w.client.internal.ListTaskRunsWithResponse(
		ctx,
		(*client.ListTaskRunsParams)(params),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to make list task runs request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("list task runs", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &TaskRunList{TaskRuns: make([]TaskRun, len(items))}
	for i, item := range items {
		list.TaskRuns[i] = item.TaskRun
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}

// FlowRunList is a page of flow runs. Pass NextCursor as
// ListFlowRunsParams.Cursor to fetch the next page; it is nil when the page is
// empty.
type FlowRunList struct {
	FlowRuns   []FlowRun
	NextCursor *string
}

type RunFlowOption func(*StartFlowRun)

// WithFlowRunIdempotencyKey makes starting a flow run safe to retry. Repeating
// a call with the same key within 24 hours returns the flow run the first call
// started instead of starting another one. Keys are scoped to a single
// workflow.
func WithFlowRunIdempotencyKey(key string) RunFlowOption {
	return func(startFlowRun *StartFlowRun) {
		startFlowRun.IdempotencyKey = &key
	}
}

// RunFlow starts a flow run using the workflows API
// POST /flow-runs
func (w *WorkflowsService) RunFlow(ctx context.Context, flowSlug FlowSlug, input FlowInput, opts ...RunFlowOption) (*FlowRun, error) {
	startFlowRun := workflows.StartFlowRun{
		Flow:  flowSlug,
		Input: input,
	}
	for _, opt := range opts {
		opt(&startFlowRun)
	}

	resp, err := w.client.internal.StartFlowRunWithResponse(ctx, startFlowRun)
	if err != nil {
		return nil, fmt.Errorf("failed to make run flow request: %w", err)
	}

	if resp.StatusCode() != 202 {
		return nil, apiError("run flow", resp.StatusCode(), resp.Body)
	}

	if resp.JSON202 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return resp.JSON202, nil
}

// GetFlowRun gets details about a specific flow run
// GET /flow-runs/{flowRunId}
func (w *WorkflowsService) GetFlowRun(ctx context.Context, flowRunID string) (*FlowRunDetails, error) {
	resp, err := w.client.internal.GetFlowRunWithResponse(ctx, flowRunID)
	if err != nil {
		return nil, fmt.Errorf("failed to make get flow run request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("get flow run", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return resp.JSON200, nil
}

// CancelFlowRun cancels a running flow
// DELETE /flow-runs/{flowRunId}
func (w *WorkflowsService) CancelFlowRun(ctx context.Context, flowRunID string) error {
	resp, err := w.client.internal.CancelFlowRunWithResponse(ctx, flowRunID)
	if err != nil {
		return fmt.Errorf("failed to make cancel flow run request: %w", err)
	}

	if resp.StatusCode() != 204 {
		return apiError("cancel flow run", resp.StatusCode(), resp.Body)
	}

	return nil
}

// ListFlowRuns lists flow runs with optional filtering
// GET /flow-runs
func (w *WorkflowsService) ListFlowRuns(ctx context.Context, params *ListFlowRunsParams) (*FlowRunList, error) {
	resp, err := w.client.internal.ListFlowRunsWithResponse(ctx, params)
	if err != nil {
		return nil, fmt.Errorf("failed to make list flow runs request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, apiError("list flow runs", resp.StatusCode(), resp.Body)
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	items := *resp.JSON200
	list := &FlowRunList{FlowRuns: make([]FlowRun, len(items))}
	for i, item := range items {
		list.FlowRuns[i] = item.FlowRun
	}
	if len(items) > 0 {
		list.NextCursor = &items[len(items)-1].Cursor
	}
	return list, nil
}
