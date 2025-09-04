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
	"log/slog"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/executor"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/server"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/uds"
)

var taskSingleton = task.NewTasks()

func RegisterTask(task task.Task) error {
	return taskSingleton.RegisterTask(task)
}

// RegisterTaskWithOptions registers a task with configuration options
func RegisterTaskWithOptions(t task.Task, options *Options) error {
	return taskSingleton.RegisterTaskWithOptions(t, options)
}

type TaskContext = task.TaskContext
type Options = task.Options
type Retry = task.Retry

func Start() {
	ctx := context.Background()

	executor := executor.NewExecutor(taskSingleton)

	callbackerClient, err := uds.NewCallbackClient()
	if err != nil {
		slog.ErrorContext(ctx, "Failed to create callbacker", "error", err)
		return
	}
	serverAdapter := server.NewServerAdapter(executor, callbackerClient)

	inputResp, err := callbackerClient.GetInputWithResponse(ctx)
	if err != nil {
		slog.ErrorContext(ctx, "Failed to get input", "error", err)
		return
	}
	if inputResp.StatusCode() != 200 || inputResp.JSON200 == nil {
		slog.ErrorContext(ctx, "unexpected response", "status", inputResp.StatusCode())
		return
	}
	taskName := inputResp.JSON200.TaskName
	rawInput := inputResp.JSON200.Input
	var input []interface{}
	err = json.Unmarshal(rawInput, &input)
	if err != nil {
		slog.ErrorContext(ctx, "Failed to unmarshal input", "error", err, "rawInput", string(rawInput))
		return
	}
	slog.InfoContext(ctx, "Received input", "taskName", taskName, "rawInput", string(rawInput), "input", input)

	// We use this to avoid idempotency checks by the server adapter
	emptyTaskRunID := ""
	err = serverAdapter.StartTask("some response url", taskName, emptyTaskRunID, input...)
	if err != nil {
		slog.ErrorContext(ctx, "Failed to start task", "error", err)
		return
	}
	slog.InfoContext(ctx, "Started task successfully")

	serverAdapter.WaitForTaskComplete()
}
