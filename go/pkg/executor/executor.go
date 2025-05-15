package executor

import (
	"context"
	"log"
	"runtime/debug"

	"render.com/pkg/task"
)

type Executor struct {
	tasks        *task.Tasks
	orchestrator OrchestratorAdapter
	executorDone func(taskID string)
}

type OrchestratorAdapter interface {
	CompleteTask(ctx context.Context, taskName string, result interface{}) error
	ExecuteTask(taskName string, input ...interface{}) ([]interface{}, error)
}

func NewExecutor(tasks *task.Tasks, orchestrator OrchestratorAdapter, executorDone func(taskID string)) *Executor {
	return &Executor{
		tasks:        tasks,
		orchestrator: orchestrator,
		executorDone: executorDone,
	}
}

func (e *Executor) Execute(ctx context.Context, taskName string, taskID string, input ...interface{}) error {
	// Ensure the task is registered
	_, err := e.tasks.GetTaskByName(taskName)
	if err != nil {
		return err
	}

	go func() {
		defer func() {
			if r := recover(); r != nil {
				log.Printf("Recovered from panic: %v", r)
				log.Printf("Stack trace: %s", string(debug.Stack()))
			}
		}()

		log.Printf("Executing task: %s, input: %v", taskName, input)

		result, err := e.tasks.ExecuteTaskByName(taskName, input...)
		if err == nil {
			log.Printf("Task completed: %s", taskName)
			e.orchestrator.CompleteTask(context.Background(), taskName, result)
			e.executorDone(taskID)
		}
	}()

	return nil
}
