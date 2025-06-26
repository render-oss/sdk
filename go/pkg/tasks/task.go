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
	"os"
	"strconv"

	"github.com/renderinc/workflow-sdk/go/pkg/internal/executor"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/server"
	"github.com/renderinc/workflow-sdk/go/pkg/internal/task"
)

var taskSingleton = task.NewTasks()

func RegisterTask(task task.Task) error {
	return taskSingleton.RegisterTask(task)
}

func Start() {
	executor := executor.NewExecutor(taskSingleton)
	serverAdapter := server.NewServerAdapter(executor)
	handler := server.NewServerHandler(taskSingleton, serverAdapter)

	port := os.Getenv("SIDECAR_PORT")
	intPort, err := strconv.Atoi(port)
	if err != nil {
		panic(err)
	}

	srv, err := handler.Start(intPort)
	if err != nil {
		panic(err)
	}
	defer func() {
		_ = srv.Close()
	}()
}

type TaskContext = task.TaskContext
