package executor

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/callbackapi"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
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

	// TODO: Update this once we have sub tasks working
	noOpExecutorContext := newExecutorContext(func(taskName string, input ...interface{}) ([]interface{}, error) {
		return nil, nil
	})

	result, err := e.tasks.ExecuteTaskByName(taskName, noOpExecutorContext, input...)

	return e.completeTask(context.Background(), taskName, result, err)
}

func (e *Executor) completeTask(ctx context.Context, taskName string, result []interface{}, taskErr error) error {
	output, err := json.Marshal(result)
	if err != nil {
		return fmt.Errorf("failed to marshal output: %w", err)
	}

	var callbackRequest *callbackapi.CallbackRequest

	if taskErr != nil {
		isReportedBySdk := true
		callbackRequest = &callbackapi.CallbackRequest{
			Status: callbackapi.Error,
			Error: &callbackapi.TaskError{
				Details:         taskErr.Error(),
				IsReportedBySdk: &isReportedBySdk,
			},
		}
	} else {
		callbackRequest = &callbackapi.CallbackRequest{
			Status: callbackapi.Complete,
			Complete: &callbackapi.TaskComplete{
				Output: output,
			},
		}
	}

	callbackRequest.Metadata = &callbackapi.TaskMetadata{
		TaskName: taskName,
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

	log.Printf("Calling task: %s", taskName)

	result, err := e.executeTask(taskName, input...)
	if err != nil {
		return &task.TaskResult{Error: err}
	}

	log.Printf("Task completed: %s", taskName)

	return &task.TaskResult{Result: result}
}
