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

func Run(ctx context.Context, unixSocketPath string) (_err error) {
	callbackerClient, err := uds.NewCallbackClient(unixSocketPath)
	if err != nil {
		return fmt.Errorf("failed to create callbacker: %w", err)
	}

	defer func() {
		var callbackTaskErr *callbackapi.TaskError

		if r := recover(); r != nil {
			stackTrace := string(debug.Stack())
			callbackTaskErr = &callbackapi.TaskError{
				Details:    fmt.Sprintf("task panicked: %v", r),
				StackTrace: &stackTrace,
			}
		} else if _err != nil {
			callbackTaskErr = &callbackapi.TaskError{
				Details: fmt.Sprintf("task failed: %v", _err),
			}
			_err = nil
		} else {
			// No error, nothing to do
			return
		}

		resp, callbackErr := callbackerClient.PostCallbackWithResponse(ctx, callbackapi.PostCallbackJSONRequestBody{
			Error: callbackTaskErr,
		})
		// todo better handle errs?
		if callbackErr != nil {
			_err = callbackErr
			return
		}
		if resp.StatusCode() != 200 {
			_err = fmt.Errorf("callback failed with status code %d", resp.StatusCode())
			return
		}
	}()

	executor := executor.NewExecutor(taskSingleton, callbackerClient)

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
	err = executor.Execute(ctx, taskName, input...)
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
