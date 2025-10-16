package executor

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/render-oss/sdk/go/pkg/internal/callbackapi"
	"github.com/render-oss/sdk/go/pkg/internal/task"
)

type Executor struct {
	tasks      *task.Tasks
	callbacker *callbackapi.ClientWithResponses
}

type CompleteTask func(ctx context.Context, taskName string, result []interface{}, err error) error
type ExecuteTask func(taskName string, input ...interface{}) ([]interface{}, error)

func NewExecutor(tasks *task.Tasks, callbacker *callbackapi.ClientWithResponses) *Executor {
	return &Executor{
		tasks:      tasks,
		callbacker: callbacker,
	}
}

func (e *Executor) Execute(ctx context.Context, taskName string, input ...interface{}) error {
	// Ensure the task is registered
	_, err := e.tasks.GetTaskByName(taskName)
	if err != nil {
		return err
	}

	executorContext := newExecutorContext(e.executeSubTask)

	result, err := e.tasks.ExecuteTaskByName(taskName, executorContext, input...)

	return e.completeTask(context.Background(), taskName, result, err)
}

func (e *Executor) executeSubTask(taskName string, input ...interface{}) (_results []interface{}, _err error) {
	ctx := context.Background()
	inputBytes, err := json.Marshal(input)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal input: %w", err)
	}

	taskRun, err := e.callbacker.PostRunSubtaskWithResponse(ctx, callbackapi.PostRunSubtaskJSONRequestBody{
		TaskName: taskName,
		Input:    &inputBytes,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to run task: %w", err)
	}
	if taskRun.StatusCode() != http.StatusOK {
		return nil, fmt.Errorf("failed to kick off subtask")
	}
	if taskRun.JSON200 == nil || taskRun.JSON200.TaskRunId == "" {
		return nil, fmt.Errorf("invalid response from task run")
	}
	subtaskRunID := taskRun.JSON200.TaskRunId

	var resp *callbackapi.SubtaskResultResponse
	for ; ; time.Sleep(time.Second) {
		taskRunDetails, err := e.callbacker.PostGetSubtaskResultWithResponse(ctx, callbackapi.PostGetSubtaskResultJSONRequestBody{
			TaskRunId: subtaskRunID,
		})
		if err != nil {
			return nil, fmt.Errorf("failed to get task run details: %w", err)
		}
		resp = taskRunDetails.JSON200
		if resp == nil || resp.StillRunning {
			continue
		}
		break
	}

	if resp.Complete != nil {
		var result []interface{}
		if err := json.Unmarshal(resp.Complete.Output, &result); err != nil {
			return nil, fmt.Errorf("failed to unmarshal output: %w", err)
		}
		return result, nil
	}
	if resp.Error != nil {
		return nil, fmt.Errorf("task error: %s", resp.Error.Details)
	}
	return nil, fmt.Errorf("invalid task run result format")
}

func (e *Executor) completeTask(ctx context.Context, taskName string, result []interface{}, taskErr error) error {
	output, err := json.Marshal(result)
	if err != nil {
		return fmt.Errorf("failed to marshal output: %w", err)
	}

	var callbackRequest *callbackapi.CallbackRequest

	if taskErr != nil {
		callbackRequest = &callbackapi.CallbackRequest{
			Error: &callbackapi.TaskError{
				Details: taskErr.Error(),
			},
		}
	} else {
		callbackRequest = &callbackapi.CallbackRequest{
			Complete: &callbackapi.TaskComplete{
				Output: output,
			},
		}
	}

	resp, err := e.callbacker.PostCallbackWithResponse(ctx, *callbackRequest)
	if err != nil {
		return err
	}

	if resp.StatusCode() != 200 {
		return fmt.Errorf("callback failed with status code %d", resp.StatusCode())
	}

	return nil
}

type executorContext struct {
	executeTask ExecuteTask
}

func newExecutorContext(executeTask ExecuteTask) *executorContext {
	return &executorContext{
		executeTask: executeTask,
	}
}

func (e *executorContext) ExecuteTask(t task.Task, input ...interface{}) *task.TaskResult {
	taskName, err := task.GetFunctionName(t)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	result, err := e.executeTask(taskName, input...)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	return &task.TaskResult{Result: result}
}
