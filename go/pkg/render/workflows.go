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

// RunTask executes a task using the workflows API
// POST /task-runs
func (w *WorkflowsService) RunTask(taskIdentifier TaskIdentifier, input TaskData) (*TaskRunWithGet, error) {
	runTask := workflows.RunTask{
		Task:  workflows.TaskIdentifier(taskIdentifier),
		Input: workflows.TaskData(input),
	}

	resp, err := w.client.internal.CreateTaskWithResponse(context.Background(), runTask)
	if err != nil {
		return nil, fmt.Errorf("failed to make run task request: %w", err)
	}

	if resp.StatusCode() != 202 {
		return nil, fmt.Errorf("run task failed with status %d: %s", resp.StatusCode(), resp.Status())
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
// GET /tasks-runs/{taskRunId}
func (w *WorkflowsService) GetTaskRun(taskRunID string) (*TaskRunDetails, error) {
	resp, err := w.client.internal.GetTaskRunWithResponse(context.Background(), taskRunID)
	if err != nil {
		return nil, fmt.Errorf("failed to make get task run request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("get task run failed with status %d: %s", resp.StatusCode(), resp.Status())
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	return (*TaskRunDetails)(resp.JSON200), nil
}

// CancelTaskRun cancels a running task
// DELETE /tasks-runs/{taskRunId}
func (w *WorkflowsService) CancelTaskRun(taskRunID string) error {
	resp, err := w.client.internal.DeleteTaskRunWithResponse(context.Background(), taskRunID)
	if err != nil {
		return fmt.Errorf("failed to make cancel task run request: %w", err)
	}

	if resp.StatusCode() != 204 {
		return fmt.Errorf("cancel task run failed with status %d: %s", resp.StatusCode(), resp.Status())
	}

	return nil
}

// ListTaskRuns lists task runs with optional filtering
// GET /task-runs
func (w *WorkflowsService) ListTaskRuns(params *ListTaskRunsParams) ([]TaskRun, error) {
	resp, err := w.client.internal.ListTaskRunsWithResponse(
		context.Background(),
		(*client.ListTaskRunsParams)(params),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to make list task runs request: %w", err)
	}

	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("list task runs failed with status %d: %s", resp.StatusCode(), resp.Status())
	}

	if resp.JSON200 == nil {
		return nil, fmt.Errorf("unexpected response format")
	}

	// Convert slice of workflows.TaskRun to []TaskRun
	result := make([]TaskRun, len(*resp.JSON200))
	for i, taskRun := range *resp.JSON200 {
		result[i] = TaskRun(taskRun)
	}

	return result, nil
}
