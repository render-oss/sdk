// Package tasks provides a workflow SDK for defining and executing tasks in a workflow system.
//
// This package allows you to register task functions and start a task execution server.
// Tasks are functions that accept a TaskContext as their first parameter, followed by
// any number of additional parameters.
//
// Example usage:
//
//	func myTask(ctx tasks.TaskContext, input string) string {
//		return "processed: " + input
//	}
//
//	func main() {
//		err := tasks.RegisterTask(myTask)
//		if err != nil {
//			panic(err)
//		}
//		tasks.Start()
//	}
package tasks

import (
	"context"
	"encoding/json"
	"fmt"
	"runtime/debug"

	"github.com/render-oss/sdk/go/pkg/internal/callbackapi"
	"github.com/render-oss/sdk/go/pkg/internal/executor"
	"github.com/render-oss/sdk/go/pkg/internal/task"
	"github.com/render-oss/sdk/go/pkg/internal/uds"
)

var taskSingleton = task.NewTasks()

func RegisterTask(task task.Task) error {
	return taskSingleton.RegisterTask(task)
}

func MustRegister(task task.Task) {
	err := RegisterTask(task)
	if err != nil {
		panic(fmt.Errorf("failed to register task: %w", err))
	}
}

// RegisterTaskWithOptions registers a task with configuration options
func RegisterTaskWithOptions(t task.Task, options *Options) error {
	return taskSingleton.RegisterTaskWithOptions(t, options)
}

type TaskContext = task.TaskContext
type Options = task.Options
type Retry = task.Retry

// Run is the entrypoint for executing a task. It initiates the callback client,
// and ensures that errors and panics are reported correctly
func Run(ctx context.Context, unixSocketPath string) error {
	callbackerClient, err := uds.NewCallbackClient(unixSocketPath)
	if err != nil {
		return fmt.Errorf("failed to create callback client at %s: %w", unixSocketPath, err)
	}
	if taskErr := executeTaskWithRecovery(ctx, callbackerClient); taskErr != nil {
		resp, err := callbackerClient.PostCallbackWithResponse(ctx, callbackapi.PostCallbackJSONRequestBody{
			Error: taskErr,
		})
		if err != nil || (resp != nil && resp.StatusCode() != 200) {
			return fmt.Errorf("failed to report error to callback client; original error is %s; error from callback is %w", taskErr.Details, err)
		}
	}
	return nil
}

// executeTaskWithRecovery calls executeTask, and wraps the error returned
// (if any) in a *callbackapi.TaskError. If executeTask panics, then the panic
// message and the stack trace get passed upwards.
func executeTaskWithRecovery(ctx context.Context, callbackerClient *callbackapi.ClientWithResponses) (_taskErr *callbackapi.TaskError) {
	defer func() {
		if r := recover(); r != nil {
			stackTrace := string(debug.Stack())
			_taskErr = &callbackapi.TaskError{
				Details:    fmt.Sprintf("task panicked: %v", r),
				StackTrace: &stackTrace,
			}
		}
	}()

	if err := executeTask(ctx, callbackerClient); err != nil {
		return &callbackapi.TaskError{
			Details: fmt.Sprintf("task failed: %v", err),
		}
	}
	return nil
}

// executeTask executes a single task, returning idiomatic errors.
func executeTask(ctx context.Context, callbackerClient *callbackapi.ClientWithResponses) error {
	execer := executor.NewExecutor(taskSingleton, callbackerClient)

	inputResp, err := callbackerClient.GetInputWithResponse(ctx)
	if err != nil {
		return fmt.Errorf("failed to get input: %w", err)
	}
	if inputResp.StatusCode() != 200 || inputResp.JSON200 == nil {
		return fmt.Errorf("failed to get input: status code %d", inputResp.StatusCode())
	}
	taskName := inputResp.JSON200.TaskName
	rawInput := inputResp.JSON200.Input
	var input []interface{}
	err = json.Unmarshal(rawInput, &input)
	if err != nil {
		return fmt.Errorf("failed to unmarshal input: %w", err)
	}

	// We use this to avoid idempotency checks by the server adapter
	err = execer.Execute(ctx, taskName, input...)
	if err != nil {
		return err
	}

	return nil
}

func Register(ctx context.Context, unixSocketPath string) error {
	callbackerClient, err := uds.NewCallbackClient(unixSocketPath)
	if err != nil {
		return fmt.Errorf("failed to create callbacker: %w", err)
	}

	tasks := make([]callbackapi.Task, 0, len(taskSingleton.Tasks))
	for name := range taskSingleton.Tasks {
		tasks = append(tasks, callbackapi.Task{
			Name: name,
		})
	}

	resp, err := callbackerClient.PostRegisterTasksWithResponse(
		ctx,
		callbackapi.PostRegisterTasksJSONRequestBody{
			Tasks: tasks,
		},
	)
	if err != nil {
		return fmt.Errorf("failed to register tasks: %w", err)
	}
	if resp.StatusCode() != 200 {
		return fmt.Errorf("failed to register tasks: status code %d", resp.StatusCode())
	}
	return nil
}
